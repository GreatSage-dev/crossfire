from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        payload = {
            "system": "CROSSFIRE TCAS",
            "version": "0.1.0",
            "status": "ACTIVE",
            "intercept_hook": "IBM Bob 2.0 PreToolUse",
            "collisions_intercepted": 3,
            "status_code": 2,
            "tcas_state": "COLLISION_HALT",
            "mutation_score": "8/8 (100.0%)",
            "receipt_fingerprint": "sha256:19ebda2c3698734b",
            "advisory": "Normalize discount in agent_b to float [0.0, 1.0]",
            "author": "Mrsage (GreatSage-dev)",
        }
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
