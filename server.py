#!/usr/bin/env python3
import http.server
import socketserver
import socket

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK\n')
            return
        
        self.send_response(200)
        self.end_headers()
        hostname = socket.gethostname()
        message = f"Hello from {hostname} (Python distroless)!\n"
        self.wfile.write(message.encode())

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server starting on: {PORT}...")
        httpd.serve_forever()