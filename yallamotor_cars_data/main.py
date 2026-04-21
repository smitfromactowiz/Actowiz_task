import json
import requests
from lxml import html
from request_pagedata import getPageData

finalobjectList = []
def getDetailsData(data):
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'csrf-token': 'undefined',
        'origin': 'https://www.kia.com',
        'priority': 'u=1, i',
        'referer': 'https://www.kia.com/in/buy/find-a-dealer/result.html?state=AN&city=EEE',
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': '_fbp=fb.1.1776764593967.602077032441334660; _twpid=tw.1776764595635.170069533164713639; renderid=rend01; WMONID=VNN3Kp4f_PI; SCOUTER=x53rq1abio8ouj; __cflb=04dToPPtdqTVeCCaEkPQCuAY2ttTQ1pCXBW7XKPNgX; __cf_bm=X3YLzQbTgbVZmLlU2ZeT0PX9cb8.JRJErGQGWllxeOc-1776765704.9407337-1.0.1.1-LJW2ddbcMy_ymb53tce43kaEaMweVpshhExa9wNipw5ozgSOMCOJAyk0C9CZIkyt0H3WELFRZJaomKZ797ObsQ0q985W_OBjb0Tth1Se9B8J60lrFL84LwbbKcbYtWvu; _gid=GA1.2.1079174784.1776765707; cookie-agree=true; _gat_UA-137890001-2=1; _gcl_au=1.1.1481527713.1776764594.90683660.1776765073.1776766119; JSESSIONID=node01ou960pk30xd61g15jey1jd56u1620951.node0; _ga_9PSV9LG5D2=GS2.1.s1776764594$o1$g1$t1776766120$j59$l0$h0; _ga=GA1.1.1184121850.1776764595; _uetsid=84777d603d6611f19c576d1cb1052838; _uetvid=84779a903d6611f187c0e557ff2b4bfb',
    }
    delerdata = requests.post("https://www.kia.com/api/kia2_in/findAdealer.getDealerList.do",headers=headers,data=data)
    if delerdata.status_code == 200:
         detailsjsondata = json.loads(delerdata.text)

         for item in detailsjsondata.get("data"): 
            print(item.get("website"))
            finalobjectList.append({
                "website": item.get("website"),
                "dealerName" : item.get("dealerName"),
                "address" : item.get("address1"),
                "phone1" : item.get("phone1"),
                "phone2" : item.get("phone2"),
                "dealerType" : item.get("dealerType"),
                "city_name":item.get("cityName"),
                "state_name":item.get("stateName")
            })


stateandcitystr = getPageData("https://www.kia.com/api/kia2_in/findAdealer.getStateCity.do")
stateandcity = json.loads(stateandcitystr)

for item in stateandcity.get("data").get("stateAndCity"):
    state = item.get("val1").get("key")
    for citydata in item.get("val2"):
        city = citydata.get("key")
        data = {
            'state': state,
            'city': city,
            'dealerType': 'A',
        }
        getDetailsData(data)

with open("finaloutput.json","w",encoding="utf-8") as f:
    json.dump(finalobjectList,f,ensure_ascii=False)