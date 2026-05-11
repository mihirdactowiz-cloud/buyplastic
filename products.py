from lxml import html
from request_functions import get_page
from db import insert_product_url

def get_products(category_url):
    response = get_page(category_url)
    data = response.text
    tree = html.fromstring(data)
    product_urls = tree.xpath("//a[@class='card-figure__link']/@href")
    product_urls = list(dict.fromkeys(product_urls))
    final_urls = []
    for url in product_urls:
        if not url.startswith("http"):
            url = "https://buyplastic.com" + url
        final_urls.append(url)
        insert_product_url(url)
        print("INSERTED :", url)
    return final_urls 