# Ship 🚢

Ship is a command line application that makes transferring files from a computer to a phone or another computer easy <br>
Ship is Developed on macOS Catalina and should work on all platforms that python3 supports

<a href="https://www.producthunt.com/posts/ship-9?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-ship-9" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=206345&theme=light" alt="Ship - The best way to move files between your devices | Product Hunt Embed" style="width: 250px; height: 54px;" width="250px" height="54px" /></a>
<br>
[![forthebadge](https://forthebadge.com/images/badges/uses-badges.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-electricity.svg)](https://forthebadge.com)

## Table of Contents
  * [Requirements 📺](#requirements-📺)
  * [Installation ⬆️](#installation-⬆️)
  * [uninstallation ⬇️](#uninstallation-⬇️)
  * [Usage 💯](#usage-💯)
  * [Releases 🏭](#releases-🏭)
  * [Common issues when Installing 🪑](#common-issues-when-installing-🪑)
  * [Platforms Tested on 🧪](#platforms-tested-on-🧪)
  * [Issues 🤫](#issues-🤫)

# Requirements 📺
* pip is required to download ship
* to download pip on windows users use click [Python 3.7.7](https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64-webinstall.exe)
* to download pip on darwin macOS(for OS X 10.9 and later) click [Python 3.7.7](https://www.python.org/ftp/python/3.7.7/python-3.7.7-macosx10.9.pkg)

## Installation ⬆️ 
* Obviously should not be install in a virtual environment
```bash
pip install shipapp
```

## Uninstallation ⬇️
```bash
pip uninstall shipapp
```

# Usage 💯

## How to use (Basic)
1. Type in the command and filename that you want to share.
```bash 
ship [FILENAME]
```

2. Copy the url into another device browser (can be phone or computer).
```bash
Make sure to click 'ctrl-c' to kill after usage
Mon Jul  6 22:37:27 2020 Sharing Server Starts - http://0a1752d38560.ngrok.io
```

3. Download by clicking 'Ship It' and close the server by clicking <kbd>Ctrl</kbd> + <kbd>c</kbd>
```bash
^CMon Jul  6 23:26:38 2020 Sharing Server Stop - http://0a1752d38560.ngrok.io
```

## Advanced Information ⚙️
```bash 
usage: ship [-h] [-p [port]] [-q] [-P] [-L] [-l] [-V] [-v] [main]

Send file to phone or other computers. Make sure to kill this process after completetion
if your phone is having trouble reading qrcode use flag -q: ship -q [FILENAME]

positional arguments:
  main                  file to be shared

optional arguments:
  -h, --help            show this help message and exit
  -p [port], --port [port]
                        port to be shared on
  -q, --qrcode          if flagged qrcode will be in new tab
  -o, --open            if flagged browser will open automatically
  -P, --private         if flagged host address will be on private ip
  -L, --localhost       if flagged host address will be localhost
  -l, --link            if flagged ship will start the Link Sharing Server
  -V, --verbose         if flagged additional details will be shown via stdout
  -v, --version         show program's version number and exit
```

# Releases 🏭

## alpha release v0.0.4.0 (In development/unstable)
Ship will watch a file and will restart server with new file content<br>
Ship can now be called from within Python as Shipapp.ShipIt<br>

## alpha release v0.0.3.0
Now Ship can fallback on an Empty port if port 9999 is being used <br>
Whole codebase revamp/rewrite with better errors and comments<br>
Now you can run multiple instance on Ship<br>
Whole design with use of external css<br>
Ship can now share links on top of files<br>
new -o, --open cli flag auto open browsers on host computer <br>
new -P, --private cli flag: if flagged host address will be on private ip<br>
new -L, --local cli flag: force port to localhost/127.0.0.1<br>
new -V, --verbose cli flag: additional details will be shown via stdout<br>
new -l, --link cli flag: ship will start the Link Sharing Server<br>

### **alpha release v0.0.2.1**
### **alpha release v0.0.2.0**
full release on pypi <br>
support for inline and new tab qrcodes <br>
new -q, --qrcode cli flag: to display flag <br>
new -V, -version cli flag: to show version <br>
more readable errors <br>
git clone installation is not long available <br>

### **alpha release v0.0.1.6**
help file update <br>

### **alpha release v0.0.1.5**
build dist errors <br>

### **alpha release v0.0.1.4**
float right on all templates <br>

### **alpha release v0.0.1.3**
build dist errors <br>

### **alpha release v0.0.1.2**
template decision error fixed <br>
text template fixed <br>
error raising error fixed <br>

### **alpha release v0.0.1.1**
initial release

# Common issues when Installing 🪑

## Ubuntu PATH issue when downloading 
When installing ship (shipapp) python might say that script is not placed in
The PATH to solve this problem follow the steps

1. enter bashrc config file with vim 
```bash
vi .bashrc
```
2. enter insert mode in vim <kbd>Esc</kbd> then press <kbd>i</kbd> for insert
3. then at the top write with the path the python outputted
```bash
export PATH='(the path that python outputted):$PATH'
```
4. then exit vim by pressing <kbd>Esc</kbd> then typing <kbd>:</kbd><kbd>w</kbd> <kbd>q</kbd>
5. then exit the terminal and enter again then ship command should now be available 😀

# Platforms Tested on 🧪

### MacOS Catalina - version 10.15.6 😀😀
### Windows 10 - version 2004 😀😀
### Canonical Ubuntu - version 20.04 😀😀

# Issues 🤫
## Templating
Since the template are loaded in with python format method anything the uses curly braces will cause an error which include: any Javascript function, if statements, try - except blocks and embedded css.

## Mimetypes 
Can only load in mimetypes defined in the standard package.