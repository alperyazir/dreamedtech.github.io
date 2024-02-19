# Based on:
# https://stackoverflow.com/a/21957017
# https://gist.github.com/HaiyangXu/ec88cbdce3cdbac7b8d5

from http.server import SimpleHTTPRequestHandler
import socketserver
import socket
import sys
import os
import webbrowser

new = 2  # open in a new tab, if possible


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        "": "application/octet-stream",
        ".css": "text/css",
        ".html": "text/html",
        ".jpg": "image/jpg",
        ".js": "application/x-javascript",
        ".json": "application/json",
        ".manifest": "text/cache-manifest",
        ".png": "image/png",
        ".wasm": "application/wasm",
        ".xml": "application/xml",
    }

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        SimpleHTTPRequestHandler.end_headers(self)


def is_port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(("localhost", port))
    sock.close()
    return result == 0


def close_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    sock.connect(("localhost", port))
    sock.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # html_directory = os.path.join(current_directory, 'data')
    # filename = os.path.join(html_directory, 'flow.html')
    url = "http://localhost:8000/FlowBook.html"
    if is_port_open(port):
        print(f"Port {port} is already open.")
        webbrowser.open(url, new=new)
        # exit()
    else:
        with socketserver.TCPServer(("localhost", port), Handler) as httpd:
            print("Serving on port", port)

            webbrowser.open(url, new=new)
            httpd.serve_forever()
