# importing necessary libraries
import requests 
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# defining the api-endpoint  
API_ENDPOINT = "http://sldckerala.com/index.php"

# defining the headers
headers = {"Host": "sldckerala.com",
"Connection": "keep-alive",
"Cache-Control": "max-age=0",
"Upgrade-Insecure-Requests": "1",
"Origin": "http://sldckerala.com",
"Content-Type": "application/x-www-form-urlencoded",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Referer": "http://sldckerala.com/index.php",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "en-US,en;q=0.9"}

i=0

# http://sldckerala.com/index.php?txtDate=1587859200&date1=2020-06%2F20-02&date1_dp=1&date1_day=04&date1_month=03&date1_year=2020&sbtstore=SHOW

#init function
def init() :
    global i
    global today
    global day
    global month
    global year
    global parsed_html 

    today = datetime.today()- timedelta(days = i)
    day = today.day
    month = today.month
    year = today.year

    # data to be sent to api 
    data = {'txtDate':"0",
            'date1':"0",
            'date1_dp':'0',
            'date1_day':str(day),
            'date1_month':str( month), 
            'date1_year':str(year), 
            'sbtstore':'SHOW',
            } 
    
    # sending post request and saving response as response object 
    try :
        r = requests.post(url = API_ENDPOINT,headers=headers, data = data) 
    except:
        print("Server unreachable [Check Internet Connection] Exiting...")
        quit()

    print("Date is  :" +str(day)+ "-" + str( month) + "-" + str(year) )

    if r.status_code == 200:
        # parsing response text 
        parsed_html = BeautifulSoup(r.text, 'html.parser')

        if (len(parsed_html.find_all(class_="labelc1"))==0 ):
            print("NO DATA AVAILABLE FOR : "+ str(day)+ "-" + str( month) + "-" + str(year))
            print("Checking previous day ")
            print()
            i+=1
            if i > 7: 
                print("So many days checked i give up ..exiting...  ")
                quit()
            init()

    else:
        print("Server unreachable exiting...  "+ "Server code" +r.status_code)
        quit()


init()
parsed_html=parsed_html.find_all(class_="labelc1")

# extracting response text  
for i in range(0,7):
    print("Dam Name = "+ parsed_html[20+16*i].get_text())
    print("Storage = "+ parsed_html[30+16*i].get_text()+"%")
    print()

for i in range(0,4):
    print("Dam Name = "+ parsed_html[16*8+11+16*i].get_text())
    print("Storage = "+ parsed_html[16*8+11+10+16*i].get_text()+"%")
    print()

for i in range(0,5):
    print("Dam Name = "+ parsed_html[16*11+11+23+16*i].get_text())
    print("Storage = "+ parsed_html[16*11+11+23+10+16*i].get_text()+"%")
    print()