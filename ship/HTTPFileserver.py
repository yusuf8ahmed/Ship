# Standard package
from http.server import BaseHTTPRequestHandler, HTTPServer # Basic http server

# local imports: HTML templates
if str(__package__) == "ship":
    # relative import work only when using pip (or when str(__package__) == "ship")
    # very bad solution
    from .templates import BASE_TEMPLATE, TEMPLATE_ERROR, UNVIEWABLE_TEMPLATE
    from .templates import TEMPLATE_AUDIO, TEMPLATE_IMAGE, TEMPLATE_TEXT, TEMPLATE_VIDEO
    from .templates import TEMPLATE_PDF
    from .templates import TEMPLATE_URL
else:
    # absolute import only when running locally 
    from templates import BASE_TEMPLATE, TEMPLATE_ERROR, UNVIEWABLE_TEMPLATE
    from templates import TEMPLATE_AUDIO, TEMPLATE_IMAGE, TEMPLATE_TEXT, TEMPLATE_VIDEO
    from templates import TEMPLATE_PDF
    from templates import TEMPLATE_URL

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

class HTTP_File_Server(BaseHTTPRequestHandler):
    
    def __init__(self, filename, file, ico, js_filename, host, port, mimetype, css_filename, version, *args):
        self.FILENAME = filename
        self.FILE = file
        self.ICO = ico
        self.JS_FILENAME = js_filename
        self.HOST = host
        self.PORT = port
        self.MIMETYPE = mimetype
        self.CSS_FILENAME = css_filename
        self.VERSION = version
        BaseHTTPRequestHandler.__init__(self, *args)
        
    def get_response(self, name, settings):
        """Description: this function develops the html response
        and insert useful info by use the in inbuilt function ".format()"

        Args:
            name (str): the string repersenation of associated mimetype type ([type]/subtype) 
            settings (dict): a dictionary that holds values that are need in the html

        Returns:
            html (str): the final html with all info inside
        """
        try:
            html = BASE_TEMPLATE.format(
                    **{
                        "TEMPLATE":TYPES.get(name).format(**settings),
                        "HOST":self.HOST,
                        "PORT":self.PORT,
                        "VERSION": self.VERSION
                    }
                )
        except BaseException as e:
            try:
                # Section for special types as not all application mimetype use the same html/viewer
                settings.update({"HOST": self.HOST, "PORT": self.PORT, "VERSION": self.VERSION})
                html = TYPES_SPECIAL.get(settings['MIMETYPE']).format(**settings)
            except BaseException as e:
                # file cannot be opened open a pr
                html = UNVIEWABLE_TEMPLATE.format(**settings)
        return html
    
    def _set_response(self, code, type, length):
        self.send_response(code)
        self.send_header('Content-type', type)
        self.send_header('Content-Length', length)
        self.end_headers()
        
    def do_GET(self):             
        if self.path == "/{}".format(self.FILENAME):
            self.log_message("Loading {}, {}".format(self.FILENAME, self.MIMETYPE[0]))
            self._set_response(200, self.MIMETYPE[0], len(self.FILE))
            self.wfile.write(self.FILE)

        elif self.path == "/main.css":
            self.log_message("Loading main.css")
            with open(self.CSS_FILENAME, "rb") as f:
                CSS = f.read()
            self._set_response(200, "text/css", len(CSS))
            self.wfile.write(CSS)

        elif self.path == "/favicon.ico":
            self.log_message("Loading favicon")
            self._set_response(200, "image/x-icon", len(self.ICO))
            self.wfile.write(self.ICO)

        elif self.path == "/demo_defer.js":
            self.log_message("Loading pdfjs")
            with open(self.JS_FILENAME, "rb") as f:
                JS = f.read()
            self._set_response(200, "text/javascript", len(JS))
            self.wfile.write(JS)

        elif self.path == "/":
            self.log_message("Loading in main")
            res = self.get_response(
                self.MIMETYPE[0].split("/")[0],
                {
                    "FILENAME":self.FILENAME,
                    "MIMETYPE":self.MIMETYPE[0],
                    "HOST":self.HOST,
                    "PORT":self.PORT,
                    "VERSION": self.VERSION
                }
                )
            self._set_response(200, "text/html", len(res.encode('utf-8')))
            self.wfile.write(res.encode())

        else:
            self.log_message("Loading in error")
            res = self.get_response(
                "error",
                {
                    "HOST":self.HOST,
                    "PORT":self.PORT,
                    "VERSION": self.VERSION,
                    "MESSAGE":"This is an illegal route"
                }
                )
            self._set_response(404, "text/html", len(res.encode('utf-8')))
            self.wfile.write(res.encode())
            
    def do_POST(self):
        self.log_message("Ship: POST request are not allowed ({})".format(self.path).encode('utf-8'))
        
class HTTP_URL_Server(BaseHTTPRequestHandler):
    
    def __init__(self, link, ico, css_filename, version, log, *args):
        self.LINK = link
        self.ICO = ico
        self.CSS_FILENAME = css_filename
        self.VERSION = version
        self.log = log
        BaseHTTPRequestHandler.__init__(self, *args)
        
    def get_response(self, name, settings):
        """Description: this function develops the html response
        and insert useful info by use the in inbuilt function ".format()"

        Args:
            settings (dict): a dictionary that holds values that are need in the html

        Returns:
            html (str): the final html with all info inside
        """
        try:
            if name == "link":
                html = TEMPLATE_URL.format(**settings)
            else:
                html = BASE_TEMPLATE.format(
                        **{
                            "TEMPLATE":TYPES.get(name).format(**settings),
                            "VERSION": self.VERSION
                        }
                    )
            return html
        except BaseException as e:
            print("{}".format(e))
        
    def _set_response(self, code, type, length):
        self.send_response(code)
        self.send_header('Content-type', type)
        self.send_header('Content-Length', length)
        self.end_headers()
    
    def respond(self, res):
        self.wfile.write(res.encode())
        
    def route_main(self):
        self.log("Loading main route")
        res = self.get_response(
            "link",
            {
                "LINK":self.LINK,
                "VERSION": self.VERSION
            }
        )
        self._set_response(200, "text/html", len(res.encode('utf-8')))
        self.respond(res)
    
    def route_css(self):
        self.log("Loading main.css")
        with open(self.CSS_FILENAME, "rb") as f:
            CSS = f.read()
        self._set_response(200, "text/css", len(CSS))
        self.wfile.write(CSS)
    
    def route_favicon(self):
        self.log("Loading favicon")
        self._set_response(200, "image/x-icon", len(self.ICO))
        self.wfile.write(self.ICO)
    
    def route_error(self, message):
        self.log("Loading in error")
        res = self.get_response(
            "error",
            {
                "MESSAGE": message,
                "VERSION": self.VERSION
            }
        )
        self._set_response(404, "text/html", len(res.encode('utf-8')))
        self.respond(res)

    def do_GET(self):
        # cooked version of switch case statement 
        try: 
            self.log("calling route {}".format(self.path))
            case = {
                "/" : self.route_main,
                "/main.css" : self.route_css,
                "/favicon.ico" : self.route_favicon,
                }
            case[self.path]()
        except BaseException as e:
            self.log("{}".format(e))
            self.route_error("This is a illegal route") 
            
    def do_POST(self):
        self.log("Ship: POST request are not allowed ({})".format(self.path).encode('utf-8'))
        self.log_message("Ship: POST request are not allowed ({})".format(self.path).encode('utf-8'))

        