BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>Page Title</title>
        <link rel="shortcut icon" href="/files/favicon.ico" type="image/x-icon">
    </head>
    <body>
        <p style="">Testing: Basically giphy on crack but only served localy</p>
        {TEMPLATE}
    </body>
</html>
"""
TEMPLATE_APPLICATION = """
<div style="display:flex; justify-content:center;">
    <a href="{FILENAME}" download>
        <object data="http://{HOST}:{PORT}/{FILENAME}" type="{MIMETYPE}" width="750px" height="750px">
            <embed src="http://{HOST}:{PORT}/{FILENAME}" type="{MIMETYPE}">
                <p>This browser does not support {MIMETYPE}</p>
            </embed>
        </object>
        <p style="margin-top: 3;">Click this to download and wait two seconds</p>
    </a>
</div>

"""
TEMPLATE_AUDIO = """
<div style="display:flex; justify-content:center;">
    <a href="{FILENAME}" download>
        <audio controls>
            <source src="{FILENAME}" type="{MIMETYPE}">
            Your browser does not support the audio element.
        </audio>
        <p style="margin-top: 3;">Click this to download and wait two seconds</p>
    </a>
</div>
"""
TEMPLATE_IMAGE = """
<p>Filename: {FILENAME}</p>
<div style="display:flex; justify-content:center;">
    <a href="{FILENAME}" download>
        <img src="{FILENAME}" alt="document" style="height:500px; width:auto;">
        <p style="margin-top: 3;">Click this to download and wait two seconds</p>
    </a>
</div>
"""
TEMPLATE_TEXT = """
<p>Filename: {FILENAME}</p>
<div style="display:flex; justify-content:center;">
    <a href="{FILENAME}" download>
        <embed src="{FILENAME}">
        <p style="margin-top: 3;">Click this to download and wait two seconds</p>
    </a>
</div
"""
TEMPLATE_VIDEO = """
<p>Filename: {FILENAME}</p>
<div style="display:flex; justify-content:center;">
    <video width="320" height="500" src="{FILENAME}" preload controls></video>
    <a href="{FILENAME}" download>
        <p style="margin-top: 3;">Click this to download and wait two seconds</p>
    </a>
</div
"""
TEMPLATE_ERROR = """
<div style="display:flex; justify-content:center;">
    <a href="http://{HOST}:{PORT}">Return to home</a>
</div
"""
TEMPLATE_PDF = """
<script src="https://mozilla.github.io/pdf.js/build/pdf.js"></script>

<h1>PDF.js Previous/Next example</h1>

<div>
    <button id="prev">Previous</button>
    <button id="next">Next</button>
    &nbsp; &nbsp;
    <span>Page: <span id="page_num"></span> / <span id="page_count"></span></span>
</div>

<canvas id="the-canvas"></canvas>
<script>
    var url = 'https://{HOST}:{PORT}/{FILENAME}';
</script>
<script src="demo_defer.js" defer></script>
"""