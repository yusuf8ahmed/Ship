echo "Welcome to Ship:
Ship is a simple python command line application
made to ease the transfer of files with the use 
of the internet.
"

read -r -p "Proceed with installation? [y/n]:  " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    # Create a symlink to $(pwd)/dist/ship/ship from /usr/local/bin
    ln -s $(pwd)/dist/ship/ship /usr/local/bin
else
    exit 0
fi