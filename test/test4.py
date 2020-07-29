from http.server import BaseHTTPRequestHandler, HTTPServer # Basic http server
from inspect import currentframe, getframeinfo
from socketserver import ThreadingMixIn
from pathlib import Path, PurePath
import socket
import mimetypes
import os 

class HTTP_File_Server(BaseHTTPRequestHandler):
    def __init__(self, filename, resurl,  *args):
        self.FILENAME = filename
        self.RESURL = resurl
        BaseHTTPRequestHandler.__init__(self, *args)

    def _set_response(self, code, type, length):
        self.send_response(code)
        self.send_header('Content-type', type)
        self.send_header('Content-Length', length)
        self.end_headers()

    def do_GET(self):             
        if self.path == "{}".format(self.RESURL):
            try:
                with open(self.FILENAME, "rb") as f:
                    FILE = f.read()
                    mimetype_inner = mimetypes.guess_type(self.FILENAME)
                    type = mimetype_inner[0]
                    self.send_response(200)
                    self.send_header('Content-type', type)
                    self.send_header('Content-Length', len(FILE))
                    self.end_headers()
                    self.wfile.write(FILE)
            except BaseException as e:
                print(f"Loading File url error: {e}")
        elif self.path == "/":
            try:
                res = "Hello"
                self._set_response(200, "text/html", len(res.encode('utf-8')))
                self.wfile.write(res.encode())
            except BaseException as e:
                print(f"Loading index error: {e}")
        else:
            res = ""
            self._set_response(404, "text/html", len(res.encode('utf-8')))
            self.wfile.write(res.encode())
   

def random_port():
    """function return a random empty port

    Returns:
        port (int): random empty port
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

FILENAME = Path(r"C:\Users\Yusuf\Desktop\Python\Ship\files\test.jpg")    
host = "127.0.0.1"
port = random_port()

def winfileurl(filename):
    FILENAME_IN_URL = str(filename).replace('\\', '/')
    drive, path = os.path.splitdrive(FILENAME_IN_URL)
    return path

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

def HTTP_handler(*args):
    return HTTP_File_Server(FILENAME, winfileurl(FILENAME), *args)

print(f"path to file :{str(FILENAME)}")
print(f"url to access file:{str(winfileurl(FILENAME))}")
print(f"http://{host}:{port}")

print(f"""
os.path.isabs(path): {os.path.isabs(winfileurl(FILENAME))}
os.path.isabs(path): {os.path.isabs('files/test.pdf')}
""")

myserver = ThreadingSimpleServer((host, port), HTTP_handler)

myserver.serve_forever()
  