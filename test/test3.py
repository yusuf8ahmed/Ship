from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import socket
import webbrowser

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello world\t' + threading.currentThread().getName().encode() + b'\t' + str(threading.active_count()).encode() + b'\n')

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0
    server = ThreadingSimpleServer((HOST, PORT), Handler)
   
    ip, port = server.server_address
    url = "http://{}:{}".format(ip, port)
    print(url)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    webbrowser.open(url=url)

    while True:
        try:
            pass
        except KeyboardInterrupt:
            break
    server.shutdown()
    server.server_close()