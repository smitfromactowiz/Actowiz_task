import json
import requests
from lxml import html

headers = {
    "content-type": "text/html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}

data = requests.get("https://www.maggi.in/en/product/maggi-2-minute-special-masala-instant-noodles/", headers=headers)

if data.status_code == 200:
    root = html.fromstring(data.text)
    table = root.xpath('//div[@class="mg-freeze-table__main"]//table')
    table = table[0]
    rows = table.xpath('.//tr')
    nutrition_info = {}
    for row in rows:
        columns = row.xpath('.//td')
        if len(columns) >= 2:
            main_key = columns[0].text_content().strip()
            if main_key[0]=="-":
                main_key = main_key[1:]
            key = table.xpath('.//th')
            d1={}
            i=0
            for k,v in zip(key,columns):
                v1 = v.xpath('.//text()')
                k1 = k.xpath('.//text()')
                if k1:
                    if i < 2:   
                        d1[k1[0].strip()]=float(v1[0].strip())
                    else:
                        d1[k1[0].strip()]=v1[0].strip()
                    i=i+1
            nutrition_info[main_key] = d1
                        
with open("output.json", "w") as f:
    json.dump(nutrition_info, f, indent=4)