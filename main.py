from categories import get_categories
from products import get_products
from variant_api import get_variants
from db import create_product_urls_table,  create_products_table, get_pending_urls, insert_product, update_status

# CREATE TABLES
create_product_urls_table()
create_products_table()

# GET CATEGORIES
categories = get_categories()
print(f"TOTAL CATEGORIES : {len(categories)}")

# STORE PRODUCT URLS
for category in categories:
    print(f"\nCATEGORY : {category}")
    products = get_products(category)
    print(f"TOTAL PRODUCTS : {len(products)}")

# SCRAPE VARIANTS
pending_urls = get_pending_urls()
print(f"\nTOTAL PENDING URLS : {len(pending_urls)}")
for product_url in pending_urls:
    try:
        print(f"\nPRODUCT : {product_url}")
        variants = get_variants(product_url)
        for item in variants:
            insert_product(item)
        update_status(product_url, "done")
        print("DONE")

    except Exception as e:
        update_status(product_url, "error")
        print("ERROR :", e)