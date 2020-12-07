#install docker
sudo apt install -y docker.io
sudo systemctl enable docker --now
dockersudo usermod -aG docker $USER

#run docker - might want to put this in a different file as it may be run more than just on env setup
docker run --rm -it -p 80:80 vulnerables/web-dvwa
#Need to go to localhost/setup.php and then select create / reset database