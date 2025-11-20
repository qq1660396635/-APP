# server.py
import http.server
import socketserver

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("服务器运行在 http://localhost:{}".format(PORT))
    httpd.serve_forever()
