import http.server
import json
from socketserver import ThreadingTCPServer
from threading import Thread

class CommandServerRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        data = {}
        data["error"] = 0

        if self.path == "/":
            data["result"] = self.handle_base()
        else:
            data["error"] = 404
            data["error_description"] = "%s is not a valid action" % (self.path,)

        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_base(self):
        return {
            "receiver_count" : len(self.server._bridge._receivers),
            "sender_count" : len(self.server._bridge._senders)
        }




class CommandServer(Thread, ThreadingTCPServer):
    def __init__(self, host, port, bridge):
        Thread.__init__(self, name="CommandServer")
        ThreadingTCPServer.__init__(self, (host, port), CommandServerRequestHandler)
        self._bridge = bridge

    def run(self):
        self.serve_forever()