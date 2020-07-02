#!/usr/bin/env python3
# source env/bin/activate

"""entrypoint for console script (function main)
and __main__.py is usually entry when calling from python
'python ship []'
"""
import sys
import multiprocessing as mp 
import traceback
import signal
import threading

__version__ = "0.0.3.0"
if sys.version_info >= (3, 0):
    # Third party package
    import qrcode  # load QR code

    # Standard package
    import os  # os.path operations
    import time  # Logging
    import argparse  # cli
    import logging  # do logs
    import webbrowser # open webbrowser
    
    #local imports
    if str(__package__) == "ship":
        # relative import work only when using pip as __package__ == "ship"
        # very bad solution
        from .httpfileserver import HTTP_File_Server  #get the http request handler class
        from .colors import Colors  # Color for terminal
        from .shiperror import ShipError, ShipPrint, ShipExit  # Ship Template Error and Print Class
        from .funkship import local_address, random_port, display_qrcode
        from .funkship import check_filename, mimetype_and_type, read_file
        from .funkship import read_file_ico, create_server
        from .funkship import command
    else:
        # absolute import only when running locally 
        from httpfileserver import HTTP_File_Server  #get the http request handler class
        from colors import Colors  # Color for terminal
        from shiperror import ShipError, ShipPrint, ShipExit  # Ship Template Error and Print Class
        from funkship import local_address, random_port, display_qrcode
        from funkship import check_filename, mimetype_and_type, read_file
        from funkship import read_file_ico, create_server
        from funkship import command
else:
    raise SystemExit("Ship: Python must be greater that version 3")   

#COMMAND LINE ARGUMENTS
qr_help = "if your phone is having trouble reading qrcode use flag -q:{} ship -q [FILENAME]{}".format(Colors.Green,Colors.Reset)
parser = argparse.ArgumentParser(
    description="""Send file to phone or other computers. Make sure to kill this process after completetion\n{}""".format(qr_help)
    ,formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('file', type=str, nargs='?', help='file to be shared')
parser.add_argument('-p','--port', type=int, default=9999, metavar='port', nargs='?', help='port to be shared on')
parser.add_argument('-l','--local', action='store_true', help='if flagged host address will be localhost/127.0.0.1')
parser.add_argument('-q','--qrcode', action='store_true', help='if flagged qrcode will be in new tab')
#parser.add_argument('-o','--open', action='store_true', help='if flagged browser will open automatically')
parser.add_argument('-v', '--version', action='version', version="Ship {}".format(__version__))
args = parser.parse_args()

#? CONST
# Files 
ICO_FILENAME = os.path.join(os.path.dirname(__file__), "favicon.ico") 
JS_FILENAME = os.path.join(os.path.dirname(__file__), "demo_defer.js")
CSS_FILENAME = os.path.join(os.path.dirname(__file__), "main.css")
# HTTP server config
HOST = "127.0.0.1" if args.local == True else local_address()
PORT = args.port
# File operations
FILENAME = check_filename(args.file)
ABS_FILEPATH = os.path.abspath(args.file)
MIMETYPE, TYPE = mimetype_and_type(FILENAME)
FILE = read_file(FILENAME)
# Favicon operations
ICO = read_file_ico(ICO_FILENAME)
# command 
COMMAND = command(args.file)
# QR code and option
QR = qrcode.QRCode()
QR_OPTION = args.qrcode
# # Webbrowser option
# WB_OPTION = args.open

def HTTP_handler(*args):
    """Description: create HTTP handler with *args given by http.server.HTTPServer
    
    Args(reliant on global scope):
        FILENAME (str): name of file to be shared
        FILE (bytes): the bytes of the file to be shared
        ICO (bytes): the bytes of the favicon
        JS_FILENAME (str): the full path of the js_filename 
        HOST (str): the ip address of host computer
        PORT (int): the sharing port of host computer
        MIMETYPE (str):  the mimetype of the file to be shared  
            
    Args:
        args (list): list of args given by HTTPSever in create_server function
        
    :reliant on global scope
    """
    try:
        HTTP_File_Server(FILENAME, FILE, ICO, JS_FILENAME, HOST, PORT, MIMETYPE, CSS_FILENAME, __version__, *args)
    except BaseException as e:
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{}".format(e), "{} : function HTTP_handler".format(exc_tb.tb_lineno))

def main(): 
    """Ship Executing as standalone script, running from terminal
    
    Args(defined in global scope):
        QR (qrcode.main.QRCode): qrcode object to be used in main function
        QR_OPTION (bool): how to show qr code in line(:False) or new tab(:True) [from argparse]
        HOST (str): host to be runned on [from argparse] 
        PORT (int): port to be runned on [from argparse]
        HTTP_handler (function): a function that return a instance of my Handler class 
        
    :reliant on global scope
    """
    
    qr, qr_option, host, port = QR, QR_OPTION, HOST, PORT
    myServer, port_assigned = create_server(host, port, HTTP_handler)
    url = "http://{}:{}".format(host, port_assigned) 
    print("Make sure to click 'ctrl-c' to kill after usage")
    print("{} Sharing Server Starts - {}".format(time.asctime(), url))
    display_qrcode(qr, qr_option, url)

    try:
        myServer.serve_forever() 
    except KeyboardInterrupt as e: 
        pass
    print("{} Sharing Server Stop - {}".format(time.asctime(), url))
    myServer.server_close() 
        
if "__main__" in __name__ :
    main()
