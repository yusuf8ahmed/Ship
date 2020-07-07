#!/usr/bin/env python3
# source env/bin/activate

"""entrypoint for console script (function main)
and __main__.py is usually entry when calling from python
'python ship []'
"""

from os import terminal_size
import sys
import multiprocessing as mp 
import traceback
import signal
import threading

__version__ = "0.0.3.0"
if sys.version_info >= (3, 0):
    # Third party package
    import qrcode  # load QR code
    from pyngrok import ngrok #ngrok for tunnel to localhost
    from pyngrok.ngrok import PyngrokConfig

    # Standard package
    import os  # os.path operations
    import time  # Logging
    import argparse  # cli
    #import logging  # do logs
    import webbrowser # open webbrowser
    
    #local imports
    if str(__package__) == "ship":
        # relative import work only when using pip as __package__ == "ship"
        # very bad solution
        from .httpfileserver import HTTP_File_Server  #get the http request handler class
        from .httpfileserver import HTTP_URL_Server  #get the http request handler class
        from .colors import Colors  # Color for terminal
        from .shiperror import ShipError, ShipPrint, ShipExit  # Ship Template Error and Print Class
        from .funkship import local_address, random_port, display_qrcode
        from .funkship import check_filename, mimetype_and_type, read_file
        from .funkship import read_file_ico, create_server,check_link
        from .funkship import command
    else:
        # absolute import only when running locally 
        from httpfileserver import HTTP_File_Server  #get the http request handler class
        from httpfileserver import HTTP_URL_Server  #get the http request handler class
        from colors import Colors  # Color for terminal
        from shiperror import ShipError, ShipPrint, ShipExit  # Ship Template Error and Print Class
        from funkship import local_address, random_port, display_qrcode
        from funkship import check_filename, mimetype_and_type, read_file
        from funkship import read_file_ico, create_server, check_link
        from funkship import command
    #Global config
    #logging.basicConfig(level=logging.DEBUG,format="%(levelname)s:PID-%(process)d:%(message)s")
else:
    raise SystemExit("Ship: Python must be greater that version 3")   

#COMMAND LINE ARGUMENTS
qr_help = "if your phone is having trouble reading qrcode use flag -q:{} ship -q [FILENAME]{}".format(Colors.Green,Colors.Reset)
desc = """Send file to phone or other computers. Make sure to kill this process after completetion\n{}""".format(qr_help)
parser = argparse.ArgumentParser(prog="ship", description=desc, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('main', type=str, nargs='?', help='file to be shared')
parser.add_argument('-p','--port', type=int, default=9999, metavar='port', nargs='?', help='port to be shared on')
parser.add_argument('-q','--qrcode', action='store_true', help='if flagged qrcode will be in new tab')
#parser.add_argument('-o','--open', action='store_true', help='if flagged browser will open automatically')
parser.add_argument('-P','--private', action='store_true', help='if flagged host address will be on private ip')
parser.add_argument('-L','--localhost', action='store_true', help='if flagged host address will be localhost')
parser.add_argument('-l','--link', action='store_true', help='if flagged ship will start the Link Sharing Server')
parser.add_argument('-V', '--verbose', action='store_true', help='if flagged additional details will be shown via stdout')
parser.add_argument('-v', '--version', action='version', version="Ship {}".format(__version__))
args = parser.parse_args()

def veb_log(*args, level="debug"):
    """Description: veb_log or verbose logger is use when verbose 
    flag is flagged
    :RELIANT ON GLOBAL SCOPE
    
    Args(reliant on global scope):
        VEB_OPTION (bool): verbose flag option (True) or (False)

    Args:
        level (str, optional): level of debugging. Defaults to "debug".
        *args, **kwargs: passed to logging.[level]
    """
    if VEB_OPTION:
        if level == "debug":
            print("DEBUG: {}".format(*args))
            #logging.debug(*args)
        elif level == "info":
            print("INFO: {}".format(*args))
            #logging.info(*args)
        elif level == "warning":
            print("WARNING: {}".format(*args))
            #logging.warning(*args)
        elif level == "error":
            print("ERROR: {}".format(*args))
            #logging.error(*args)
        elif level == "critical":
            print("CRITICAL: {}".format(*args))
            #logging.critical(*args)
          
#? CONST
# Files 
ICO_FILENAME = os.path.join(os.path.dirname(__file__), "favicon.ico") 
JS_FILENAME = os.path.join(os.path.dirname(__file__), "demo_defer.js")
CSS_FILENAME = os.path.join(os.path.dirname(__file__), "main.css")
# Command representation
COMMAND = " ".join(sys.argv)
# Verbose option
VEB_OPTION = args.verbose
# QR code and option
QR = qrcode.QRCode()
QR_OPTION = args.qrcode
# link option
LINK_OPTION = args.link
# Webbrowser option
# WB_OPTION = args.open
# HTTP server config
PORT = args.port
HOST = "127.0.0.1" # ngrok
LOCAL, PRIVATE = False, False
if args.localhost == True:
    LOCAL = True
    HOST = "127.0.0.1" # localhost
elif args.private == True:
    PRIVATE = True
    HOST = local_address() # private ip
# File operations
MAIN = args.main
# Favicon operations
ICO = read_file_ico(ICO_FILENAME)
if LINK_OPTION:
    veb_log("Ship sharing link", level="debug")
    LINK = check_link(MAIN, veb_log)
else:
    veb_log("Ship sharing file", level="debug")
    FILENAME = check_filename(MAIN, veb_log)
    ABS_FILEPATH = os.path.abspath(FILENAME)
    veb_log("FILEPATH:{}".format(ABS_FILEPATH), level="debug")
    MIMETYPE, TYPE = mimetype_and_type(FILENAME, veb_log)
    FILE = read_file(FILENAME, veb_log)
   
veb_log("argparse line: {}".format(args), level="debug") 

def HTTP_handler(*args):
    """Description: create HTTP handler with *args given by http.server.HTTPServer
    :RELIANT ON GLOBAL SCOPE
    
    Args(reliant on global scope):
        FILENAME (str): name of file to be shared
        FILE (bytes): the bytes of the file to be shared
        ICO (bytes): the bytes of the favicon
        JS_FILENAME (str): the full path of the js_filename 
        HOST (str): the ip address of host computer
        PORT (int): the sharing port of host computer
        MIMETYPE (str):  the mimetype of the file to be shared  
        CSS_FILENAME (str): the full path of the css_filename 
        __version__ (str): version of ship
            
    Args:
        args (list): list of args given by HTTPSever in create_server function
    """
    try:
        if LINK_OPTION:
            #URL Server route method is based switch case method
            HTTP_URL_Server(LINK, ICO, CSS_FILENAME, __version__, veb_log, *args)
        else:
            #File Server route method is based switch case method
            HTTP_File_Server(FILENAME, FILE, ICO, JS_FILENAME, HOST, PORT, MIMETYPE, CSS_FILENAME, __version__, *args)
    except BaseException as e:
        veb_log("error when creating server", level="error")
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{}".format(e), "{} : function HTTP_handler".format(exc_tb.tb_lineno))
  
def log_event_callback(log):
    pass
    
def hosting(host, port):
    if LOCAL == False and PRIVATE == False:
        veb_log("Running on ngork".format(args), level="debug") 
        pyngrok_config = PyngrokConfig(log_event_callback=log_event_callback)
        url = ngrok.connect(port, pyngrok_config=pyngrok_config)
    else:
        url = "http://{}:{}".format(host, port)
    return url

def main(): 
    """Ship executing as standalone script, running from terminal
    :RELIANT ON GLOBAL SCOPE
    
    Args(defined in global scope):
        QR (qrcode.main.QRCode): qrcode object to be used in main function
        QR_OPTION (bool): how to show qr code in line(False) or new tab(True) [from argparse]
        HOST (str): host to be runned on [from argparse] 
        PORT (int): port to be runned on [from argparse]
        HTTP_handler (function): a function that return a instance of my handler class 
    """
    qr, qr_option, host, port = QR, QR_OPTION, HOST, PORT
    myServer, port_assigned = create_server(host, port, HTTP_handler)
    veb_log("Created HTTP server", level="debug") 
    url = hosting(host, port_assigned)
    print("Make sure to click 'ctrl-c' to kill after usage")
    print("{} Sharing Server Starts - {}".format(time.asctime(), url))
    veb_log("displaying qrcode", level="debug")
    display_qrcode(qr, qr_option, url)

    try:
        myServer.serve_forever() 
    except KeyboardInterrupt as e: 
        pass
    veb_log("stopping HTTP server", level="debug")
    print("{} Sharing Server Stop - {}".format(time.asctime(), url))
    myServer.server_close() 
      
if "__main__" in __name__ :
    veb_log("__file__={}|__name__={}|__package__={}".format(__file__ ,__name__,__package__), level="debug") 
    veb_log("Command line: {}".format(COMMAND), level="debug") 
    veb_log("{}".format(MAIN), level="debug") 
    main()
