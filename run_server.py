import http.server
import socketserver
import os

PORT = 8081
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Hanwha Ocean RPA Portfolio Server active at:")
        print(f"🔗 http://127.0.0.1:{PORT}/index.html")
        print("\nPress CTRL+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 RPA Server shutdown by user.")
            httpd.shutdown()

if __name__ == "__main__":
    run()
