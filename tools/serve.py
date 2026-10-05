"""Lokale Vorschau ohne Cache: python3 tools/serve.py [port]"""
import http.server, os, sys, functools
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site')
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            body = open(os.path.join(ROOT, '404.html'), 'rb').read()
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
        super().send_error(code, message, explain)
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 8771), functools.partial(H, directory=ROOT)).serve_forever()
