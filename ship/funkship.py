"""funkship aka shipfunc is a file holding function that are need for the
terminal side(__main__.py) and the import/script(shipapp.py) side of Ship.
all function with this file are not reliant on the global scope of the files.
"""
import sys 

if sys.version_info >= (3, 0):  
    
    # Standard package
    import os
    import re
    import socket  # get local ip address
    import platform  # find platform 
    import mimetypes  # to find mimetype of specific files
    from http.server import HTTPServer  # Basic http server
    from inspect import currentframe, getframeinfo  # Get line number
    from socketserver import ThreadingMixIn
    
    # local imports
    if str(__package__) == "ship":
        # relative import work only when using pip (Or when str(__package__) == "ship")
        # very bad solution
        from .shiperror import ShipError, ShipPrint  # Ship Template Error and Print Class
        from .colors import Colors  # Color for terminal
        #from .__main__ import veblog
    else:
        # absolute import only when running locally 
        from shiperror import ShipError, ShipPrint  # Ship Template Error and Print Class
        from colors import Colors 
        #from __main__ import veblog
else:
    raise SystemExit("Ship: Python must be greater that version 3")

__all__ = [
        "local_address", "random_port", "display_qrcode",
        "check_filename", "mimetype_and_type", "read_file"
        "read_file_ico", "create_server", "killport", "command"]

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

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

def check_port(port):
    """check if port is open

    Args:
        port (int): a port

    Returns:
        conn (bool): if  socket is Open (True) and is opposite (False) 
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex(("127.0.0.1",port))
    if result == 0:
        conn = True
    else:
        conn = False
    s.close()
    return conn
    
def display_qrcode(qr, option, data):
    """
    Description: display qrcode either in terminal or new window
    
    Args:
        option (bool): in line (False) vs new/split tab (True) QR code
        data (str): URL of the HTTP server
    """
    qr.add_data(data)
    if option:
        im = qr.make_image()
        im.show()
    else:
        qr.print_ascii(invert=1) 
        
def check_filename(name, log):
    """
    Description: Check that args.file is a string and assign it to FILENAME

    Args:
        name (str): filename from args.file 

    Raises:
        SystemExit: if type of args.file is not string

    Returns:
        filename_inner (str): filename
    """
    log("checking arg.file".format())
    if os.path.exists(name):
        try:   
            filename_inner, frameinfo = name, getframeinfo(currentframe())
            if type(filename_inner) != str:
                raise ShipError("filename argument can only be of type string not {}".format(type(filename_inner)), frameinfo.lineno)
            else:
                return filename_inner
        except BaseException as e:
            _, _, exc_tb = sys.exc_info()
            raise ShipError("function :{}".format(__name__,e), exc_tb.tb_lineno)
    else:
        raise ShipError("file {} doesn't exist".format(name), "")
    
def mimetype_and_type(filename, log):
    """
    Description: generate MIMETYPE AND TYPE from FILENAME

    Args:
        FILENAME (str): filename
        log (func): 

    Raises:
        ShipError (1): will be raised if any other error happens
        ShipError (2): will be raised if MIMETYPE cannot be found

    Returns:
        (mimetype_inner, type) (tuple): a tuple containing MIMETYPE AND TYPE
    """
    log("checking and getting mimetype of file {}".format(filename))
    try:
        mimetype_inner = mimetypes.guess_type(filename)
        type = mimetype_inner[0].split("/")[0]
        log("mimetype of file {} is {}".format(filename, mimetype_inner))
        return (mimetype_inner, type)
    except BaseException as e:
        log("Error occured in {}".format(__name__), level="error")
        _, _, exc_tb = sys.exc_info()
        rep = """please report file type on the github issues page:\nhttps://github.com/yusuf8ahmed/Ship/issues """
        if mimetype_inner == (None, None):
            raise ShipError("file type is not supported ({}, {})\n{}".format(filename, mimetype_inner, rep), exc_tb.tb_lineno)
        else:
            raise ShipError("{} ({}, {})\n{}".format(e, filename, mimetype_inner, rep), exc_tb.tb_lineno)
        
def read_file(filename, log):
    """
    Description: reading in file (to be shared) in read-binary mode

    Args:
        FILENAME (str): filename

    Raises:
        SystemExit: will be raised if a any error happen
        # most probably will be reading file errors 

    Returns:
        FILE (bytes): a bytes string of the whole file
    """
    log("reading {}".format(filename))
    try:
        with open(filename, "rb") as f: 
            return f.read()
    except BaseException as e:
        log("Error occured in {}".format(__name__), level="error")
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{} : ({})".format(e, filename), "{} : function read_file".format(exc_tb.tb_lineno))
    
def read_file_ico(ico_filename):
    """
    Description: reading in file (.ico) in read-binary mode

    Args:
        ICO_FILENAME (str): .ico filename

    Raises:
        SystemExit: will be raised if any error happen
        # most probably will be reading file errors 

    Returns:
        ICO (bytes): a bytes string of the whole file
    """
    try:
        with open(ico_filename, "rb") as f:
            return f.read()
    except BaseException as e:
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{} : ({})".format(e, ico_filename), "{} : function read_file_ico".format(exc_tb.tb_lineno))
 
 
def check_link(link, log):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, link):
        log("Link is valid {}".format(link))
        return link
    else:
        log("Link is invalid {}".format(link), level="error")
        raise ShipError("Link is invalid {}".format(link), ":function check_link")
        
    
def create_server(host, port, HTTP_handler, forceport=False) -> tuple:
    """
    Description: creates http server

    Args:
        HOST (str): the ip address of host computer
        PORT (int): the sharing port of host computer 
        HTTP_handler (function): this function is used to create a HTTP_File_Server 
        instance with the with *args given by http.server.HTTPServer 

    Raises:
        SystemExit: will be raised if any error happen
    """
    try:
        return ThreadingSimpleServer((host, port), HTTP_handler), port
    except OSError as OSe:
        if (OSe.errno == 48):
            try:
                if forceport == True:
                    return ThreadingSimpleServer((host, port), HTTP_handler), port  
                elif forceport == False:
                    port_reassign = random_port()
                    ShipPrint("Unable to use port {} switching to {}".format(port, port_reassign))
                    ShipPrint("New server one https://{}:{}".format(host, port_reassign))
                    return ThreadingSimpleServer((host, port_reassign), HTTP_handler), port_reassign  
            except BaseException as e:
                _, _, exc_tb = sys.exc_info()
                raise ShipError("{} (forceport error)".format(e), "{}".format(exc_tb.tb_lineno))
        else:
            _, _, exc_tb = sys.exc_info()
            raise ShipError("{} (OsError not 48)".format(OSe), "{}".format(exc_tb.tb_lineno))
    except BaseException as BEe:
        _, _, exc_tb = sys.exc_info()
        raise ShipError("{} (Other Error)".format(BEe), "{}".format(exc_tb.tb_lineno))
        
def command(file):
    if platform.system() == 'Linux':    
        return "ship {}".format(file)
    elif platform.system() == 'Windows':
        return "ship {}".format(file)
    elif platform.system() == 'Darwin':
        return "ship {}".format(file)
    