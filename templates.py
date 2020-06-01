

BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>Ship</title>
        <link rel="shortcut icon" href="/files/favicon.ico" type="image/x-icon">
        <style>
        </style>
    </head>
    <body>
        <p style="">Testing: Basically giphy on crack but only served localy</p>
        <div style="top: 0;bottom: 0;left: 0;right: 0;">
        {TEMPLATE}        
        <div>
    </body>
</html>
"""

# TEMPLATE_APPLICATION = """
# <div>
#     <a href="{FILENAME}" download>
#         <object data="http://{HOST}:{PORT}/{FILENAME}" type="{MIMETYPE}" width="750px" height="750px">
#             <embed src="http://{HOST}:{PORT}/{FILENAME}" type="{MIMETYPE}">
#                 <p>This browser does not support {MIMETYPE}</p>
#             </embed>
#         </object>
#         <p>download</p>
#     </a>
# </div>
# """

TEMPLATE_AUDIO = """
<div>
    <audio controls>
        <source src="{FILENAME}" type="{MIMETYPE}">
        Your browser does not support the audio element.
    </audio>
    <p>Filename: {FILENAME}</p>
    <a href="{FILENAME}" style="text-decoration: none;" download>
        <p style="text-decoration: none;">download</p>
    </a>
</div>
"""
TEMPLATE_IMAGE = """
<div >
    <img src="{FILENAME}" alt="document" style="height:500px; width:auto;">
    <div style="height:500px; width:auto;">
        <p>Filename: {FILENAME}</p>
        <a href="{FILENAME}" style="text-decoration: none; color: black; float: right;" download>
            <p style="text-decoration: none;">download</p>
        </a>    
    </div>
</div>
"""
TEMPLATE_TEXT = """
<div>
    <embed src="{FILENAME}">
    <p>Filename: {FILENAME}</p>
    <a href="{FILENAME}" style="text-decoration: none;" download>
        <p style="text-decoration: none;">download</p>
    </a>
</div
"""
TEMPLATE_VIDEO = """
<div>
    <video width="320" height="500" src="{FILENAME}" autoplay preload controls>
        Your browser does not support the video tag.
    </video>
    <p>Filename: {FILENAME}</p>
    <a href="{FILENAME}" style="text-decoration: none;" download>
        <p>download</p>
    </a>
</div
"""
TEMPLATE_ERROR = """
<div>
    <p>{MESSAGE}</p>
    <a href="http://{HOST}:{PORT}">Return to home</a><br>
</div
"""
TEMPLATE_PDF = """
<!DOCTYPE html>
<html>
    <head>
        <title>Ship</title>
        <link rel="shortcut icon" href="/files/favicon.ico" type="image/x-icon">
        <script src="https://mozilla.github.io/pdf.js/build/pdf.js"></script>        
    </head>
    <body>
        <p>Testing: Basically giphy on crack but only served localy</p>
        <div style="top: 0;bottom: 0;left: 0;right: 0;">
            <div>
                <button id="prev">Previous</button>
                <button id="next">Next</button>
                &nbsp; &nbsp;
                <span>Page: <span id="page_num"></span> / <span id="page_count"></span></span>
                <a href="{FILENAME}" style="text-decoration: none;" download>
                    <p>download</p>
                </a>
            </div>
            <canvas id="the-canvas" style="border: 1px solid black; direction: ltr;"></canvas>
        </div>
        <script>
            var url = 'http://{HOST}:{PORT}/{FILENAME}';
        </script>
        <script src="demo_defer.js" defer></script>
    </body>
</html>
"""

FULL_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>Ship</title>
        <link rel="shortcut icon" href="/files/favicon.ico" type="image/x-icon">
    </head>
    <body>
        <p style="">Basically giphy on crack but only served localy</p>
        <p style="">file cannot be view but will download</p>
        <a href="{FILENAME}"  style="text-decoration: none;" download>
            <p>download</p>
        </a>
    </body>
</html>
"""
__all__ = [BASE_TEMPLATE, TEMPLATE_AUDIO, TEMPLATE_IMAGE, TEMPLATE_TEXT, TEMPLATE_VIDEO, TEMPLATE_ERROR, TEMPLATE_PDF, FULL_TEMPLATE ]
