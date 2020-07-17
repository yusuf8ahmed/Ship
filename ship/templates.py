#!/usr/bin/env python3

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Ship</title>
    <meta charset="UTF-8">
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="main.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Ship is a command line application that makes transferring files from a computer to a phone or another computer easy ">
</head>
<body style="margin: 0;">
    <div class="header">
        <a href="" class="logo">Ship</a>
        <div class="header-right">
            <a href="https://github.com/yusuf8ahmed/Ship">
                <img src="https://raw.githubusercontent.com/tabler/tabler-icons/e46e9271274ff49678b92fe7a514388165b5a586/icons/brand-github.svg"
                    alt="logo"/>
                <!--/*https://github.githubassets.com/favicons/favicon.svg*/-->
            </a>
            <a href="https://twitter.com/yusuf88ahmed">
                <img id="ml10"
                    src="https://raw.githubusercontent.com/tabler/tabler-icons/e46e9271274ff49678b92fe7a514388165b5a586/icons/brand-twitter.svg"
                    alt="logo"/>
            </a>
        </div>
    </div>
    <div class="main">
        <!--BASE_TEMPLATE-->
        {TEMPLATE}
    </div>
    <div id="footer">
        <!--BASE_TEMPLATE-->
        Ship: {VERSION}
    </div>
</body>
</html>
"""

TEMPLATE_AUDIO = """
<div>
    <!--TEMPLATE_AUDIO-->
    <audio controls>
        <source src="{FILENAME}" type="{MIMETYPE}">
        Your browser does not support the audio element.
    </audio>
    <p>Filepath: {FILENAME}</p>
    <button id="shipbutton">
        <a href="{FILENAME}" style="text-decoration: none; color: white;" download>
            <p>Ship It</p>
        </a>
    </button>
</div>
"""

TEMPLATE_IMAGE = """
<div>
    <!--TEMPLATE_IMAGE-->
    <img src="{FILENAME}" alt="{FILENAME} image" style="width: 400px;height: auto;">
    <p>Filepath: {FILENAME}</p>
    <button id="shipbutton">
        <a href="{FILENAME}" style="text-decoration: none; color: white;" download>
            <p>Ship It</p>
        </a>
    </button>
</div>
"""

TEMPLATE_TEXT = """
<div>
    <!--TEMPLATE_TEXT-->
    <iframe src="{FILENAME}" id="text" 
        style="width: 350px;height: 230px; border:0 ; 
        border-left: 6px solid #ccc!important; border-color: #D3D3D3!important;">
    </iframe>
    <p>Filepath: {FILENAME}</p>
    <button id="shipbutton">
        <a href="{FILENAME}" style="text-decoration: none; color: white;" download>
            <p>Ship It</p>
        </a>
    </button>
</div>
"""

TEMPLATE_VIDEO = """
<div>
    <!--TEMPLATE_VIDEO-->
    <video src="{FILENAME}" autoplay preload controls>
        Your browser does not support the video tag.
    </video>
    <p>Filepath: {FILENAME}</p>
    <button id="shipbutton">
        <a href="{FILENAME}" style="text-decoration: none; color: white;" download>
            <p>Ship It</p>
        </a>
    </button> 
</div>
"""

TEMPLATE_ERROR = """ 
<div>
    <!--TEMPLATE_ERROR -->
    <p>{MESSAGE}</p>
    <a href="">Return to home</a>
</div>
"""

TEMPLATE_PDF = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Ship</title>
    <meta charset="UTF-8">
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="main.css">
    <script src="https://mozilla.github.io/pdf.js/build/pdf.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Ship is a command line application that makes transferring files from a computer to a phone or another computer easy ">
</head>
<body style="margin: 0;">
    <div class="header">
        <a href="" class="logo">Ship</a>
        <div class="header-right">
            <a href="https://github.com/yusuf8ahmed/Ship">
                <img src="https://raw.githubusercontent.com/tabler/tabler-icons/e46e9271274ff49678b92fe7a514388165b5a586/icons/brand-github.svg"
                    alt="logo"/>
                <!--/*https://github.githubassets.com/favicons/favicon.svg*/-->
            </a>
            <a href="https://twitter.com/yusuf88ahmed">
                <img id="ml10"
                    src="https://raw.githubusercontent.com/tabler/tabler-icons/e46e9271274ff49678b92fe7a514388165b5a586/icons/brand-twitter.svg"
                    alt="logo"/>
            </a>
        </div>
    </div>
    <div class="main">
        <!--TEMPLATE_PDF-->
        <div>
            <div>
                <button id="prev">Previous</button>
                <button id="next">Next</button>
                &nbsp; &nbsp;
                <span>Page: <span id="page_num"></span> / <span id="page_count"></span></span>
            </div>
            <canvas id="the-canvas" style="border: 1px solid black; direction: ltr; width:100%; height:100%;" height="673" width="476">
            </canvas>
            <p>Filepath: {FILENAME}</p>
            <button id="shipbutton">
                <a href="{FILENAME}" style="text-decoration: none; color: white;" download>
                    <p>Ship It</p>
                </a>
            </button>         
        </div>
    </div>
    <div id="footer">
        <!--TEMPLATE_PDF-->
        Ship: {VERSION}
    </div>
    <script>
        var url = window.location.href+'{FILENAME}';
    </script>
    <script src="demo_defer.js" defer></script>
</body>
</html>
"""

UNVIEWABLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Ship</title>
    <meta charset="UTF-8">
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="main.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Ship is a command line application that makes transferring files from a computer to a phone or another computer easy ">
</head>
<body style="margin: 0;">
    <div class="header">
        <a href="" class="logo">Ship</a>
        <div class="header-right">
            <a href="https://github.com/yusuf8ahmed/Ship">
                <img src="https://raw.githubusercontent.com/tabler/tabler-icons/e46e9271274ff49678b92fe7a514388165b5a586/icons/brand-github.svg"
                    alt="logo"/>
                <!--/*https://github.githubassets.com/favicons/favicon.svg*/-->
            </a>
            <a href="https://twitter.com/yusuf88ahmed">
                <img id="ml10"
                    src="https://raw.githubusercontent.com/tabler/tabler-icons/e46e9271274ff49678b92fe7a514388165b5a586/icons/brand-twitter.svg"
                    alt="logo"/>
            </a>
        </div>
    </div>
    <div class="main" style="flex-direction: column;">
        <!--UNVIEWABLE_TEMPLATE-->
        <div>
            <p>file cannot be viewed but can be downloaded</p> <br>
            <p>Filepath: {FILENAME}</p> <br>
            <button id="shipbutton">
                <a href="{FILENAME}" style="text-decoration: none; color: white;" download>
                    <p>Ship It</p>
                </a>
            </button> 
        </div>
    </div>
    <div id="footer">
        <!--UNVIEWABLE_TEMPLATE-->
        Ship: {VERSION}
    </div>
</body>
</html>
"""

TEMPLATE_URL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Ship</title>
    <meta charset="UTF-8">
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="main.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Ship is a command line application that makes transferring files from a computer to a phone or another computer easy ">
</head>
<body style="margin: 0;">
    <div class="header">
        <a href="" class="logo">Ship</a>
        <div class="header-right">
            <a href="https://github.com/yusuf8ahmed/Ship">
                <img src="https://raw.githubusercontent.com/tabler/tabler-icons/e46e9271274ff49678b92fe7a514388165b5a586/icons/brand-github.svg"
                    alt="logo"/>
                <!--/*https://github.githubassets.com/favicons/favicon.svg*/-->
            </a>
            <a href="https://twitter.com/yusuf88ahmed">
                <img id="ml10"
                    src="https://raw.githubusercontent.com/tabler/tabler-icons/e46e9271274ff49678b92fe7a514388165b5a586/icons/brand-twitter.svg"
                    alt="logo"/>
            </a>
        </div>
    </div>
    <div class="main" style="flex-direction: column;"> 
        <!--TEMPLATE_URL-->
        <p style="line-break: anywhere;width: 70%;text-align: center;">
        {LINK}
        </p>
        <button id="shipbutton" style="width: unset;">
            <a href="{LINK}" style="text-decoration: none; color: white;">
                <p>OPEN LINK</p>
            </a>
        </button> 
    </div>
    <div id="footer">
        <!--TEMPLATE_URL-->
        Ship: {VERSION}
    </div>
</body>
</html>
"""