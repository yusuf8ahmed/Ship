# Ship
Ship is a command line application that makes transferring files from a computer to a phone or another computer easy <br>
Ship is Developed on MacOS Catalina and should work on all platforms that python3 supports

<a href="https://www.producthunt.com/posts/ship-9?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-ship-9" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=206345&theme=light" alt="Ship - The best way to move files between your devices | Product Hunt Embed" style="width: 250px; height: 54px;" width="250px" height="54px" /></a>

# All platforms

## Installation
1. install from pip
`pip install shipapp`

## Uninstallation
1. uninstall from pip
`pip uninstall shipapp`

# Usage

## How to use (Basic)
1. Type in the command and filename that you want to share.
```bash 
ship [FILENAME]
```

2. Copy the url into another device browser (can be phone or computer).
```bash
Make sure to click 'ctrl-c' to kill after usage
Sun Jun 14 11:19:34 2020 Sharing Server Starts text - http://192.168.2.178:9999
```

3. Download by clicking 'download' and close the server by clicking <kbd>Ctrl</kbd> + <kbd>c</kbd>
```bash
^CSun Jun 14 11:21:58 2020 Sharing Server Stop - http://192.168.2.178:9999
```

## Advanced Information
```bash 

abdulwahid@Abdulwahid ~ % ship -h
usage: ship [-h] [-p [port]] [-q] [-V] [file]

Send file to phone or other computers. Make sure to kill this process after completetion
if your phone is having trouble reading qrcode use flag -q: ship -q [FILENAME]

positional arguments:
  file                  file to be shared

optional arguments:
  -h, --help            show this help message and exit
  -p [port], --port [port]
                        port to be shared one
  -q, --qrcode          if flagged qrcode will be in new tab
  -V, --version         show program's version number and exit
```

# Releases
## alpha release v0.0.1.1
initial release

## alpha release v0.0.1.2
template decision error fixed <br>
text template fixed <br>
error raising error fixed <br>

## alpha release v0.0.1.3
build dist errors <br>

## alpha release v0.0.1.4
float right on all templates <br>

## alpha release v0.0.1.5
build dist errors <br>

## alpha release v0.0.1.6
help file update <br>

# Issues
## Templating
Since the template are loaded in with python format method anything the uses curly braces will cause an error which include: any Javascript function, if statments, try - execpt blocks and embedded css.

## Mimetypes 
Can only load in Mimetypes defined in the standard package "import mimetypes"