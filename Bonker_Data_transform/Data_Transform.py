import json


with open("C:\\Users\smit.panchal\Downloads\\bonker.json", "r", encoding="utf-8") as f:
    data = json.load(f)

BASE_URL = "https://www.bonkerscorner.com/products/"

output = []


for product in data["products"]:
    handle = product.get("handle")
    product_url = BASE_URL + handle


    first_variant = product["variants"][0]
    full_name = first_variant.get("name")
    product_name = full_name.split(" - ")[0]

    vendor = product.get("vendor")


    product_price = int(first_variant.get("price")) / 100

    # Extract variant options (Size)
    sizes = []
    variants_list = []

    for v in product.get("variants", []):
        variant_id = v.get("id")
        variant_price = int(v.get("price")) / 100
        variant_name = v.get("public_title")  # XS, S, M...

        sizes.append(variant_name)

        variants_list.append({
            "variantName": variant_name,
            "variantId": variant_id,
            "variantUrl": f"{product_url}?variant={variant_id}",
            "variantPrice": variant_price
        })

    output.append({
        "productName": product_name,
        "vendor": vendor,
        "productUrl": product_url,
        "productPrice": product_price,
        "variantCount": len(variants_list),
        "variantOptions": [
            {
                "optionName": "Size",
                "optionValues": sizes
            }
        ],
        "variants": variants_list
    })


with open("output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("✅ Done! Output saved in output.json")