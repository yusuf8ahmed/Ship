# Ship
Ship is a command line application that makes transferring files from a computer to a phone or another computer easy <br>
Ship is Developed on MacOS Catalina and should work with any Mac OS X 10.7 (Lion) or newer

<a href="https://www.producthunt.com/posts/ship-9?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-ship-9" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=206345&theme=light" alt="Ship - The best way to move files between your devices | Product Hunt Embed" style="width: 250px; height: 54px;" width="250px" height="54px" /></a>

# Usage

## How to use 
1. type in the command and filename that you want to share.
```bash 
ship [FILENAME]
```

2. After copy the url into anthor device brower can be phone or computer.
```bash
Make sure to click 'ctrl-c' to kill after usage
Sun Jun 14 11:19:34 2020 Sharing Server Starts text - http://192.168.2.178:9999
```

3. Download by clicking download and close the server by click Ship
```bash
^CSun Jun 14 11:21:58 2020 Sharing Server Stop - http://192.168.2.178:9999
```

## Advanced Information
```bash 

usage: ship [-h] [-p [file]] [file]

Send file to phone or other computers. Make sure to kill this process after
completetion

positional arguments:
  file                  file to be shared

optional arguments:
  -h, --help            show this help message and exit
  -p [file], --port [file] port to be shared one
```


# MacOS

## Installation
1. clone this repo with the lastest tag <br>
`git clone https://github.com/yusuf8ahmed/Ship.git --branch v0.0.1.5 --single-branch`
2. go into the Ship folder<br>
`cd Ship`
3. and open the terminal and run <br>
`bash install.sh`

## Uninstallation
1. Go into the Ship folder and open the terminal and run <br>
`bash unistall.sh`

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

# Issues
## Templating
Since the template are loaded in with python format method anything the uses curly braces will cause an error which include: any Javascript function, if statments, try - execpt blocks and embedded css.

## Mimetypes 
Can only load in Mimetypes defined in the standard package "import mimetypes"