#install apache - if it does not exist
sudo apt-get update
sudo apt-get install apache2

#install mod-security
sudo apt-get install libapache2-mod-security2
mv /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
