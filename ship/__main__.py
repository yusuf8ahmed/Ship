#!/usr/bin/env python3
#source env/bin/activate

# version
__version__ = "0.0.2.0"
import sys # 

if sys.version_info >= (3, 0):
    # Third party package
    import qrcode #load qrcode

    # Standard package
    import os # os.path operations
    import time # Logging
    import socket # get local ip address
    import argparse # cli
    import mimetypes # to find mimetype of specific files
    from http.server import BaseHTTPRequestHandler, HTTPServer # Basic http server
    from inspect import currentframe, getframeinfo # Get line number

    # Local Import 
    from .HTTPFileserver import HTTP_File_Server
    # Color for terminal
    from .colors import Colors
    # Ship Error for terminal
    from .ShipError import ShipError
else:
    raise SystemExit("Ship: Python must be greater that version 3")

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

def display_qrcode(QR, option, data):
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
        raise ShipError("filename argument can only be of type string not {}".format(type(FILENAME)),frameinfo.lineno)
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
            raise ShipError("file type is not supported ({}, {})\n{}".format(FILENAME, MIMETYPE, rep), exc_tb.tb_lineno)
        else:
            raise ShipError("{} ({}, {})\n{}".format(e, FILENAME, MIMETYPE, rep), exc_tb.tb_lineno)
       
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
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{} : ({})".format(e, FILENAME), "{} : function read_file".format(exc_tb.tb_lineno))
    
def read_file_ico(ICO_FILENAME):
    """
    Description: reading in file (.ico) in read-binary mode

    Args:
        ICO_FILENAME (str): .ico filename

    Raises:
        SystemExit: will be rasied if any error happen
        # most probably will be reading file errors 

    Returns:
        ICO (bytes): a bytes string of the whole file
    """
    try:
        with open(ICO_FILENAME, "rb") as f:
            return f.read()
    except BaseException as e:
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{} : ({})".format(e, ICO_FILENAME), "{} : function read_file_ico".format(exc_tb.tb_lineno))

def HTTP_handler(*args):
    """
    Description: create HTTP handler with *args given by http.server.HTTPServer
    """
    try:
        HTTP_File_Server(FILENAME, FILE, ICO, JS_FILENAME, HOST, PORT, MIMETYPE, *args)
    except BaseException as e:
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{}".format(e), "{} : function HTTP_handler".format(exc_tb.tb_lineno))

def create_server(HOST, PORT, HTTP_handler):
    """creates http server

    Args:
        HOST (str): ip address of host computer
        PORT (int): the sharing port of host computer 
        HTTP_handler (function): this function is used to create a HTTP_File_Server 
        instance with the with *args given by http.server.HTTPServer 

    Raises:
        SystemExit: will be rasied if any error happen
    """
    try:
        return HTTPServer((HOST, PORT), HTTP_handler)
    except OSError as e:
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{}".format(e), exc_tb.tb_lineno)

#COMMAND LINE ARGUMENTS
qr_help = "if your phone is having trouble reading QRcode use flag -q:{} ship -q [FILENAME]{}".format(Colors.Green,Colors.Reset)
parser = argparse.ArgumentParser(
    description="""Send file to phone or other computers. Make sure to kill this process after completetion\n{}""".format(qr_help)
    , formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('file', type=str, nargs='?', help='file to be shared')
parser.add_argument('-p','--port', type=int, default=9999, metavar='port', nargs='?', help='port to be shared one')
parser.add_argument('-q','--qrcode', action='store_true', help='if flagged qrcode will be in new tab')
parser.add_argument('-V', '--version', action='version', version="Ship {}".format(__version__))
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
    myServer = create_server(HOST, PORT, HTTP_handler)
    print("Make sure to click 'ctrl-c' to kill after usage")
    print("{} Sharing Server Starts {} - http://{}:{}".format(time.asctime(), TYPE, HOST, PORT))
    display_qrcode(QR, QR_OPTION, "http://{}:{}".format(HOST, PORT))
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass
    myServer.server_close()
    print("{} Sharing Server Stop - http://{}:{}".format(time.asctime(), HOST, PORT))

if __name__ == "__main__":
    main()
