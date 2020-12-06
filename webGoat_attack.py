import requests
import json

#Constants
mURL = 'http://localhost:8080/WebGoat'
APP_USER = 'guest1'
APP_PASSWORD = 'guest123'
EXP_RESP = 200

#Global Variables
isLoggedIn = False

################
# Tests
################

#Test log in successfull
def test_LoggedIn(response):
    failed = ("WebGoat/login" in response.url)
    if failed: print("ERROR: Failed to log in") 
    else: print("......Logged in")    

#Print packet details
def printPacket(packet, printText):
    print("\n***** Request *****")
    print("Request body:\n", packet.request.body)
    print("Request Headers:\n", packet.request.headers)
    print("\n***** Response *****")
    print("Status Code:", packet.status_code)
    print("url", packet.url)
    print("headers", packet.headers)    
    if printText:
        print("$$$$$$ Text\n", packet.text)


def checkHome(mSession):   
    #should change to checkAtLogin, check for /WebGoat/login 
    #regex?
    x = mSession.get(mURL + "/welcome.mvc")
    printPacket(x, False)
     

def login(mSession):
    #login to web app
    global mSessionID
    print ("Attempting Login")
    payload = {
        "username": APP_USER,
        "password": APP_PASSWORD       
    }

    cust_headers = {
        "Host":"localhost:8080",
        "Connection":"keep-alive",
        "Cache-Control":"max-age=0",
        "Upgrade-Insecure-Requests":"1",
        "Origin":"http://localhost:8080",
        "Content-Type":"application/x-www-form-urlencoded",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site":"same-origin",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-User":"?1",
        "Sec-Fetch-Dest":"document",
        "Referer":"http://localhost:8080/WebGoat/login",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"en-US,en;q=0.9",
    }

    y = mSession.post(mURL + "/login", data=payload, headers=cust_headers)
    #print("$$$$-Current cookies\n", mSession.cookies.get_dict())
    printPacket(y, False)
    test_LoggedIn(y)
 
def test_SQL_Injection_1(mSession):
    #Basic 
    print ("...Getting SQLInjectionLesson")
    responseA = mSession.get("http://localhost:8080/WebGoat/start.mvc#lesson/SqlInjection.lesson.lesson")
    printPacket(responseA, True)
    responseB = mSession.get("http://localhost:8080/WebGoat/start.mvc#lesson/SqlInjection.lesson/1")
    printPacket(responseB, True)
    attackURL = "http://localhost:8080/WebGoat/SqlInjection/attack2?query=select * from employees where userid = 96134"
    #WHERE first_name = Bob    
    payload = {
        #"query" : "select department from employees where userid = 96134",        
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"en-US,en;q=0.9",
        "Connection":"keep-alive",
        "Content-Length":"60",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Host":"localhost:8080",
        "Origin":"http://localhost:8080",
        "Referer":"http://localhost:8080/WebGoat/start.mvc",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
    }
    response = mSession.post(attackURL, payload)
    print("...SQL Injection Attack 1 w\cookies")
    printPacket(response, True)

def test_SQL_Injection_2(mSession):
    attackURL = "http://localhost:8080/WebGoat/SqlInjection/attack2"
    payload = {
        "query":"UPDATE employees SET department = 'Sales' WHERE userID = 89762"
    }

    response = mSession.post(attackURL, payload)
    print("...SQL Injection Attack 2 w\cookies")
    printPacket(response, false)

def main():
    print("Attacking - " + mURL)
    session = requests.Session()
    login(session)
    test_SQL_Injection_1(session)
    #test_SQL_Injection_2(session)
    #checkHome(session)
    
    


if __name__ == "__main__":
    main()
    