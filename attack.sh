echo "****************************"
echo "Running with security off"
echo "****************************"
cd /etc/modsecurity
rm modsecurity.conf
cp /home/haxbox/Code/Projects/Attack/mod_sec_configs/modsecurity_off.conf ./modsecurity.conf
sudo systemctl restart apache2
cd /home/haxbox/Code/Projects/Attack
python3 attack.py

echo ""
echo "****************************"
echo "Running with security on"
echo "****************************"
cd /etc/modsecurity
rm modsecurity.conf
cp /home/haxbox/Code/Projects/Attack/mod_sec_configs/modsecurity_on.conf ./modsecurity.conf
sudo systemctl restart apache2
cd /home/haxbox/Code/Projects/Attack
python3 attack.py