# Standard package
from http.server import BaseHTTPRequestHandler, HTTPServer # Basic http server

# local imports: HTML templates
if str(__package__) == "ship":
    # relative import work only when using pip (or when str(__package__) == "ship")
    # very bad solution
    from .templates import BASE_TEMPLATE, TEMPLATE_ERROR, FULL_TEMPLATE
    from .templates import TEMPLATE_AUDIO, TEMPLATE_IMAGE, TEMPLATE_TEXT, TEMPLATE_VIDEO
    from .templates import TEMPLATE_PDF
else:
    # absolute import only when running locally 
    from templates import BASE_TEMPLATE, TEMPLATE_ERROR, FULL_TEMPLATE
    from templates import TEMPLATE_AUDIO, TEMPLATE_IMAGE, TEMPLATE_TEXT, TEMPLATE_VIDEO
    from templates import TEMPLATE_PDF

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
                # Section for Special types current PDF as it needs its own viewer
                settings.update({"HOST": self.HOST, "PORT": self.PORT, "VERSION": self.VERSION})
                html = TYPES_SPECIAL.get(settings['MIMETYPE']).format(**settings)
            except BaseException as e:
                # file cannot be opened open a pr
                html = FULL_TEMPLATE.format(**settings)
        return html
        
    def do_GET(self):             
        if self.path == "/{}".format(self.FILENAME):
            self.log_message("Loading {}, {}".format(self.FILENAME, self.MIMETYPE[0]))
            self.send_response(200, "OK")
            self.send_header("Content-Type", self.MIMETYPE[0])
            self.send_header('Content-Length', len(self.FILE))
            self.end_headers()
            self.wfile.write(self.FILE)

        elif self.path == "/main.css":
            self.log_message("Loading main.css")
            with open(self.CSS_FILENAME, "rb") as f:
                CSS = f.read()
            self.send_response(200, "OK")
            self.send_header("Content-Type", "text/css")
            self.send_header('Content-Length', len(CSS))
            self.end_headers()
            self.wfile.write(CSS)

        elif self.path == "/favicon.ico":
            self.log_message("Loading favicon")
            self.send_response(200, "OK")
            self.send_header("Content-Type", "image/x-icon")
            self.send_header('Content-Length', len(self.ICO))
            self.end_headers()
            self.wfile.write(self.ICO)

        elif self.path == "/demo_defer.js":
            self.log_message("Loading pdfjs")
            with open(self.JS_FILENAME, "rb") as f:
                JS = f.read()
            self.send_response(200, "OK")
            self.send_header("Content-Type", "text/javascript")
            self.send_header('Content-Length', len(JS))
            self.end_headers()
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
            self.send_response(200, "OK")
            self.send_header("Content-type", "text/html")
            self.send_header('Content-Length', len(res.encode('utf-8')))
            self.end_headers()
            self.wfile.write(res.encode())

        else:
            self.log_message("Loading in error")
            res = self.get_response(
                "error",
                {
                    "HOST":self.HOST,
                    "PORT":self.PORT,
                    "MESSAGE":"This is an illegal route"
                }
                )
            self.send_response(404, "Not Found")
            self.send_header("Content-type", "text/html")
            self.send_header('Content-Length', len(res.encode('utf-8')))
            self.end_headers()
            self.wfile.write(res.encode())
            
    def do_POST(self):
        self.log_message("HTTP POST method is not allowed")