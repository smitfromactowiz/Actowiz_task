import json
from logging import root
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
CREATE TABLE IF NOT EXISTS billboard_top_100 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    song_name VARCHAR(255),
    artist_name VARCHAR(255),
    image_url TEXT,
    lw INT,
    peak INT,
    weeks INT,
    debut_position VARCHAR(50),
    debut_chart_date VARCHAR(50),
    peak_position VARCHAR(50),
    peak_chart_date VARCHAR(50),
    awards TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")






url = "https://www.billboard.com/charts/hot-100/"
data = requests.get(url)
if data.status_code == 200:
    root = html.fromstring(data.text)
    musiclist = root.xpath('//div[contains(@class,"chart-results-list")]/div[@class="o-chart-results-list-row-container"]')
    for item in musiclist:
        eachitem = item.xpath('ul[contains(@class,"o-chart-results-list-row")]/li')
        imageurl = eachitem[1].xpath('div/div/img/@src')[0]
        songName = eachitem[3].xpath('.//h3/text()')[0].strip()
        artistName = eachitem[3].xpath('ul/li/span//text()')
        if not artistName:
            artistName = eachitem[3].xpath('ul/li/span/text()')[0].strip()
        else:
            artistName = artistName[0].strip()
        rightsection = eachitem[3].xpath('ul/li/ul/div[@class="lrv-u-flex"]/li/span/text()')
        lw = (rightsection[0].strip())
        if lw == "-":
            lw = None
        else:
            lw = int(lw)  
        peak = int(rightsection[1].strip())
        weeks = int(rightsection[2].strip())
        itemExpand= item.xpath('div/div[@class="charts-results-item-detail-inner // "]/div')
        debutPosition = itemExpand[0].xpath('div[@class="o-chart-position-stats__debut"]/div/span/text()')[0].strip()
        debutChartDate = itemExpand[0].xpath('div[@class="o-chart-position-stats__debut"]/div/div/span/a/text()')[0].strip()

        peakPosition = itemExpand[0].xpath('div[@class="o-chart-position-stats__peak"]/div/span/text()')[0].strip()
        peakChartDate = itemExpand[0].xpath('div[@class="o-chart-position-stats__peak"]/div/div/span/a/text()')[0].strip()
        

        awardLists = itemExpand[1].xpath('div[@class="o-chart-awards-list"]/div')
        finalawardList = ""
        if awardLists:
            for award in awardLists:
                awardname = award.xpath('p/text()')[0]
                finalawardList += awardname + ", "

        cursor.execute("""
INSERT INTO billboard_top_100 (song_name, artist_name, image_url, lw, peak, weeks, debut_position, debut_chart_date, peak_position, peak_chart_date, awards)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (songName, artistName, imageurl, lw, peak, weeks, debutPosition, debutChartDate, peakPosition, peakChartDate, finalawardList))
        print(artistName)

    connect.commit()
    cursor.close()
    connect.close()
