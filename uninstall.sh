
read -r -p "Unistalling ship Proceed? [y/n]:  " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    rm -R /usr/local/bin/files
    rm /usr/local/bin/Python
    rm /usr/local/bin/ship
    rm /usr/local/bin/base_library.zip
    rm /usr/local/bin/libcrypto.1.1.dylib /usr/local/bin/libncursesw.5.dylib /usr/local/bin/libssl.1.1.dylib

    read -r -p "Ship will delete all .so files within usr/local/bin Proceed? [y/n]:  " response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
    then
        #shared objects
        rm /usr/local/bin/*.so
    else
        exit 0   
    fi
else
    exit 0
fi