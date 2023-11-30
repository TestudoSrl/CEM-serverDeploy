#!/bin/sh
# Ver. 0.1 10.05.2010
# ..:: Aste83.net ::.. - Installazione Firewall debian.
echo "Installo il firewall. Attendere..."
#apt update && DEBIAN_FRONTEND=noninteractive apt upgrade -y
#DEBIAN_FRONTEND=noninteractive apt install python3-pip -y
#DEBIAN_FRONTEND=noninteractive pip install netifaces psutil -y

DESTINATION_PATH=/etc # without / at the end

cd iptables
python3 get-netinfo-light.py

cp rc.z-fw $DESTINATION_PATH/rc.z
cp rc.z-init $DESTINATION_PATH/init.d/rc.z
# cp get-netinfo-light.py $DESTINATION_PATH
# chmod 777 $DESTINATION_PATH/rc.z
# chmod 777 $DESTINATION_PATH/rc.z

# rm -rif /etc/get-netinfo-light.py
# cd $DESTINATION_PATH/init.d/
# update-rc.d rc.z start 20 2 3 4 5 . stop 20 0 1 6 .
# echo "Installazione eseguita."

# echo "Editare il file /etc/rc.z a piacere"
# #/etc/init.d/rc.z
# #END
