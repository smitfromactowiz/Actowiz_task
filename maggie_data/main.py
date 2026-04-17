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
    if not table:
        raise Exception("Nutrition table not found")
    table = table[0]
    rows = table.xpath('.//tr')
    nutrition_info = {}
    key = table.xpath('.//th')

    for row in rows:
        columns = row.xpath('.//td')
        if len(columns) >= 2:
            main_key = columns[0].text_content().strip().lstrip("-")
          
            d1={}
            for k,v in zip(key,columns):
                v1 = v.text_content().strip()
                k1 = k.text_content().strip()
                if k1:
                    try:
                        value = float(v1)
                    except ValueError as e:
                        value = v1
                        pass
                     
                  
                    
                    d1[k1]=value
                    
            nutrition_info[main_key] = d1
                        
with open("output.json", "w") as f:
    json.dump(nutrition_info, f, indent=4)