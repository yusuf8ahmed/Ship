echo "Uninstall Ship:
If you having problems or error please tell me
on the github issues page:
https://github.com/yusuf8ahmed/Ship/issues 
"

read -r -p "Proceed with uninstallation? [y/n]:  " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    unlink /usr/local/bin/ship
else
    exit 0
fi