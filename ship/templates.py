#!/usr/bin/env python3

BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>Ship</title>
        <link rel="shortcut icon" href="/files/favicon.ico" type="image/x-icon">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <div style="top: 0;bottom: 0;left: 0;right: 0;">
        {TEMPLATE}        
        <div>
    </body>
</html>
"""

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
    <img src="{FILENAME}" alt="document" style="">
    <div style="">
        <p>Filename: {FILENAME}</p>
        <a href="{FILENAME}" style="text-decoration: none; color: black;" download>
            <p style="text-decoration: none;">download</p>
        </a>    
    </div>
</div>
"""

TEMPLATE_TEXT_ = """
<div>
    <embed src="{FILENAME}" style="border:0 border-left: 6px solid #ccc; border-color: #D3D3D3!important;">
    <p>Filename: {FILENAME}</p>
    <a href="{FILENAME}" style="text-decoration: none;" download>
        <p style="text-decoration: none;">download</p>
    </a>
</div
"""

TEMPLATE_TEXT = """
<div>
    <iframe src="{FILENAME}" id="text" style="border:0; border-left: 6px solid #ccc!important; border-color: #D3D3D3!important;"></iframe>
    <p>Filename: {FILENAME}</p>
    <a href="{FILENAME}" style="text-decoration: none;" download>
        <p style="text-decoration: none;">download</p>
    </a>
</div>
    <script defer>
        var id = 'text'
        document.getElementById("text").height = document.getElementById(id).contentWindow.document.body.scrollHeight + "px"
        document.getElementById("text").width= document.getElementById(id).contentWindow.document.body.scrollWidth + "px"
    </script>
"""

TEMPLATE_VIDEO = """
<div>
    <video src="{FILENAME}" autoplay preload controls>
        Your browser does not support the video tag.
    </video>
    <div style=""> 
        <div style="display: inline-block">
            <p>Filename: {FILENAME}</p>
        </div>
        <div style="display: inline-block;">
            <a href="{FILENAME}" style="text-decoration: none;" download>
                <p>download</p>
            </a> 
        </div>
    </div>
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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <p style="">file cannot be viewed but will download</p>
        <a href="{FILENAME}" style="text-decoration: none;" download>
            <p>download</p>
        </a>
    </body>
</html>
"""