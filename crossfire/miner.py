"""AST-based invariant claim miner for extracting value domain, state lifecycle, and error contracts."""

import ast
from typing import Optional

from crossfire.models import InvariantClaim, MinerError

_LIFECYCLE_KEYWORDS = {
    "evict",
    "purge",
    "delete",
    "destroy",
    "invalidate",
    "clean",
    "cleanup",
    "flush",
    "expire",
    "lifecycle",
    "teardown",
    "drop",
    "session",
    "cache",
    "sync",
    "async",
}


class _ValueDomainVisitor(ast.NodeVisitor):
    """AST visitor that detects and extracts invariant claims across all 3 contract classes:
    - value_domain (e.g. float[0.0, 1.0] vs int[0, 100])
    - state_lifecycle (async vs sync)
    - error_contract (raises[...] vs returns_none)
    """

    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        # Key: (symbol, domain, contract_type, line) -> max confidence
        self._claims_map: dict[tuple[str, str, str, int], float] = {}
        self._current_function_params: set[str] = set()

    def add_claim(
        self,
        symbol: str,
        domain: str,
        line: int,
        confidence: float,
        contract_type: str = "value_domain",
    ) -> None:
        """Register a mined claim, keeping the highest confidence for duplicates."""
        if not symbol or not symbol.strip() or line < 1:
            return
        key = (symbol.strip(), domain.strip(), contract_type, line)
        if key not in self._claims_map or confidence > self._claims_map[key]:
            self._claims_map[key] = confidence

    def get_claims(self) -> list[InvariantClaim]:
        """Convert collected claim records into validated InvariantClaim instances."""
        claims = [
            InvariantClaim(
                agent_id=self.agent_id,
                symbol=symbol,
                domain=domain,
                contract_type=contract_type,  # type: ignore[arg-type]
                source_line=line,
                confidence=round(confidence, 4),
            )
            for (symbol, domain, contract_type, line), confidence in self._claims_map.items()
        ]
        # Deterministic sorting by source line, then symbol
        claims.sort(key=lambda c: (c.source_line, c.symbol))
        return claims

    def _infer_symbol_name(
        self, other_node: Optional[ast.AST], fallback: str = "discount"
    ) -> str:
        """Dynamically identify the invariant symbol name without hardcoded keyword gates."""
        if isinstance(other_node, ast.Name):
            return other_node.id
        if isinstance(other_node, ast.Attribute):
            return other_node.attr
        # Check active function parameters
        for param in self._current_function_params:
            return param
        return fallback

    def _get_exception_name(self, node: Optional[ast.AST]) -> Optional[str]:
        """Extract exception class name from AST node."""
        if node is None:
            return None
        if isinstance(node, ast.Call):
            return self._get_exception_name(node.func)
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return None

    def _get_call_name(self, node: Optional[ast.AST]) -> Optional[str]:
        """Extract function or method call name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return None

    def _inspect_lifecycle(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Inspect function definition for state lifecycle contract (async vs sync)."""
        is_async = isinstance(node, ast.AsyncFunctionDef)
        name_lower = node.name.lower()
        docstring = ast.get_docstring(node) or ""
        doc_lower = docstring.lower()

        if is_async:
            self.add_claim(
                symbol=node.name,
                domain="async",
                line=node.lineno,
                confidence=0.95,
                contract_type="state_lifecycle",
            )
        else:
            has_lifecycle_term = any(term in name_lower for term in _LIFECYCLE_KEYWORDS)
            has_lifecycle_doc = any(
                term in doc_lower
                for term in ("lifecycle", "synchronous", "asynchronous", "evict", "purge", "deletion")
            )
            if has_lifecycle_term or has_lifecycle_doc:
                self.add_claim(
                    symbol=node.name,
                    domain="sync",
                    line=node.lineno,
                    confidence=0.95,
                    contract_type="state_lifecycle",
                )

    def _inspect_error_contracts(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Inspect function definition for error contracts (returns_none vs raises[...])."""
        for child in ast.walk(node):
            if child is not node and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if isinstance(child, ast.Raise) and child.exc is not None:
                exc_name = self._get_exception_name(child.exc)
                if exc_name:
                    self.add_claim(
                        symbol=node.name,
                        domain=f"raises[{exc_name}]",
                        line=child.lineno,
                        confidence=0.95,
                        contract_type="error_contract",
                    )
            elif isinstance(child, ast.Return):
                if isinstance(child.value, ast.Constant) and child.value.value is None:
                    self.add_claim(
                        symbol=node.name,
                        domain="returns_none",
                        line=child.lineno,
                        confidence=0.95,
                        contract_type="error_contract",
                    )

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Inspect async function definitions for lifecycle and error contracts."""
        self._inspect_lifecycle(node)
        self._inspect_error_contracts(node)
        previous_params = self._current_function_params
        self._current_function_params = {arg.arg for arg in node.args.args}
        self.generic_visit(node)
        self._current_function_params = previous_params

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Inspect function parameter annotations, default values, lifecycle, and errors."""
        self._inspect_lifecycle(node)
        self._inspect_error_contracts(node)

        previous_params = self._current_function_params
        self._current_function_params = {arg.arg for arg in node.args.args}

        # Check positional/keyword arguments with defaults
        defaults = node.args.defaults
        args = node.args.args
        if defaults:
            num_defaults = len(defaults)
            args_with_defaults = args[-num_defaults:]
            for arg, default in zip(args_with_defaults, defaults):
                self._inspect_arg_default(arg, default, node.lineno)

        # Check kw-only arguments with defaults
        for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults):
            if default is not None:
                self._inspect_arg_default(arg, default, node.lineno)

        # Continue traversing the function body
        self.generic_visit(node)
        self._current_function_params = previous_params

    def _inspect_arg_default(self, arg: ast.arg, default: ast.AST, lineno: int) -> None:
        """Check whether default argument values denote float or int percentage domains."""
        symbol = arg.arg
        line = getattr(arg, "lineno", lineno)
        if isinstance(default, ast.Constant):
            val = default.value
            if isinstance(val, float) and 0.0 <= val <= 1.0:
                self.add_claim(symbol=symbol, domain="float[0.0, 1.0]", line=line, confidence=0.85)
            elif isinstance(val, int) and not isinstance(val, bool) and 1 < val <= 100:
                self.add_claim(symbol=symbol, domain="int[0, 100]", line=line, confidence=0.85)
            elif isinstance(val, int) and val in (0, 1):
                # Check type annotation if available
                if arg.annotation and isinstance(arg.annotation, ast.Name):
                    if arg.annotation.id == "float":
                        self.add_claim(symbol=symbol, domain="float[0.0, 1.0]", line=line, confidence=0.85)
                    elif arg.annotation.id == "int":
                        self.add_claim(symbol=symbol, domain="int[0, 100]", line=line, confidence=0.85)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Detect direct variable assignments specifying domain invariants."""
        if isinstance(node.value, ast.Constant):
            val = node.value.value
            for target in node.targets:
                if isinstance(target, ast.Name):
                    symbol = target.id
                    if isinstance(val, float) and 0.0 <= val <= 1.0:
                        self.add_claim(symbol=symbol, domain="float[0.0, 1.0]", line=node.lineno, confidence=0.85)
                    elif isinstance(val, int) and not isinstance(val, bool) and 1 < val <= 100:
                        self.add_claim(symbol=symbol, domain="int[0, 100]", line=node.lineno, confidence=0.85)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Detect annotated assignments specifying domain invariants."""
        if isinstance(node.target, ast.Name) and node.value and isinstance(node.value, ast.Constant):
            symbol = node.target.id
            val = node.value.value
            if isinstance(val, float) and 0.0 <= val <= 1.0:
                self.add_claim(symbol=symbol, domain="float[0.0, 1.0]", line=node.lineno, confidence=0.90)
            elif isinstance(val, int) and not isinstance(val, bool) and 1 < val <= 100:
                self.add_claim(symbol=symbol, domain="int[0, 100]", line=node.lineno, confidence=0.90)
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        """Inspect assertion test expressions for boundary comparisons using ast.walk()."""
        for subnode in ast.walk(node.test):
            if isinstance(subnode, ast.Compare):
                self._inspect_compare(subnode, node.lineno)
        self.generic_visit(node)

    def _inspect_compare(self, compare: ast.Compare, lineno: int) -> None:
        """Analyze a comparison expression for value domain bounds."""
        # Case 1: Chained boundary comparison (e.g. 0.0 <= discount <= 1.0 or 0 <= discount <= 100)
        if len(compare.ops) == 2 and len(compare.comparators) == 2:
            left_node = compare.left
            mid_node = compare.comparators[0]
            right_node = compare.comparators[1]

            if isinstance(mid_node, ast.Name):
                symbol = mid_node.id
                op1 = compare.ops[0]
                op2 = compare.ops[1]

                # Check for standard ascending order: low <= x <= high
                if isinstance(op1, (ast.Lt, ast.LtE)) and isinstance(op2, (ast.Lt, ast.LtE)):
                    low_val = left_node.value if isinstance(left_node, ast.Constant) else None
                    high_val = right_node.value if isinstance(right_node, ast.Constant) else None
                    self._evaluate_bounds(symbol, low_val, high_val, lineno)

                # Check for descending order: high >= x >= low
                elif isinstance(op1, (ast.Gt, ast.GtE)) and isinstance(op2, (ast.Gt, ast.GtE)):
                    low_val = right_node.value if isinstance(right_node, ast.Constant) else None
                    high_val = left_node.value if isinstance(left_node, ast.Constant) else None
                    self._evaluate_bounds(symbol, low_val, high_val, lineno)

        # Case 2: Single upper bound comparison (e.g. x <= 1.0 or x <= 100)
        elif len(compare.ops) == 1 and len(compare.comparators) == 1:
            op = compare.ops[0]
            comp = compare.comparators[0]
            if isinstance(compare.left, ast.Name) and isinstance(comp, ast.Constant):
                symbol = compare.left.id
                val = comp.value
                if isinstance(op, (ast.Lt, ast.LtE)):
                    if isinstance(val, float) and val <= 1.0:
                        self.add_claim(symbol=symbol, domain="float[0.0, 1.0]", line=lineno, confidence=0.90)
                    elif isinstance(val, int) and not isinstance(val, bool) and val == 100:
                        self.add_claim(symbol=symbol, domain="int[0, 100]", line=lineno, confidence=0.90)

    def _evaluate_bounds(self, symbol: str, low_val: object, high_val: object, lineno: int) -> None:
        """Infer domain based on boundary numerical values."""
        if low_val is None or high_val is None:
            return

        is_float_bound = isinstance(low_val, float) or isinstance(high_val, float)

        if is_float_bound and high_val == 1.0:
            self.add_claim(symbol=symbol, domain="float[0.0, 1.0]", line=lineno, confidence=1.0)
        elif not is_float_bound and high_val == 100 and low_val == 0:
            self.add_claim(symbol=symbol, domain="int[0, 100]", line=lineno, confidence=1.0)
        elif high_val == 1.0 and low_val == 0:
            self.add_claim(symbol=symbol, domain="float[0.0, 1.0]", line=lineno, confidence=1.0)
        elif high_val == 100:
            self.add_claim(symbol=symbol, domain="int[0, 100]", line=lineno, confidence=0.95)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Detect literal percentage multiplications (e.g., price * 15 vs price * 0.15) and (1.0 - discount)."""
        # Case A: Subtractions such as (1.0 - discount) or (100 - discount)
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.BinOp) and isinstance(subnode.op, ast.Sub):
                if isinstance(subnode.left, ast.Constant):
                    if subnode.left.value == 1.0 and isinstance(subnode.right, ast.Name):
                        self.add_claim(
                            symbol=subnode.right.id,
                            domain="float[0.0, 1.0]",
                            line=subnode.lineno,
                            confidence=0.90,
                        )
                    elif subnode.left.value == 100 and isinstance(subnode.right, ast.Name):
                        self.add_claim(
                            symbol=subnode.right.id,
                            domain="int[0, 100]",
                            line=subnode.lineno,
                            confidence=0.90,
                        )

        # Case B: Literal percentage multiplications (price * 15 vs price * 0.15)
        if isinstance(node.op, ast.Mult):
            lit = None
            other = None
            if isinstance(node.left, ast.Constant) and isinstance(node.left.value, (int, float)):
                lit = node.left.value
                other = node.right
            elif isinstance(node.right, ast.Constant) and isinstance(node.right.value, (int, float)):
                lit = node.right.value
                other = node.left

            if lit is not None and not isinstance(lit, bool):
                symbol = self._infer_symbol_name(other, fallback="discount")
                if isinstance(lit, float) and 0.0 < lit <= 1.0:
                    self.add_claim(
                        symbol=symbol,
                        domain="float[0.0, 1.0]",
                        line=node.lineno,
                        confidence=0.85,
                    )
                elif isinstance(lit, int) and 1 < lit <= 100:
                    self.add_claim(
                        symbol=symbol,
                        domain="int[0, 100]",
                        line=node.lineno,
                        confidence=0.85,
                    )

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Detect function calls passing numeric boundary arguments across any parameter name."""
        for kw in node.keywords:
            if kw.arg and isinstance(kw.value, ast.Constant):
                val = kw.value.value
                if isinstance(val, float) and 0.0 <= val <= 1.0:
                    self.add_claim(
                        symbol=kw.arg,
                        domain="float[0.0, 1.0]",
                        line=node.lineno,
                        confidence=0.85,
                    )
                elif isinstance(val, int) and not isinstance(val, bool) and 1 < val <= 100:
                    self.add_claim(
                        symbol=kw.arg,
                        domain="int[0, 100]",
                        line=node.lineno,
                        confidence=0.85,
                    )
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        """Detect error contract expectations in try/except blocks."""
        for handler in node.handlers:
            exc_name = self._get_exception_name(handler.type)
            if exc_name:
                for subnode in ast.walk(node):
                    if isinstance(subnode, ast.Call):
                        callee = self._get_call_name(subnode.func)
                        if callee:
                            self.add_claim(
                                symbol=callee,
                                domain=f"raises[{exc_name}]",
                                line=handler.lineno,
                                confidence=0.90,
                                contract_type="error_contract",
                            )
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        """Detect caller comparisons against None (e.g. if get_item() is None)."""
        if len(node.ops) == 1 and isinstance(node.ops[0], (ast.Is, ast.Eq)):
            if isinstance(node.comparators[0], ast.Constant) and node.comparators[0].value is None:
                if isinstance(node.left, ast.Call):
                    callee = self._get_call_name(node.left.func)
                    if callee:
                        self.add_claim(
                            symbol=callee,
                            domain="returns_none",
                            line=node.lineno,
                            confidence=0.90,
                            contract_type="error_contract",
                        )
        self.generic_visit(node)


def extract_claims(source: str, agent_id: str) -> list[InvariantClaim]:
    """Extract invariant claims from Python source code across all contract types.

    Uses pure Python ast parsing with NodeVisitor to discover value domain
    assertions, argument defaults, assignments, literal multiplications,
    state lifecycle models (async vs sync), and error contracts.

    Args:
        source: Python source code as a string.
        agent_id: Unique identifier for the agent or module claiming the invariants.

    Returns:
        A list of InvariantClaim objects extracted from the source code.

    Raises:
        MinerError: If source code has syntax errors or cannot be parsed.
    """
    if not source or not source.strip():
        return []

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise MinerError(f"Failed to parse source code for agent '{agent_id}': {e}") from e

    visitor = _ValueDomainVisitor(agent_id=agent_id)
    visitor.visit(tree)
    return visitor.get_claims()
