import os
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
from inspect import currentframe, getframeinfo
# Get line 

if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
    #running in a PyInstaller bundle
    from .templates import BASE_TEMPLATE, TEMPLATE_ERROR, FULL_TEMPLATE
    from .templates import TEMPLATE_AUDIO, TEMPLATE_IMAGE, TEMPLATE_TEXT, TEMPLATE_VIDEO
    from .templates import TEMPLATE_PDF
    #files
    bdir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    ICO_FILENAME = os.path.join(bdir, "files/favicon.ico")
    JS_FILENAME = os.path.join(bdir, "files/demo_defer.js")
else:
    #running in a normal Python process
    from templates import BASE_TEMPLATE, TEMPLATE_ERROR, FULL_TEMPLATE
    from templates import TEMPLATE_AUDIO, TEMPLATE_IMAGE, TEMPLATE_TEXT, TEMPLATE_VIDEO
    from templates import TEMPLATE_PDF
    # files
    ICO_FILENAME = os.path.join(os.path.dirname(__file__), "favicon.ico") 
    JS_FILENAME = os.path.join(os.path.dirname(__file__), "demo_defer.js")
    
# source env/bin/activate

# rm -rf build dist
# python3.7 -m PyInstaller cli.spec
# [("ship/favicon.ico", "files"), ("ship/demo_defer.js", "files")]

# git init
# git status
# git add .
# git commit -m "alpha release v0.0.1.x"
# git push origin master

# git tag -a v0.0.1.x -m "alpha release v0.0.1.x"
# git push origin v0.0.1.x

# cli stuff
parser = argparse.ArgumentParser(description="""Send file to phone or other computers. Make sure to kill this process after completetion""")
parser.add_argument('file', type=str, nargs='?', help='file to be shared')
parser.add_argument('-p','--port', type=int ,default=9999, metavar='file', nargs='?', help='port to be shared one')
args = parser.parse_args()

def local_address():
    """Return the/a network-facing IP number for this system."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.connect(("google.com", 80))
    local = s.getsockname()[0]
    s.close()
    return local

# CONST
# http server config
HOST = local_address()
PORT = args.port

# sharing file config
FILENAME, frameinfo = args.file, getframeinfo(currentframe())
#FILENAME = args.file
if type(FILENAME) != str:
    raise SystemExit("Ship: line {}: filename argument can only be of type string not {}".format(frameinfo.lineno , type(FILENAME)))
try:
    MIMETYPE, frameinfo = mimetypes.guess_type(FILENAME), getframeinfo(currentframe())
    #MIMETYPE = mimetypes.guess_type(FILENAME)
    TYPE = MIMETYPE[0].split("/")[0]
except:
    rep = """please report file type on the github issues page:\nhttps://github.com/yusuf8ahmed/Ship/issues """
    raise SystemExit("""Ship: line {}: file type is not supported {}, {}\n{}""".format(frameinfo.lineno, FILENAME, MIMETYPE,rep))
try:
    with open(FILENAME, "rb") as f:
        FILE = f.read()
except BaseException as e:
    raise SystemExit("Ship: file reading error ({}) : {}".format(FILENAME,e)) 

# favicon config
try:
    with open(ICO_FILENAME, "rb") as f:
        ICO = f.read()
except BaseException as e:
    raise SystemExit("Ship: favicon reading error ({}) : {}".format(FILENAME,e))  

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
    try:
        r = BASE_TEMPLATE.format(**{
            "TEMPLATE":TYPES.get(name).format(**settings),
            "HOST": HOST,
            "PORT":PORT})
    except BaseException as e:
        print(e)
        try:
            settings.update({"HOST": HOST, "PORT":PORT})
            r = TYPES_SPECIAL.get(settings['MIMETYPE']).format(**settings)
        except BaseException as e:
            r = FULL_TEMPLATE.format(**settings)
    return r

def main():
    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/{}".format(FILENAME):
                self.log_message("Loading {}, {}".format(FILENAME, MIMETYPE[0]))
                self.send_response(200, "OK")
                self.send_header("Content-Type", MIMETYPE[0])
                self.send_header('Content-Length', len(FILE))
                self.end_headers()
                self.wfile.write(FILE)

            elif self.path == "/files/favicon.ico":
                self.log_message("Loading favicon")
                self.send_response(200, "OK")
                self.send_header("Content-Type", "image/x-icon")
                self.send_header('Content-Length', len(ICO))
                self.end_headers()
                self.wfile.write(ICO)

            elif self.path == "/demo_defer.js":
                with open(JS_FILENAME, "rb") as f:
                    JS = f.read()
                self.log_message("Loading pdfjs")
                self.send_response(200, "OK")
                self.send_header("Content-Type", "text/javascript")
                self.send_header('Content-Length', len(JS))
                self.end_headers()
                self.wfile.write(JS)

            elif self.path == "/":
                self.log_message("Loading in main")
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
                self.log_message("Loading in error")
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
    print("Make sure to click 'ctrl-c' to kill after usage")
    print("{} Sharing Server Starts {} - http://{}:{}".format(time.asctime(),TYPE,HOST,PORT))
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        myServer.server_close()
        print("{} Sharing Server Stop - http://{}:{}".format(time.asctime(),HOST,PORT))
        sys.exit()
        pass
    myServer.server_close()
    print("{} Sharing Server Stop - http://{}:{}".format(time.asctime(),HOST,PORT))

if __name__ == "__main__":
    main()
