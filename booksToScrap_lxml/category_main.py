import json
from urllib.parse import urljoin
from lxml import html
import requests
import mysql.connector
url = "https://books.toscrape.com/"

header = {
   "content-type" : "text/html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}
data = requests.get(url,headers=header)
root = html.fromstring(data.content)

conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="books_db"
    )

cursor = conn.cursor()

def get_category_links():
    if data.status_code == 200 :

        cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255),
    category_url TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


        category_name = root.xpath("//ul[contains(@class,'nav')]/li/ul/li/a/text()")
        category_link = root.xpath("//ul[contains(@class,'nav')]/li/ul/li/a/@href")

        for i in range(len(category_name)):
            temp = category_name[i].replace("\n","").strip()
            newurl = f"{url}{category_link[i]}"

            cursor.execute("""
                INSERT INTO categories (category_name, category_url)
                VALUES (%s, %s)
            """, (temp, newurl))

            conn.commit()
        
    
        cursor.close()
        conn.close()
    print("Categories inserted successfully.")


def get_all_books_links():
     if data.status_code == 200 :
    

        cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_name VARCHAR(255),
    book_url TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")  
        pages =int(root.xpath("//ul[contains(@class,'pager')]/li[contains(@class,'current')]/text()")[0].split()[-1])
        
    
        
        for i in range(1,pages+1):
            url1 = f"{url}catalogue/category/books_1/page-{i}.html"
            data1 = requests.get(url1,headers=header)
            root1 = html.fromstring(data1.content)

            book_name = root1.xpath("//article[contains(@class,'product_pod')]/h3/a/@title")
            book_link = root1.xpath("//article[contains(@class,'product_pod')]/h3/a/@href")
            for i in range(len(book_name)):
                temp = book_name[i].replace("\n","").strip()
                newurl = f"{url}{book_link[i]}".replace("../../","catalogue/")

                newurl1 = urljoin(url1, book_link[i]) # this is how we can use urljoin
               
                cursor.execute("""
                    INSERT INTO books (book_name, book_url)
                    VALUES (%s, %s)
                """, (temp, newurl))
                
                conn.commit()
        cursor.close()
        conn.close()

            


def get_all_book_link_by_category():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books_with_category (
        id INT AUTO_INCREMENT PRIMARY KEY,
        book_name VARCHAR(255),
        book_url TEXT,
        category_name VARCHAR(255),
        category_id INT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    """)

    cursor.execute("SELECT category_name, category_url, id FROM categories")
    categories = cursor.fetchall()

    for category in categories:
        category_name = category[0]
        category_url = category[1]
        category_id = category[2]

        response = requests.get(category_url, headers=header)
        root = html.fromstring(response.content)

        page_text = root.xpath("//ul[contains(@class,'pager')]/li[contains(@class,'current')]/text()")

        total_pages = 1
        if page_text:
            total_pages = int(page_text[0].split()[-1])

        for page_num in range(1, total_pages + 1):

            if page_num == 1:
                page_url = category_url
            else:
                page_url = category_url.replace("index.html", f"page-{page_num}.html")

            page_response = requests.get(page_url, headers=header)
            page_root = html.fromstring(page_response.content)

            book_names = page_root.xpath("//article[contains(@class,'product_pod')]/h3/a/@title")
            book_links = page_root.xpath("//article[contains(@class,'product_pod')]/h3/a/@href")

            for name, link in zip(book_names, book_links):

                full_link = urljoin(page_url, link)

                cursor.execute("""
                    INSERT INTO books_with_category
                    (book_name, book_url, category_name, category_id)
                    VALUES (%s, %s, %s, %s)
                """, (name.strip(), full_link, category_name, category_id))

    conn.commit()

    print("All Books Inserted Successfully")




def product_page_data(url):
    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)
    

    book_title = root.xpath("//div[contains(@class,'product_main')]/h1/text()")[0]
    book_price = root.xpath("//div[contains(@class,'product_main')]/p[contains(@class,'price_color')]/text()")[0]
    instock = int(root.xpath("//div[contains(@class,'product_main')]/p[contains(@class,'instock')]/text()")[1].strip().replace("In stock (", "").replace("available)", "").strip())

    description = root.xpath("//div[@id='product_description']/following-sibling::p/text()")
    if description:
        description = description[0].strip()
    
    rows = root.xpath("//table[contains(@class,'table')]//tr")
    product_info={}
    for row in rows:
        key = row.xpath("./th/text()")[0].strip()
        value = row.xpath("./td/text()")[0].strip()
        product_info[key] = value



    output = {
        "book_title": book_title,
        "book_price": book_price,
        "instock": instock,
        "description": description,
        "product_info": product_info
    }


    with open(f"book_{book_title}_details.json", "a", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
        

get_all_books_links()