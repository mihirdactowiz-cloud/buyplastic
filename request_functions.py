import requests
from request_data import cookies, headers

def get_page(url):
    response = requests.get(
        url,
        cookies=cookies,
        headers=headers
    )
    return response