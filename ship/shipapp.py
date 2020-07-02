#!/usr/bin/env python3
"""use ship without the command line interface
"""

# source env/bin/activate
import sys 

if sys.version_info >= (3, 0):  
    # Third party package
    import qrcode  # load QR code

    # Standard package
    import os  # os.path operations
    import time  # Logging
    import socket  # get local ip address
    import logging  # do logs
    import multiprocessing as mp
    import threading
        
    # local imports
    if str(__package__) == "ship":
        # relative import work only when using pip (Or when str(__package__) == "ship")
        # very bad solution
        from .httpfileserver import HTTP_File_Server  #get the http request handler class
        from .shiperror import ShipError, ShipPrint,ShipExit  # Ship Template Error and Print Class
        from .funkship import local_address, random_port, display_qrcode
        from .funkship import check_filename, mimetype_and_type, read_file
        from .funkship import read_file_ico, create_server
    else:
        # absolute import only when running locally 
        from httpfileserver import HTTP_File_Server  #get the http request handler class
        from shiperror import ShipError, ShipPrint, ShipExit # Ship Template Error and Print Class
        from funkship import local_address, random_port, display_qrcode
        from funkship import check_filename, mimetype_and_type, read_file
        from funkship import read_file_ico, create_server
else:
    raise SystemExit("Ship: Python must be greater that version 3")   

def ShipIt(filename, argport=9999, auto_open=False, qr_option=False, qr_display=False): 
    """Description: (This is unstable) Start ship without the command line interface 
    may require admin power or user password
    
    Args:
        filename (str): file to be shared
        argport (int): port to be shared on
        auto_open (bool): should the website appear automatically, yes (True), no (False) 
        qr_display (bool): should the qr appear, yes (True), no (False) 
        qr_option (bool): how to show qr code, in line(False) or new tab(True)

    Raises:
        ShipError: SystemExit clone with template
        
    """
    #enclosing variables
    ico_filename = os.path.join(os.path.dirname(__file__), "favicon.ico") 
    js_filename = os.path.join(os.path.dirname(__file__), "demo_defer.js")
    qr = qrcode.QRCode()
    host = local_address()
    port = argport
    abs_filepath = os.path.abspath(filename)
    filename_inner = check_filename(abs_filepath)
    file_inner = read_file(filename_inner)
    mimetype_inner, _ = mimetype_and_type(filename_inner)
    ico = read_file_ico(ico_filename)
    
    def HTTP_handler(*args):
        """
        Description: create HTTP handler with *args given by http.server.HTTPServer
        :reliant on enclosing scope
        """
        try:
            return HTTP_File_Server(filename, file_inner, ico, js_filename, host, port, mimetype_inner, *args)
        except BaseException as e:
            _, _, exc_tb = sys.exc_info()
            raise ShipError("{}".format(e), "{} : function HTTP_handler".format(exc_tb.tb_lineno)) 
    
    myServer, port_assigned = create_server(host, port, HTTP_handler)
    url = "http://{}:{}".format(host, port_assigned)
    
    if qr_display: 
        display_qrcode(qr, qr_option, url)

    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        pid = os.fork()
        if pid == 0:
            # We are in the child process.
            return (host, port_assigned, url)
        else:
            # We are in the parent process.
            try:
                myServer.serve_forever()
            except BaseException as e:
                pass
    elif sys.platform == "win32":
        def sleeper(m):
            sys.stdout.flush()
            m.serve_forever()

        p = mp.Process(target=sleeper, args=(myServer,))
        p.start()
        return host, port_assigned, url
        

# thread = threading.Thread(target=myServer.serve_forever)
# thread.setDaemon = True
# try:
#     thread.start()
#     if auto_open:
#         webbrowser.open(url, new=2, autoraise=True)
# except KeyboardInterrupt:
#     myServer.shutdown()
#     sys.exit(0)
# return host, port_assigned, url

# #? replica of os.fork 
# #? can run be gives some werid multiprocessing error if stopped
# def child(server):
#     try:
#         server.serve_forever() 
#     except BaseException as e:
#         server.server_close() 
        
# try:
#     p = mp.Process(target=child, args=(myServer,)).start()
# except:
#     myServer.server_close() 

# return host, port_assigned, url
