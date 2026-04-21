import requests
import json
from lxml import html

def getPageData(url):
    
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        # 'content-length': '0',
        'csrf-token': 'undefined',
        'origin': 'https://www.kia.com',
        'priority': 'u=1, i',
        'referer': 'https://www.kia.com/in/buy/find-a-dealer.html',
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'renderid=rend01; WMONID=PXp6q1HVl84; SCOUTER=z1u7oabenfpovm; __cflb=04dToPPtdqTVeCCaEkPQCuAY2ttTQ1pFCKsNhTdGf1; _twpid=tw.1776764838686.189474143317254514; _fbp=fb.1.1776764839188.371119609209016231; _gid=GA1.2.1719215777.1776765501; cookie-agree=true; JSESSIONID=node0g9coy65r0nq51m8agc5incj3z1627715.node0; __cf_bm=3lrG1EGBd3Rzl1bB273pVzuJ62hLRj7CmIsBOkmhh4E-1776770805.4642365-1.0.1.1-TNbL8VazVhOtg5IOB.Nr.xADh7LHb6C.WAipLHSaA5iQPwMSzkOxqcB95tKxzdSkKCHwY_BCxGvFF7mgjIWWynUEYYKeU_Ql11W.EhDHD5PgczjVSeifVC93tMXVJGQ9; _gcl_au=1.1.1175457922.1776764837.357001812.1776770807.1776770832; _uetsid=16574c403d6711f19e88f93f669e2b0f; _uetvid=1657dd603d6711f1a9f001bf122958a7; _ga=GA1.1.1751769301.1776764839; _ga_9PSV9LG5D2=GS2.1.s1776770741$o2$g1$t1776771782$j60$l0$h0',
    }

   
    data = requests.get(url,headers=headers)

    if data.status_code == 200:
        return data.text
    
    return None