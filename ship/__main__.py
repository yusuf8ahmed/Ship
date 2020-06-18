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
        
def check_filename(name):
    """
    Description: Check that args.file is a string and assign it to FILENAME

    Args:
        name (str): filename from args.file 

    Raises:
        SystemExit: if type of args.file is not string

    Returns:
        FILENAME_INNER (str): filename
    """
    FILENAME_INNER, frameinfo = name, getframeinfo(currentframe())
    if type(FILENAME_INNER) != str:
        raise SystemExit("Ship: line {}: filename argument can only be of type string not {}".format(frameinfo.lineno , type(FILENAME)))
    else:
        return FILENAME_INNER

def mimetype_and_type(FILENAME):
    """
    Description: generate MIMETYPE AND TYPE from FILENAME

    Args:
        FILENAME (str): filename

    Raises:
        SystemExit: will be rasied if MIMETYPE cannot be found
        SystemExit: will be rasied if any other error happens

    Returns:
        (MIMETYPE, TYPE) (tuple): a tuple containing MIMETYPE AND TYPE
    """    
    
    try:
        MIMETYPE = mimetypes.guess_type(FILENAME)
        TYPE = MIMETYPE[0].split("/")[0]
        return (MIMETYPE, TYPE)
    except BaseException as e:
        _, _, exc_tb = sys.exc_info()
        rep = """please report file type on the github issues page:\nhttps://github.com/yusuf8ahmed/Ship/issues """
        if MIMETYPE == (None, None):
            raise SystemExit("""Ship: line {}: file type is not supported ({}, {})\n{}""".format(exc_tb.tb_lineno, FILENAME, MIMETYPE,rep))
        else:
            raise SystemExit("""Ship: line {}: {} ({}, {})\n{}""".format(exc_tb.tb_lineno, e, FILENAME, MIMETYPE,rep))
       
def read_file(FILENAME):
    """
    Description: reading in file (to be shared) in read-binary mode

    Args:
        FILENAME (str): filename

    Raises:
        SystemExit: will be rasied if a any error happen
        # most probably will be reading file errors 

    Returns:
        FILE (bytes): a bytes string of the whole file
    """
    try:
        with open(FILENAME, "rb") as f: 
            return f.read()
    except BaseException as e:
        raise SystemExit("Ship: {} : ({})".format(e,FILENAME)) 
    
def read_file_ico(ICO_FILENAME):
    """
    Description: reading in file (.ico) in read-binary mode

    Args:
        ICO_FILENAME (str): .ico filename

    Raises:
        SystemExit: will be rasied if a any error happen
        # most probably will be reading file errors 

    Returns:
        ICO (bytes): a bytes string of the whole file
    """
    try:
        with open(ICO_FILENAME, "rb") as f:
            return f.read()
    except BaseException as e:
        raise SystemExit("Ship: {} : ({})".format(e,FILENAME)) 

def HTTP_handler(*args):
    """
    Description: create HTTP handler with *args given by http.server.HTTPServer
    """
    HTTP_File_Server(FILENAME, FILE, ICO, JS_FILENAME, HOST, PORT, MIMETYPE, *args)

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

#? CONST
# Files 
ICO_FILENAME = os.path.join(os.path.dirname(__file__), "favicon.ico") 
JS_FILENAME = os.path.join(os.path.dirname(__file__), "demo_defer.js")
# QRcode
QR = qrcode.QRCode()
# HTTP server config
HOST = local_address()
PORT = args.port
# QR code
QR_OPTION = args.qrcode
# File Properties
FILENAME = check_filename(args.file)
MIMETYPE, TYPE = mimetype_and_type(FILENAME)
FILE = read_file(FILENAME)
ICO = read_file_ico(ICO_FILENAME)

def main():
    try:
        myServer = HTTPServer((HOST, PORT), HTTP_handler)
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
