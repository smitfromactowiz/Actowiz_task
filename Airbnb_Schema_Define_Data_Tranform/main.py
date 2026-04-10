import json
import jmespath

data = ""
with open("air_bnb.json","r",encoding="utf-8") as f:
    data = json.load(f)

with open("air_bnb2.json","r",encoding="utf-8") as f2:
    data2 = json.load(f2)


StartPart = jmespath.search("niobeClientData[0][1].data.presentation.stayProductDetailPage.sections",data)
niobeClientData = jmespath.search("sbuiData.sectionConfiguration.root",StartPart)
FirstPart = jmespath.search("sections[0].sectionData",niobeClientData)
SecondPart = jmespath.search("sections[1].sectionData",niobeClientData)
ThirdPart = jmespath.search("sections[17].section",StartPart)

title = FirstPart.get("title")
capacityStrList = jmespath.search("overviewItems[*].title",FirstPart)
capacityList = {}
for i in capacityStrList:
    d = i.split(" ")
    temp = {d[1]: int(d[0])}
    capacityList.update(temp)

rating = float(jmespath.search("reviewData.ratingText",FirstPart))
review = int(jmespath.search("reviewData.reviewCountText",FirstPart).split(" ")[0])

profile_name = SecondPart.get("title")
profile_year = jmespath.search("overviewItems[0].title",SecondPart)
profile_url = jmespath.search("hostAvatar.avatarImage.baseUrl",SecondPart)

profile = {
    "profile_name" : profile_name,
    "year_of_expreience" : profile_year,
    "profile_url" : profile_url
}

highlights = jmespath.search("highlights[].{ title: title, subtitle: subtitle}",ThirdPart)

description = jmespath.search("sections[18].section.htmlDescription.htmlText",StartPart).split("<br /><br />")
description = f"{description[0]}\n\n{description[1]}"

firstPart_bnb2 = jmespath.search("data.presentation.stayProductDetailPage.sections.sections[1].section.structuredDisplayPrice.primaryLine",data2)
paymentDetails = {"currency":'INR',"discounted_price":int(firstPart_bnb2.get("discountedPrice")[1:].replace(",","")),"original_price":int(firstPart_bnb2.get("originalPrice")[1:].replace(",","")),"price_type":firstPart_bnb2.get("qualifier")}
hotelname = jmespath.search("sections[21].section.listingTitle",StartPart).split("|")[2].strip()





StartPart1 = jmespath.search("niobeClientData[0][1].data.presentation.stayProductDetailPage.sections.sections[20].section",data)
title = StartPart1.get("title")
seeAllAmenitiesGroups = jmespath.search("seeAllAmenitiesGroups[].{ category : title, amenities : amenities[].title }",StartPart1)

SecondPageData = {
        "amenities" : seeAllAmenitiesGroups
    }




with open("airbnb_review.json","r",encoding="utf-8") as f:
    data3 = json.load(f)

StartPart3 = jmespath.search("data.presentation.stayProductDetailPage.reviews",data3)

reviewsNames = jmespath.search("reviews[].reviewer.firstName",StartPart3)
reviewsDates = jmespath.search("reviews[].localizedDate",StartPart3)
reviewsRating = jmespath.search("reviews[].rating",StartPart3)
reviewsComments = jmespath.search("reviews[].commentV2",StartPart3)

FinalReviews = []

for i in range(len(reviewsNames)) :
    temp = {
        "name" : reviewsNames[i],
        "rating" : reviewsRating[i],
        "date" : reviewsDates[i],
        "Comments" :reviewsComments[i]
    } 
    FinalReviews.append(temp)


StartPart4 = jmespath.search("niobeClientData[0][1].data.presentation.stayProductDetailPage.sections.sections[5].section",data)

name = jmespath.search("cardData.name",StartPart4)
counting = jmespath.search("cardData.stats[].value",StartPart4)
detail = jmespath.search("cardData.stats[].label",StartPart4)

review1 = {}
for i in range(len(counting)):
    if '.' in counting[i]:
        review1[f"{detail[i]}"] = float(counting[i])
    else:
        review1[f"{detail[i]}"] = int(counting[i])

ProfileView = {
    "host_name" : name, 
    "details" : review1
}

Airbnb_data = {
    "restaurant_name" : hotelname,
    "details":{
    "title" : title,
    "capacity" : capacityList,
    "rating" : float(rating),
    "review" : review,
    "profile" : profile,
    "highlights" : highlights,
    "description": description,
   
    },
     "paymentDetails" : paymentDetails,
    "amenities" : seeAllAmenitiesGroups,
    "reviews" : FinalReviews,
    "profileView" : ProfileView

}

with open("Airbnb_data.json","w",encoding="utf-8") as f:
    json.dump(Airbnb_data,f,indent=4)

