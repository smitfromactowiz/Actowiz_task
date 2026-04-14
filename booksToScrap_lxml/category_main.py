import json
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
                cursor.execute("""
                    INSERT INTO books (book_name, book_url)
                    VALUES (%s, %s)
                """, (temp, newurl))
                
                conn.commit()
        cursor.close()
        conn.close()

            


def get_all_link_by_category():

    if data.status_code == 200 :

        cursor.execute("""
CREATE TABLE IF NOT EXISTS books_with_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_name VARCHAR(255),
    book_url TEXT,
    category_name VARCHAR(255),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

        cursor.execute(""" select category_name,category_url from categories """)
        categories = cursor.fetchall()
        for i in categories:
            category_name = i[0]
            category_url = i[1]
            data2 = requests.get(category_url,headers=header)
            root2 = html.fromstring(data2.content)

            
            page = root2.xpath("//ul[contains(@class,'pager')]/li[contains(@class,'current')]/text()")
            if len(page) > 0 :
                pages = int(page[0].split()[-1])
           
                for i in range(1,pages+1):
                    page_url = category_url.replace("index.html",f"page-{i}.html")
                    data3 = requests.get(page_url,headers=header)
                    root3 = html.fromstring(data3.content)
                    book_name = root3.xpath("//article[contains(@class,'product_pod')]/h3/a/@title")
                    book_link = root3.xpath("//article[contains(@class,'product_pod')]/h3/a/@href")

                    for i in range(len(book_name)):
                        temp = book_name[i].replace("\n","").strip()
                        newurl = f"{url}{book_link[i]}".replace("../../../","catalogue/")

                        cursor.execute("""
                            INSERT INTO books_with_category (book_name, book_url, category_name)
                            VALUES (%s, %s, %s)
                        """, (temp, newurl, category_name))
                        conn.commit()
                       
                      
            else:
                book_name = root2.xpath("//article[contains(@class,'product_pod')]/h3/a/@title")
                book_link = root2.xpath("//article[contains(@class,'product_pod')]/h3/a/@href")  

                for i in range(len(book_name)):
                    temp = book_name[i].replace("\n","").strip()
                    newurl = f"{url}{book_link[i]}".replace("../../../","catalogue/")

                    cursor.execute("""
                        INSERT INTO books_with_category (book_name, book_url, category_name)
                        VALUES (%s, %s, %s)
                    """, (temp, newurl, category_name))
                    conn.commit()
                    
        cursor.close()
        conn.close()

get_all_link_by_category()