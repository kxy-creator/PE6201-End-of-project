"""Loopback-only demonstration UI. No authentication or production submission."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
from src.hrask import HRAsk
APP=HRAsk()
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        if self.path!='/':self.send_error(404);return
        data=Path(__file__).with_name('demo.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(data)
    def do_POST(self):
        if self.path!='/ask':self.send_error(404);return
        if self.headers.get('Origin') not in [None,'http://127.0.0.1:8765','http://localhost:8765']:self.send_error(403);return
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<=0 or n>12000:raise ValueError('Invalid request size')
            body=json.loads(self.rfile.read(n));mode=body.get('mode','offline')
            if mode not in ['offline','openai','openrouter']:raise ValueError('Invalid mode')
            data=json.dumps(APP.ask(body['question'],mode),ensure_ascii=False).encode()
            self.send_response(200);self.send_header('Content-Type','application/json; charset=utf-8');self.end_headers();self.wfile.write(data)
        except (ValueError,KeyError):self.send_error(400,'Invalid question')
if __name__=='__main__':
    print('HR-Ask demo: http://127.0.0.1:8765',flush=True)
    HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
