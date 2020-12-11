# 1 - Setup DETER with NS file

# 2 - SSH into 
#   ssh uwiscmaa@users.isi.deterlab.net -p 22
#   Enter password

#3 - download git folder
#   cd /mnt/projects/proj/CS740WAFPROJ
#   git clone https://github.com/ChrisHayes1/WafAttack.git

#4 Run

#Download DVWA for victim
cd /proj/CS740WAFPROJ
git clone https://github.com/digininja/DVWA.git
 
#4 - Run main_install.sh from Within users.isi.deterlab.net
ssh Victim.sandbox.CS740WAFPROJ.isi.deterlab.net
cd /proj/CS740WAFPROJ/WafAttack/Proxy
sudo sh defend_setup.sh

ssh Attack.sandbox.CS740WAFPROJ.isi.deterlab.net
