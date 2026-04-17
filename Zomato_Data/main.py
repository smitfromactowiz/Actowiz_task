import json


with open("Zomato_Data/data-2026216105652.json", "r", encoding="utf-8") as f:
    data = json.load(f)

output = []

restaurant_id = data.get("page_data").get("sections").get("SECTION_BASIC_INFO").get("res_id")

restaurant_name = data.get("page_data").get("sections").get("SECTION_BASIC_INFO").get("name")

restaurant_url = data.get("page_info").get("canonicalUrl")

restaurant_contact = [data.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("phoneDetails").get("phoneStr")]

fssai_licence_number = None

location = {
    "full_address": data.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("address"),
    "region":data.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("country_name"),
    "city": data.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("city_name"),
    "pincode": data.get("page_data").get("sections").get("SECTION_RES_CONTACT").get("zipcode"),
    "state": ""
}

cuisines = []


for i in data.get("page_data").get("sections").get("SECTION_RES_HEADER_DETAILS").get("CUISINES", []):
    cuisines.append({"name":i.get("name"),
                     "url":i.get("url")})
    

opening_hours = data.get("page_data").get("sections").get("SECTION_BASIC_INFO").get("timing").get("customised_timings").get('opening_hours')


timings = {
    "monday": {"open": None, "close": None},
    "tuesday": {"open": None, "close": None},
    "wednesday": {"open": None, "close": None},
    "thursday": {"open": None, "close": None},
    "friday": {"open": None, "close": None},
    "saturday": {"open": None, "close": None},
    "sunday": {"open": None, "close": None}
}

if opening_hours:
    for entry in opening_hours:
        timing_str = entry.get("timing", "").lower().replace("–", "-").strip()
        days_str = entry.get("days", "")

        # Split time range
        parts = timing_str.split("-")
        if len(parts) == 2:
            open_time = parts[0].strip()
            close_time = parts[1].strip()
        else:
            open_time, close_time = None, None

        days_list = [
            "monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"
        ]

        for day in days_list:
            timings[day] = {
                "open": open_time,
                "close": close_time
            }



menu_categories = []

menus = data.get("page_data", {}).get("order", {}).get("menuList", {}).get("menus", [])

for menu in menus:
    categories = menu.get("menu", {}).get("categories", [])

    for category in categories:
        category_name = category.get("category").get("name")
        if category_name == "":
            category_name = menu.get("menu").get("name")

        category_obj = {
            "category_name": category_name,
            "items": []
        }

        items = category.get("category", {}).get("items", [])

        for item in items:
            item_data = item.get("item", {})

            dietary = item_data.get("tag_slugs", [])

            item_obj = {
                "item_id": item_data.get("id"),
                "item_name": item_data.get("name"),
                "item_slugs": dietary if dietary else [],
                "item_url": None,
                "item_description": item_data.get("desc"),
                "item_price": float(item_data.get("price")) if item_data.get("price") else None,
                "is_veg": True if "veg" in dietary else False
            }

            category_obj["items"].append(item_obj)

        menu_categories.append(category_obj)



output = {
    "restaurant_id": restaurant_id,
    "restaurant_name": restaurant_name,
    "restaurant_url": restaurant_url,
    "restaurant_contact": restaurant_contact,
    "fssai_licence_number": fssai_licence_number,
    "address_info": location,
    "cuisines": cuisines,
    "timings": timings,
    "menu_categories": menu_categories
}


with open("output_zomato1.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

