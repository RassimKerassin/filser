#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import os
import argparse

class CustomHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        filename = os.path.basename(urlparse(self.path).path)
        with open(filename, 'wb') as f:
            f.write(data)
        self.send_response(200)
        self.end_headers()
        response = b'PUT request received'
        self.wfile.write(response)

    def do_GET(self):
        filename = os.path.basename(urlparse(self.path).path)
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")

def run(server_class=HTTPServer, handler_class=CustomHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server...")
        httpd.server_close()

def main():
    parser = argparse.ArgumentParser(description='Simple HTTP file server')
    parser.add_argument('port', nargs='?', type=int, default=80, help='Port number')
    args = parser.parse_args()

    run(port=args.port)

if __name__ == '__main__':
    main()
