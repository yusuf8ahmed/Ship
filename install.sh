echo "Welcome to ship:
Ship is a simple python command line application
made to ease the transfer of files with the use 
of the internet.
"

echo "Now adding ship to PATH"

# making bin directory
mkdir bin
# Moving Shipapp/dist/ship files to Shipapp/bin
cp -a dist/ship/. bin
#Adding bin to PATH
sudo cp -a bin/. /usr/local/bin