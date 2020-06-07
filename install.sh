echo "Welcome to Ship:
Ship is a simple python command line application
made to ease the transfer of files with the use 
of the internet.

Disclamer: Ship will put files in your usr/local/bin
"

read -r -p "Installing ship Proceed? [y/n]:  " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    rm -R bin
    # making bin directory
    mkdir bin
    # Moving Shipapp/dist/ship files to Shipapp/bin
    cp -a dist/ship/. bin
    #Adding bin to PATH
    sudo cp -a bin/. /usr/local/bin
else
    exit 0
fi