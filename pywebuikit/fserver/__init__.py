from __future__ import annotations
import http.server

from .. import webwindow

def make_fsh(cv: webwindow.WebWindow):
    class _FileServerHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "*")
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            self.end_headers()
            self.wfile.write(cv.fserver_res.get(self.path))
        
        def log_request(self, *args, **kwargs) -> None: ...
    
    return _FileServerHandler