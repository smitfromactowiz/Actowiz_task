
# ai generated code just for understaing purpose, not for execution


import requests
from lxml import html
import mysql.connector


connect = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="music_db"
)

cursor = connect.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS billboard_top_1001 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    song_name VARCHAR(255),
    artist_name VARCHAR(255),
    image_url TEXT,
    lw INT NULL,
    peak INT,
    weeks INT,
    debut_position INT NULL,
    debut_chart_date VARCHAR(50),
    peak_position INT NULL,
    peak_chart_date VARCHAR(50),
    awards TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")



def first_or_none(values, strip=True):

    if not values:
        return None
    return values[0].strip() if strip and isinstance(values[0], str) else values[0]


def parse_int(value):

    if value in (None, "", "-"):
        return None
    try:
        return int(value)
    except:
        return None



url = "https://www.billboard.com/charts/hot-100/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:

    root = html.fromstring(response.text)

    chart_rows = root.xpath(
        '//div[contains(@class,"o-chart-results-list-row-container")]'
    )

    for item in chart_rows:

        try:
            

            image_url = first_or_none(item.xpath('.//img/@src'))

            song_name = first_or_none(
                item.xpath('.//h3[contains(@id,"title-of-a-story")]/text()')
            )

            artist_parts = item.xpath('.//span[contains(@class,"a-no-trucate")]//text()')
            artist_name = " ".join(
    part.strip() for part in artist_parts if part.strip()
)


            stats = {}

            stat_rows = item.xpath(
                './/div[contains(@class,"lrv-u-flex@desktop")]/div'
            )

            for row in stat_rows:
                label = first_or_none(row.xpath('./span/text()'))
                value = first_or_none(row.xpath('./li/span/text()'))

                if label and value:
                    stats[label] = value

            lw = parse_int(stats.get("LW"))
            peak = parse_int(stats.get("PEAK"))
            weeks = parse_int(stats.get("WEEKS"))


            debut_position = parse_int(
                first_or_none(
                    item.xpath(
                        './/div[contains(@class,"o-chart-position-stats__debut")]'
                        '//div[contains(@class,"o-chart-position-stats__number")]'
                        '/span/text()'
                    )
                )
            )

            debut_chart_date = first_or_none(
                item.xpath(
                    './/div[contains(@class,"o-chart-position-stats__debut")]//a/text()'
                )
            )

            peak_position = parse_int(
                first_or_none(
                    item.xpath(
                        './/div[contains(@class,"o-chart-position-stats__peak")]'
                        '//div[contains(@class,"o-chart-position-stats__number")]'
                        '/span/text()'
                    )
                )
            )

            peak_chart_date = first_or_none(
                item.xpath(
                    './/div[contains(@class,"o-chart-position-stats__peak")]//a/text()'
                )
            )


            awards_list = item.xpath(
                './/div[contains(@class,"o-chart-awards-list")]//p/text()'
            )

            awards = ", ".join(
                award.strip() for award in awards_list if award.strip()
            )

            cursor.execute("""
                INSERT INTO billboard_top_1001 (
                    
                    song_name,
                    artist_name,
                    image_url,
                    lw,
                    peak,
                    weeks,
                    debut_position,
                    debut_chart_date,
                    peak_position,
                    peak_chart_date,
                    awards
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                song_name,
                artist_name,
                image_url,
                lw,
                peak,
                weeks,
                debut_position,
                debut_chart_date,
                peak_position,
                peak_chart_date,
                awards
            ))

            print(f"Inserted:  - {song_name}")

        except Exception as e:
            print("Error parsing row:", e)
    
    connect.commit()



cursor.close()
connect.close()

print("Done")