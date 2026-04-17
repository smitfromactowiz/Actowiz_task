from pydantic import BaseModel
from typing import List, Optional


class Item(BaseModel):
    item_id: Optional[str]
    item_name: Optional[str]
    item_slugs: List[str] = []
    item_url: Optional[str]
    item_description: Optional[str]
    item_price: Optional[float]
    is_veg: bool


class MenuCategory(BaseModel):
    category_name: Optional[str]
    items: List[Item]


class AddressInfo(BaseModel):
    full_address: Optional[str]
    region: Optional[str]
    city: Optional[str]
    pincode: Optional[int]
    state: Optional[str]


class Cuisine(BaseModel):
    name: str
    url: Optional[str]


class DayTiming(BaseModel):
    open: Optional[str]
    close: Optional[str]


class Timings(BaseModel):
    monday: DayTiming
    tuesday: DayTiming
    wednesday: DayTiming
    thursday: DayTiming
    friday: DayTiming
    saturday: DayTiming
    sunday: DayTiming


class Restaurant(BaseModel):
    restaurant_id: Optional[int]
    restaurant_name: Optional[str]
    restaurant_url: Optional[str]
    restaurant_contact: List[str] = []
    fssai_licence_number: Optional[str]
    address_info: AddressInfo
    cuisines: List[Cuisine]
    timings: Timings
    menu_categories: List[MenuCategory]

import json
import json

with open("output_zomato1.json", "r", encoding="utf-8") as f:
    data = json.load(f)   # ✅ THIS is dict



    
product = Restaurant(**data)  # 🔥 validation happens here


print("✅ All data is valid!")