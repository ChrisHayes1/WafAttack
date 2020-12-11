attack.py contains the scripted attacks

attack.sh contains the attack with and without modsecurity on.  I took the easy route for this and just copy different versions of the file instead of parse the file itself.  If configuration was getting modified more you could update the code.

modsec_audit.log contains a copy of the mod security audit log from the last time I ran the test

response.html contains the output.  I ran attack.sh with

sudo sh attack.sh > response.html