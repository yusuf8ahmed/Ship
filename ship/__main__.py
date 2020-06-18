#!/usr/bin/env python3
#source env/bin/activate

# version
version = "0.0.1.7"

# Third party package
import qrcode #load qrcode

# Standard package
import os # os.path operations
import time # Logging
import sys # for exiting
import socket # get local ip address
import argparse # cli
import mimetypes # to find mimetype of specific files
from http.server import BaseHTTPRequestHandler, HTTPServer # Basic http server
from inspect import currentframe, getframeinfo # Get line number

# Local Import 
from HTTPFileserver import HTTP_File_Server
# Color for terminal
from colors import Colors

# Files 
ICO_FILENAME = os.path.join(os.path.dirname(__file__), "favicon.ico") 
JS_FILENAME = os.path.join(os.path.dirname(__file__), "demo_defer.js")

# QRcode
QR = qrcode.QRCode()

#COMMAND LINE ARGUMENTS
qr_help = "if your phone is having trouble reading QRcode use flag -q:{} ship -q [FILENAME]{}".format(Colors.Green,Colors.Reset)

parser = argparse.ArgumentParser(
    description="""Send file to phone or other computers. Make sure to kill this process after completetion\n{}""".format(qr_help)
    , formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('file', type=str, nargs='?', help='file to be shared')
parser.add_argument('-p','--port', type=int, default=9999, metavar='port', nargs='?', help='port to be shared one')
parser.add_argument('-q','--qrcode', action='store_true', help='if flagged qrcode will be in new tab')
parser.add_argument('-V', '--version', action='version', version="Ship {}".format(version))
args = parser.parse_args()

def local_address():
    """
    Description: returns a network-facing IP number for this system.

    Returns:
        ip_address (str)
    """
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    socket_obj.connect(("google.com", 80))
    ip_address = socket_obj.getsockname()[0]
    socket_obj.close()
    return ip_address

def display_qrcode(option, data):
    """
    Description: display qrcode either in terminal or new window
    
    Args:
        option (bool): in line (False) vs new/split tab (True) QR code
        data (str): URL of the HTTP server
    """
    QR.add_data(data)
    if option == True:
        im = QR.make_image()
        im.show()
    else:
        QR.print_ascii(invert=1)    

# CONST
QR_OPTION = args.qrcode

# HTTP server config
HOST = local_address()
PORT = args.port

# Sharing file config
FILENAME, frameinfo = args.file, getframeinfo(currentframe())
if type(FILENAME) != str:
    raise SystemExit("Ship: line {}: filename argument can only be of type string not {}".format(frameinfo.lineno , type(FILENAME)))

# find mimetype
try:
    MIMETYPE = mimetypes.guess_type(FILENAME)
    TYPE = MIMETYPE[0].split("/")[0]
except BaseException as e:
    _, _, exc_tb = sys.exc_info()
    rep = """please report file type on the github issues page:\nhttps://github.com/yusuf8ahmed/Ship/issues """
    if MIMETYPE == (None, None):
        raise SystemExit("""Ship: line {}: file type is not supported ({}, {})\n{}""".format(exc_tb.tb_lineno, FILENAME, MIMETYPE,rep))
    else:
        raise SystemExit("""Ship: line {}: {} ({}, {})\n{}""".format(exc_tb.tb_lineno, e, FILENAME, MIMETYPE,rep))

# file to be shared to bytes
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
 
def HTTPhandler(*args):
    HTTP_File_Server(FILENAME, FILE, ICO, JS_FILENAME, HOST, PORT, MIMETYPE, *args)
    
def main():
    try:
        myServer = HTTPServer((HOST, PORT), HTTPhandler)
    except OSError as e:
        _, _, exc_tb = sys.exc_info()
        raise SystemExit("Ship: line {}: {}".format(exc_tb.tb_lineno, e))

    print("Make sure to click 'ctrl-c' to kill after usage")
    print("{} Sharing Server Starts {} - http://{}:{}".format(time.asctime(), TYPE, HOST, PORT))
    display_qrcode(QR_OPTION, "http://{}:{}".format(HOST, PORT))
    
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        myServer.server_close()
        raise SystemExit("{} Sharing Server Stop - http://{}:{}".format(time.asctime(), HOST, PORT))
        pass
    myServer.server_close()
    print("{} Sharing Server Stop - http://{}:{}".format(time.asctime(), HOST, PORT))

if __name__ == "__main__":
    main()
