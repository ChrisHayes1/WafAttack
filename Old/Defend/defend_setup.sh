# #run with $ sudo sh env_setup.sh

# #install docker
# sudo apt install -y docker.io
# sudo systemctl enable docker --now
# dockersudo usermod -aG docker $USER
# #List containers
# #sudo docker ps -a
# #stop container
# #sudo docker stop container_name #note - not image name

# #run docker - might want to put this in a different file as it may be run more than just on env setup
# sudo docker run --rm -it -p 80:80 vulnerables/web-dvwa

# #Need to go to localhost/setup.php and then select create / reset database
# localhost#I should be able to run this as a python script with request

#Ensure we have all the necessary softwar
sudo apt-get -y install apache2 mariadb-server php php-mysqli php-gd libapache2-mod-php

#Install DVWA
cd /var/www/html
sudo cp -r /proj/CS740WAFPROJ/dvwa ./dvwa


#Start MariaDB
sudo systemctl enable mysql
sudo systemctl start mysql

#Set up user in SQL
sudo mysql
create database dvwa;
create user dvwa@localhost identified by 'p@ssw0rd';
grant all on dvwa.* to dvwa@localhost;
flush privileges;
exit

#copy config to final location
sudo cp config.inc.php.dist config.inc.php

#return to users
exit