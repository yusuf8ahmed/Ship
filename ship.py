# Logging
import time
# for exiting
import sys
# get local ip address
import socket
# cli 
import argparse
# to find mimetype of specific files
import mimetypes
# Basic http server
from http.server import BaseHTTPRequestHandler, HTTPServer
# HTML templates
from templates import BASE_TEMPLATE, TEMPLATE_ERROR, FULL_TEMPLATE
from templates import TEMPLATE_APPLICATION, TEMPLATE_AUDIO, TEMPLATE_IMAGE, TEMPLATE_TEXT, TEMPLATE_VIDEO
from templates import TEMPLATE_PDF

# source env/bin/activate

# cli stuff
parser = argparse.ArgumentParser(description="""Send file to phone or other computers. Make sure to kill this process after completetion""")
parser.add_argument('file', metavar='file', type=str, nargs='?', help='file to be shared')
args = parser.parse_args()

# global const
# http server config
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
# share file config
FILENAME = args.file
if FILENAME == None:
    print("""file param cannot be "None" be sure to include a file""")
    sys.exit()
try:
    with open(FILENAME, "rb") as f:
        FILE = f.read()
except BaseException as e:
    print(f"File error: {e}")
    sys.exit()  
MIMETYPE = mimetypes.guess_type(FILENAME)
TYPE = MIMETYPE[0].split("/")[0]
# favicon config
ICO_FILENAME = "favicon.ico"
try:
    with open(ICO_FILENAME, "rb") as f:
        ICO = f.read()
except BaseException as e:
    print(f"file reading error: {e}")
    sys.exit()  
print(MIMETYPE)

# transfer files
# audio
# -
# image
# -jpg, png, gif (Working)
# text
# -txt, pdf (Working)
# video
# -mov (Working)

TYPES = {
    "audio":TEMPLATE_AUDIO ,
    "image":TEMPLATE_IMAGE,        
    "text":TEMPLATE_TEXT,
    "video":TEMPLATE_VIDEO,
    "error":TEMPLATE_ERROR,
}

TYPES_SPECIAL = {
    "application/pdf": TEMPLATE_PDF,
}

def get_response(name, settings):
    # application 
    # {'FILENAME': 'files/a.pdf', 'MIMETYPE': 'application/pdf', 'HOST': '192.168.44.241', 'PORT': 9999 }
    try:
        r = BASE_TEMPLATE.format(**{
            "TEMPLATE":TYPES.get(name).format(**settings),
            "HOST": HOST,
            "PORT":PORT})
    except:
        try:
            r = TYPES_SPECIAL.get(settings['MIMETYPE']).format(**{
                **settings,
                "HOST": HOST,
                "PORT":PORT})
        except:
            # https://stackoverflow.com/a/46315848
            r = FULL_TEMPLATE.format(**settings)
    return r

def main():
    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == f"/{FILENAME}":
                self.log_message(f"Loading {FILENAME}, {MIMETYPE}")
                self.send_response(200, "OK")
                self.send_header("Content-Type", MIMETYPE[0])
                self.send_header('Content-Length', len(FILE))
                self.end_headers()
                self.wfile.write(FILE)

            elif self.path == f"/files/favicon.ico":
                self.log_message(f"Loading favicon")
                self.send_response(200, "OK")
                self.send_header("Content-Type", "image/x-icon")
                self.send_header('Content-Length', len(ICO))
                self.end_headers()
                self.wfile.write(ICO)

            elif self.path == f"/demo_defer.js":
                JS_FILENAME = "demo_defer.js"
                try:
                    with open(JS_FILENAME, "rb") as f:
                        JS = f.read()
                    self.log_message(f"Loading pdfjs")
                    self.send_response(200, "OK")
                    self.send_header("Content-Type", "text/javascript")
                    self.send_header('Content-Length', len(JS))
                    self.end_headers()
                    self.wfile.write(JS)
                except BaseException as e:
                    print(f"file reading error: {e}")
                    self.log_message(f"Loading demo")
                    res = get_response("error", {"HOST":HOST,"PORT":PORT,"MESSAGE":"This is an illegal route"})
                    self.send_response(404, "Not Found")
                    self.send_header("Content-type", "text/html")
                    self.send_header('Content-Length', len(res.encode('utf-8')))
                    self.end_headers()
                    self.wfile.write(res.encode())
                    sys.exit() 


            elif self.path == "/":
                self.log_message(f"Loading in main")
                res = get_response(TYPE, {
                    "FILENAME":FILENAME,
                    "MIMETYPE":MIMETYPE[0],
                    "HOST":HOST,
                    "PORT":PORT})
                self.send_response(200, "OK")
                self.send_header("Content-type", "text/html")
                self.send_header('Content-Length', len(res.encode('utf-8')))
                self.end_headers()
                self.wfile.write(res.encode())

            else:
                self.log_message(f"Loading in error")
                res = get_response("error", {
                    "HOST":HOST,
                    "PORT":PORT,
                    "MESSAGE":"This is an illegal route"
                    })
                self.send_response(404, "Not Found")
                self.send_header("Content-type", "text/html")
                self.send_header('Content-Length', len(res.encode('utf-8')))
                self.end_headers()
                self.wfile.write(res.encode())

    myServer = HTTPServer((HOST, PORT), MyServer)
    myServer.request_queue_size = 2
    print("Make sure to click 'ctrl-c' to kill after usage")
    print(time.asctime(), f"Sharing Server Starts - http://{HOST}:{PORT}")
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        sys.exit()
        pass
    myServer.server_close()
    print(time.asctime(), f"Sharing Server Stop - http://{HOST}:{PORT}")

if __name__ == "__main__":
    main()