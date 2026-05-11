import requests
import json
from lxml import html
from request_functions import get_page
from functions import write_html_direct_gzip, make_hash


GRAPHQL_URL = "https://buyplastic.com/graphql"

cookies = {
    'SF-CSRF-TOKEN': '10e420aa-d1da-4326-a6b6-d48d0d4a3ebf',
    'fornax_anonymousId': '8d365b34-ec4f-479e-8a22-3a6a51b084de',
    'athena_short_visit_id': '251c03bc-b5ec-45cc-b765-360ecb64736f:1778227210',
    'SHOP_SESSION_TOKEN': 'a23dec40-a05d-4c05-a9fb-0a74d5facd30',
    '_fbp': 'fb.1.1778227212823.247910779913608605',
    '__kla_id': 'eyJjaWQiOiJaRFV5WVdJMFkyRXRNamt3WlMwMFpqSmxMVGd6WVdZdFptSXdZVGRpTldFek9USXkifQ==',
    'XSRF-TOKEN': '3a4dcc817c154565f63f124622083d9b8f35c8c30ca903dcb5108ead77f62a21',
    '_ga': 'GA1.1.343712121.1778227214',
    '_gcl_au': '1.1.896234917.1778227214',
    '_clck': '14u04py%5E2%5Eg5v%5E0%5E2319',
    'lastVisitedCategory': '33',
    'STORE_VISITOR': '1',
    '__cf_bm': 'AHYjSmG9JXML9tQpxalj0WdfBrXYt0ovV_g1I7KCAXU-1778228143.3789158-1.0.1.1-vqqnCqHH3GVewQtw.yFy4IP7CIkGcZ3RAonEgLSjXYjK3ovGtLc6k5N_qO3sSwIUEoMFSjDTsZrd_B6QTAh6nRMy2rfDQfPcKUUuIQ1BU_0JOtY6h7f859NZ1xrkU3hL',
    '_uetsid': 'f1bc03d04ab311f18cd027ad453c3199',
    '_uetvid': 'f1bc37204ab311f19f4525a00ca3925e',
    '_clsk': 'bxrp5u%5E1778228912466%5E12%5E1%5El.clarity.ms%2Fcollect',
    'Shopper-Pref': '79FA5DA42E4446611CFBCE72D49EB70AE4EB4CD1-1778833716224-x%7B%22cur%22%3A%22USD%22%2C%22funcConsent%22%3Atrue%7D',
    '_ga_50BLGJTDSB': 'GS2.1.s1778227213$o1$g1$t1778228916$j42$l0$h181293919',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://buyplastic.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://buyplastic.com/king-starboard-wg-woodgrain-hdpe-plastic-sheet/',
    'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-sf-csrf-token': '10e420aa-d1da-4326-a6b6-d48d0d4a3ebf',
    'x-xsrf-token': '3a4dcc817c154565f63f124622083d9b8f35c8c30ca903dcb5108ead77f62a21',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJjaWQiOlsxXSwiY29ycyI6WyJodHRwczovL2J1eXBsYXN0aWMuY29tIl0sImVhdCI6MTc3ODMzMzM2NiwiaWF0IjoxNzc4MTYwNTY2LCJpc3MiOiJCQyIsInNpZCI6MTAwMTA1ODIzOSwic3ViIjoiQkMiLCJzdWJfdHlwZSI6MCwidG9rZW5fdHlwZSI6MX0.PhHMHZiDEwF37Ohd4o6DC0sLlzTOg2hG-yX3HfXdgy1aI0Iynf9EyMiiBR5Px8_Q-oJczyJIJY0SlvXZ9vohBA'
}

def get_product_id(product_url):
    response = get_page(product_url)
    data = response.text
    filename = make_hash(product_url)
    write_html_direct_gzip(data, filename)
    tree = html.fromstring(data)
    product_id = tree.xpath('//input[@name="product_id"]/@value')
    if not product_id:
        return None
    return product_id[0]

def get_variants(product_url):
    product_id = get_product_id(product_url)
    if not product_id:
        return []
    all_variants = []
    cursor = None
    while True:
        after_part = ""
        if cursor:
            after_part = f', after:"{cursor}"'
        query = f"""
        query Products{{
          site{{
            product(entityId:{product_id}){{
              entityId
              name
              path
              variants(first:50 {after_part}){{
                pageInfo{{
                  hasNextPage
                  endCursor
                }}

                edges{{

                  node{{

                    entityId

                    sku

                    prices{{
                      price{{
                        value
                      }}
                    }}

                    inventory{{
                      isInStock
                    }}

                    productOptions{{

                      edges{{

                        node{{

                          entityId

                          displayName

                          ... on MultipleChoiceOption{{

                            values{{

                              edges{{

                                node{{

                                  entityId
                                  label
                                }}
                              }}
                            }}
                          }}
                        }}
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        response = requests.post(
            GRAPHQL_URL,
            headers=headers,
            cookies=cookies,
            json={"query": query}
        )

        data = response.json()
        
        site_data = data.get("data", {}).get("site", {})
        product = site_data.get("product")

        if not product:
            print("Product data not found in response:", response.text)
            return []

        variants = product.get("variants", {})
        edges = variants.get("edges", [])

        for edge in edges:
            node = edge.get("node", {})
            variant_json = {}
            
            product_options = node.get("productOptions", {}).get("edges", [])
            for option_edge in product_options:
                option_node = option_edge.get("node", {})
                option_name = option_node.get("displayName")

                if "values" not in option_node:
                    continue

                values_edges = option_node.get("values", {}).get("edges", [])
                labels = []
                for value in values_edges:
                    value_node = value.get("node", {})
                    labels.append({
                        "value_id": value_node.get("entityId"),
                        "label": value_node.get("label")
                    })

                variant_json[option_name] = labels
            
            price_val = node.get("prices", {}).get("price", {}).get("value")
            stock_status = node.get("inventory", {}).get("isInStock")

            final_data = {
                "product_name": product.get("name"),
                "product_url": product_url,
                "product_entity_id": product.get("entityId"),
                "variant_entity_id": node.get("entityId"),
                "sku": node.get("sku"),
                "price": price_val,
                "stock": stock_status,
                "variants": variant_json
            }

            all_variants.append(final_data)

        page_info = variants.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break

        cursor = page_info.get("endCursor")
    return all_variants