import json
import requests
from lxml import html
from request_pagedata import getPageData
from db import mydb
from concurrent.futures import ThreadPoolExecutor

cursor = mydb.cursor()
finalobjectList = {}
finalstateList = {}
eachCardDataList=[]

def getDetailsData(data,cityname):
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'csrf-token': 'undefined',
        'origin': 'https://www.kia.com',
        'priority': 'u=1, i',
        'referer': 'https://www.kia.com/in/buy/find-a-dealer/result.html?state=AP&city=S99',
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': '_fbp=fb.1.1776764593967.602077032441334660; _twpid=tw.1776764595635.170069533164713639; renderid=rend01; WMONID=VNN3Kp4f_PI; SCOUTER=x53rq1abio8ouj; _gid=GA1.2.1079174784.1776765707; cookie-agree=true; _gat_UA-137890001-2=1; _gcl_au=1.1.1481527713.1776764594.1064858225.1776777195.1776777194; JSESSIONID=node0c1rt45e3fqvp1ga7yv91swwuc1637462.node0; __cflb=04dToPPtdqTVeCCaEkPQCuAY2ttTQ1p5yakDCixuiP; _uetsid=84777d603d6611f19c576d1cb1052838; _uetvid=84779a903d6611f187c0e557ff2b4bfb; _ga=GA1.1.1184121850.1776764595; __cf_bm=Mb7eXjK6owG.foTAVpbgR03NvCMDZvAvg33dk_DE0wM-1776777228.7278757-1.0.1.1-bHxmDoSaEAy4s7QFj9mHcY1GEcUs9vyXxi_RI8sG_LNmsKSy4MTnm2mfJT8Mhs8RsNq0v7.aCAIAy4yLrfMs2y16oSTXkuN1q3sPSQED8Buv5LZVPfoIC3lKfN8LhfXt; _ga_9PSV9LG5D2=GS2.1.s1776777194$o4$g1$t1776777229$j25$l0$h0',
    }

    delerdata = getPageData("https://www.kia.com/api/kia2_in/findAdealer.getDealerList.do",data)
    if delerdata.status_code == 200:
         detailsjsondata = json.loads(delerdata.text)

         for item in detailsjsondata.get("data"): 
            global counter 
            counter = counter +1
            print(counter)
            address_parts = [
                item.get("address1"),
                item.get("address2"),
                item.get("address3")
            ]
            full_address = ", ".join([part for part in address_parts if part])
            eachCardDataList.append({
                "website": item.get("website"),
                "dealerName": item.get("dealerName"),
                "address": full_address,
                "phone1": item.get("phone1"),
                "phone2": item.get("phone2"),
                "cityName": item.get("cityName"),
                "stateName": item.get("stateName"),
                "dealerType": item.get("dealerType"),
            })
            cursor.execute("""
                INSERT INTO dealers
                (website, dealer_name, address, phone1, phone2, city_name, state_name, dealer_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item.get("website"),
                item.get("dealerName"),
                full_address,  # from your cleaned address logic
                item.get("phone1"),
                item.get("phone2"),
                item.get("cityName"),
                item.get("stateName"),
                item.get("dealerType")
            ))
        
         finalstateList[cityname] = eachCardDataList

stateandcitystr = getPageData("https://www.kia.com/api/kia2_in/findAdealer.getStateCity.do")
if stateandcitystr.status_code == 200:
    stateandcity = json.loads(stateandcitystr.text)

    counter = 0
    for item in stateandcity.get("data").get("stateAndCity"):
        state = item.get("val1").get("key")
        statename = item.get("val1").get("value")
        finalstateList={}
        for citydata in item.get("val2"):
            eachCardDataList=[]
            city = citydata.get("key")
            cityname = citydata.get("value")
            data = {
                "state" : state,
                "city" : city,
                'dealerType': 'A',
            }
            with ThreadPoolExecutor(max_workers=5) as e:
                e.submit(getDetailsData,data=data,cityname=cityname)
            
        finalobjectList[statename] = finalstateList
    
       

# mydb.commit()
# mydb.close()
with open("finaloutput.json","w",encoding="utf-8") as f:
    json.dump(finalobjectList,f,ensure_ascii=False)
