import http.server
import socketserver
import os
import logging

# Enterprise Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | [%(levelname)s] | %(name)s : %(message)s'
)
logger = logging.getLogger("AX-Server")

PORT = 8081
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        # Override to use professional logger
        logger.info("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("\n" + "="*60)
        print("⚓ HANWHA OCEAN SMART YARD AX: MISSION CONTROL CENTER")
        print("🚀 Enterprise Quantum Elite v25.0.0 Status: ACTIVE")
        print("="*60)
        logger.info(f"Command Center Gateway: http://127.0.0.1:{PORT}/index.html")
        logger.info(f"Strategic Dashboard: http://127.0.0.1:{PORT}/smart_yard_dashboard.html")
        print("="*60 + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("RPA Server shutdown sequence initiated by administrator.")
            httpd.shutdown()

if __name__ == "__main__":
    run()
