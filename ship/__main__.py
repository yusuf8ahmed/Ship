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
    from pyngrok import ngrok # ngrok for tunnel to localhost
    from pyngrok.ngrok import PyngrokConfig
    from loguru import logger # bruh logging

    # Standard package
    import os  # os.path operations
    import time  # Logging
    import argparse  # cli
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
else:
    raise SystemExit("Ship: Python must be greater that version 3")   

#COMMAND LINE ARGUMENTS
qr_help = "if your phone is having trouble reading qrcode use flag -q:{} ship -q [FILENAME]{}".format(Colors.Green,Colors.Reset)
desc = """Send file to phone or other computers. Make sure to kill this process after completetion\n{}""".format(qr_help)
parser = argparse.ArgumentParser(prog="ship", description=desc, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('main', type=str, nargs='?', help='file to be shared')
parser.add_argument('-p','--port', type=int, default=9999, metavar='port', nargs='?', help='port to be shared on')
parser.add_argument('-q','--qrcode', action='store_true', help='if flagged qrcode will be in new tab')
parser.add_argument('-o','--open', action='store_true', help='if flagged browser will open automatically')
parser.add_argument('-P','--private', action='store_true', help='if flagged host address will be on private ip')
parser.add_argument('-L','--localhost', action='store_true', help='if flagged host address will be localhost')
parser.add_argument('-l','--link', action='store_true', help='if flagged ship will start the Link Sharing Server')
parser.add_argument('-V', '--verbose', action='store_true', help='if flagged additional details will be shown via stdout')
parser.add_argument('-v', '--version', action='version', version="Ship {}".format(__version__))
args = parser.parse_args()
              
#? CONST
# Files 
ICO_FILENAME = os.path.join(os.path.dirname(__file__), "favicon.ico") 
JS_FILENAME = os.path.join(os.path.dirname(__file__), "demo_defer.js")
CSS_FILENAME = os.path.join(os.path.dirname(__file__), "main.css")
# Command representation
COMMAND = " ".join(sys.argv)
# Verbose option
VEB_OPTION = args.verbose
if VEB_OPTION:
    pass
else:
    class logger:
        def debug(*args, **kwargs):
            pass
# QR code and option
QR = qrcode.QRCode()
QR_OPTION = args.qrcode
# link option
LINK_OPTION = args.link
# Webbrowser option
WB_OPTION = args.open
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
logger.debug(f"main: {MAIN}")
if MAIN is None:
    logger.debug(f"main cannot be NoneType :{MAIN}")
    ShipExit("main argument cannot be empty")
    
# Favicon operations
ICO = read_file_ico(ICO_FILENAME)
if LINK_OPTION:
    logger.debug("Ship sharing link")
    LINK = check_link(MAIN, logger.debug)
else:
    logger.debug("Ship sharing file")
    FILENAME = check_filename(MAIN, logger.debug)
    ABS_FILEPATH = os.path.abspath(FILENAME)
    logger.debug("FILEPATH:{}".format(ABS_FILEPATH))
    MIMETYPE, TYPE = mimetype_and_type(FILENAME, logger.debug)
    FILE = read_file(FILENAME, logger.debug)
   
logger.debug("argparse line: {}".format(args)) 


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
            HTTP_URL_Server(LINK, ICO, CSS_FILENAME, __version__, logger.debug, *args)
        else:
            #File Server route method is based switch case method
            HTTP_File_Server(FILENAME, FILE, ICO, JS_FILENAME, HOST, PORT, MIMETYPE, CSS_FILENAME, __version__, *args)
    except BaseException as e:
        logger.debug("error when creating server", level="error")
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{}".format(e), "{} : function HTTP_handler".format(exc_tb.tb_lineno))
  
def hosting(host, port):
    if LOCAL == False and PRIVATE == False:
        logger.debug("Running on ngork") 
        url = ngrok.connect(port)
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
    logger.debug("Created HTTP server") 
    url = hosting(host, port_assigned)
    print("Make sure to click 'ctrl-c' to kill after usage")
    print("{} Sharing Server Starts - {}".format(time.asctime(), url))
    logger.debug("displaying qrcode")
    display_qrcode(qr, qr_option, url)
    
    server_thread = threading.Thread(target=myServer.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.debug("Server loop running in thread: {}".format(server_thread.name))
    
    if WB_OPTION:
        webbrowser.open(url=url)
    
    def handler(x, y):
        logger.debug("stopping HTTP server")
        print("{} Sharing Server Stop - {}".format(time.asctime(), url))        
        myServer.shutdown()
        myServer.server_close() 
        sys.exit(0)
        
    signal.signal(signal.SIGINT, handler)
        
    while True:
        #HTTP server loop
        try:
            pass
        except KeyboardInterrupt: 
            break

if "__main__" in __name__ :
    logger.debug("__file__={}|__name__={}|__package__={}".format(__file__ ,__name__,__package__)) 
    logger.debug("Command line: {}".format(COMMAND)) 
    logger.debug("{}".format(MAIN)) 
    main()
