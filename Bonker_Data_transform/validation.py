from pydantic import BaseModel
from typing import List


class Variant(BaseModel):
    variantName: str
    variantId: int
    variantUrl: str
    variantPrice: float


class VariantOption(BaseModel):
    optionName: str
    optionValues: List[str]


class Product(BaseModel):
    productName: str
    vendor: str
    productUrl: str
    productPrice: float
    variantCount: int
    variantOptions: List[VariantOption]
    variants: List[Variant]


import json

with open("output.json") as f:
    data = json.load(f)

validated_products = []

for item in data:
    product = Product(**item)  # 🔥 validation happens here
    validated_products.append(product)

print(validated_products)

print("✅ All data is valid!")