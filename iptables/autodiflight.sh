#!/bin/sh
# Ver. 0.1 10.05.2010
# ..:: Aste83.net ::.. - Installazione Firewall debian.
echo "Installo il firewall. Attendere..."
#apt update && DEBIAN_FRONTEND=noninteractive apt upgrade -y
#DEBIAN_FRONTEND=noninteractive apt install python3-pip -y
#DEBIAN_FRONTEND=noninteractive pip install netifaces psutil -y
cd /etc/
wget monitor.jezoo.it/rc.z-fw
wget monitor.jezoo.it/get-netinfo-light.py
python3 get-netinfo-light.py
mv rc.z-fw rc.z
rm -rif /etc/get-netinfo-light.py
chmod 777 rc.z
cd /etc/init.d/
wget monitor.jezoo.it/rc.z-init
mv rc.z-init rc.z
chmod 777 rc.z
update-rc.d rc.z start 20 2 3 4 5 . stop 20 0 1 6 .
echo "Installazione eseguita."
echo "Editare il file /etc/rc.z a piacere"
#/etc/init.d/rc.z
#END
