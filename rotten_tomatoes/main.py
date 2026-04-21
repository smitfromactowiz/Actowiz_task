import json
from lxml import html
from urllib.parse import urljoin
import json
import requests as re
from db import *
from concurrent.futures import ThreadPoolExecutor



def find_url(url):
    res = re.get(url)
    all_json = json.loads(res.text)

    return all_json
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def main(url):
    main_url = 'https://www.rottentomatoes.com/'
    all_data = re.get(url,headers=headers)
    tree = html.fromstring(all_data.text)
    
    script = tree.xpath("//script[@type='application/ld+json']/text()")
    for s in script:
        full_json = json.loads(s)
    page_1 = full_json.get('itemListElement').get('itemListElement')
    all_movie_data = []

    for i in page_1:
        all_movie_data.append(i.get('url').strip())
    unique = tree.xpath("//script[contains(@id,'pageInfo')]/text()")[0]

    end_cursor = json.loads(unique)
    unique_key = end_cursor.get('endCursor')
    

    while True:
        api_url = f'https://www.rottentomatoes.com/cnapi/browse/movies_in_theaters/sort:newest?after={unique_key}'
        other_page = find_url(api_url)
        cursor = other_page.get('pageInfo').get('endCursor')

        if not cursor:
            break

        unique_key = cursor

   

            
        for i in other_page.get('grid').get('list'):
            all_movie_data.append(f"https://www.rottentomatoes.com{i.get('mediaUrl').strip()}")

    return all_movie_data
    



def get_movie_data(movie_url):
    base_url = "https://www.rottentomatoes.com"
    res = re.get(movie_url,headers=headers)
    tree = html.fromstring(res.text)
    movie_name =tree.xpath("string(//rt-text[@size='1.25,1.75']/text())")
    img = tree.xpath("//div[contains(@class,'media-scorecard')]//@src")[0]
    tometometer = tree.xpath("string(//rt-text[@slot='critics-score'])") or '0%'
    popcornmeter = tree.xpath(".//div[contains(@class,'media-scorecard')]//rt-text/text()")[2]
    review_count = int(tree.xpath(".//div[contains(@id,'movie-overview')]//rt-link//text()")[0].split()[0].strip())
    description = tree.xpath("//div[@slot='description']//rt-text/text()")[0].strip()
    whattoknow = tree.xpath("string(//div[@id='critics-consensus']//p)").strip()
    cast_crew_link = urljoin(base_url,tree.xpath(".//section[contains(@class,'cast-and-crew')]//div[contains(@class,'header-wrap')]/rt-button/@href")[0])
    res1 = re.get(cast_crew_link)
    tree1 = html.fromstring(res1.text)
    crew_and_cast = tree1.xpath('.//cast-and-crew-card')
    cast_and_crew = {}
    for i in crew_and_cast:
        # cast_and_crew['name'] : i.xpath('//rt-text[@slot="title"]')
        name = i.xpath('.//rt-text[@slot="title"]/text()')[0].strip()
        img = i.xpath(".//rt-img[@slot='poster']/@src")[0].strip()
        credit = i.xpath(".//rt-text[@slot='credits']/text()")
        credit_string = ""
        for i in credit:
            credit_string +=","+i
        credit_string = credit_string.strip(',')
        cast_and_crew = {
            'name' : name,
            'img' : img,
            'credit' : credit_string
        }
    
    
    video_href = tree.xpath("string(//rt-button[@data-qa='videos-view-all-link']/@href)")
    video_main_href=urljoin(base_url,video_href)
    request_video=re.get(video_main_href,headers=headers)
    tree3 = html.fromstring(request_video.text)
    videos = []

    videos_xpath = tree3.xpath("//div[@data-qa='video-item']")

    for v in videos_xpath:
        title = v.xpath(".//a[@data-qa='video-item-title']/text()")
        link = v.xpath(".//a[@data-qa='video-item-title']/@href")
        duration = v.xpath(".//span[@data-qa='video-item-duration']/text()")
        thumbnail = v.xpath(".//img[@data-qa='video-img']/@srcset")

        videos.append({
            "title": title[0].strip() if title else None,
            "url": urljoin(base_url, link[0]) if link else None,
            "duration": duration[0].strip() if duration else None,
            "thumbnail": thumbnail[0] if thumbnail else None
        })
    all_reviews=[]
    reviews_href = tree.xpath("string(//section[@aria-labelledby='critics-reviews-label']//rt-button/@href)").strip()
    if reviews_href:
        reviews = re.get(urljoin(base_url,reviews_href),headers=headers)
        review_tree = html.fromstring(reviews.text)
        json_obj =review_tree.xpath("//script[@data-json='props']/text()")
        if not json_obj:
            print('No data')
            return
        json_obj_2 = json.loads(json_obj[0])

        page_id = json_obj_2.get('media').get('emsId')
        
        review_url= f'https://www.rottentomatoes.com/napi/rtcf/v1/movies/{page_id}/reviews?after=&before=&pageCount=20&topOnly=false&type=critic&verified=false'

        review_data = find_url(review_url)

        for i in (review_data.get('reviews')) or [] :
            all_reviews.append(
                {
                    'name': (i.get('critic') or {}).get('displayName'),
                    'review': i.get('reviewQuote'),
                    'count': i.get('originalScore'),
                    'review_type': i.get('scoreSentiment')
                }
                )
    data = {
    'movie_name':movie_name,
    'score':tometometer,
    'desc':description,
    'img':img,
    'reviews_count':review_count,
    'videos':videos,
    'want_to_know':whattoknow,
    'cast':cast_and_crew,
    'all_reviews':all_reviews,
        }
    print(f"{data.get('movie_name')} was added.")
    return data

create_db()    
all_url = main("https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest")
for i in all_url:
    data = (get_movie_data(i))
    with open("output_movie.json","w",encoding="utf-8") as f:
        json.dump(data,f)
    break

# with ThreadPoolExecutor(max_workers=5) as e:
#     result = e.map(get_movie_data,all_url)
#     conn,cur = connction()
#     for r in result:
#         if not r:
#             continue
#         cur.execute('''
#         insert into movies(movie_name,score,description,img,reviews_count,videos,want_to_know,cast_and_crew,all_reviews) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
#         ''',(
#         r.get('movie_name'),
#         r.get('score'),
#         r.get('desc'),
#         r.get('img'),
#         r.get('reviews_count'),
#         json.dumps(r.get('videos')),
#         r.get('want_to_know'),
#         json.dumps(r.get('cast')),
#         json.dumps(r.get('all_reviews'))

#         )) 
#     conn.commit()
    
# print("all done")
# conn.close()


