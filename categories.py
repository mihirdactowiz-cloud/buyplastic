from lxml import html
from request_functions import get_page


def get_categories():
    url = "https://buyplastic.com/materials/"
    response = get_page(url)
    data = response.text
    tree = html.fromstring(data)
    links = tree.xpath('//ul[@id="navPages-86"]/li/a/@href')
    links = list(dict.fromkeys(links))
    return links