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
with open(FILENAME, "rb") as f:
    FILE = f.read()
MIMETYPE = mimetypes.guess_type(FILENAME)
TYPE = MIMETYPE[0].split("/")[0]
# favicon config
ICO_FILENAME = "favicon.ico"
with open(ICO_FILENAME, "rb") as f:
    ICO = f.read()

# transfer files
# audio
# -
# image
# -jpg, png, gif (Working)
# text
# -TXT (Working)
# video
# -MOV (Working)

# HTML templates
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>Page Title</title>
        <link rel="shortcut icon" href="/files/favicon.ico" type="image/x-icon">
    </head>
    <body>
        <p style="">Testing: Basically giphy on crack but only served localy</p>
        {TEMPLATE}
    </body>
</html>
"""
TEMPLATE_AUDIO = """
<div style="display:flex; justify-content:center;">
    <a href="{FILENAME}" download>
        <audio controls>
            <source src="{FILENAME}" type="{MIMETYPE}">
            Your browser does not support the audio element.
        </audio>
        <p style="margin-top: 3;">Click this to download and wait two seconds</p>
    </a>
</div>
"""
TEMPLATE_IMAGE = """
<p>Filename: {FILENAME}</p>
<div style="display:flex; justify-content:center;">
    <a href="{FILENAME}" download>
        <img src="{FILENAME}" alt="document" style="height:500px; width:auto;">
        <p style="margin-top: 3;">Click this to download and wait two seconds</p>
    </a>
</div>
"""
TEMPLATE_TEXT = """
<p>Filename: {FILENAME}</p>
<div style="display:flex; justify-content:center;">
    <a href="{FILENAME}" download>
        <embed src="{FILENAME}">
        <p style="margin-top: 3;">Click this to download and wait two seconds</p>
    </a>
</div
"""
TEMPLATE_VIDEO = """
<p>Filename: {FILENAME}</p>
<div style="display:flex; justify-content:center;">
    <video width="320" height="500" src="{FILENAME}" preload controls></video>
    <a href="{FILENAME}" download>
        <p style="margin-top: 3;">Click this to download and wait two seconds</p>
    </a>
</div
"""
TEMPLATE_ERROR = """
<div style="display:flex; justify-content:center;">
    <a href="http://{HOST}:{PORT}">Return to home</a>
</div
"""

TYPES = {
    "audio":TEMPLATE_AUDIO ,
    "image":TEMPLATE_IMAGE,        
    "text":TEMPLATE_TEXT,
    "video":TEMPLATE_VIDEO,
    "error":TEMPLATE_ERROR,
}

def get_response(name, settings):
    return BASE_TEMPLATE.format(**{"TEMPLATE":TYPES.get(name).format(**settings),"HOST": HOST,"PORT":PORT})

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
            elif self.path == "/":
                self.log_message(f"Loading in main")
                res = get_response(TYPE, {"FILENAME":FILENAME,"MIMETYPE":MIMETYPE[0]})
                self.send_response(200, "OK")
                self.send_header("Content-type", "text/html")
                self.send_header('Content-Length', len(res.encode('utf-8')))
                self.end_headers()
                self.wfile.write(res.encode())
            else:
                self.log_message(f"Loading in error")
                res = get_response("error", {"HOST":HOST,"PORT":PORT})
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