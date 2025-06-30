import sys
import requests
import json
import config

def get_products_list():
    url = "https://api-seller.ozon.ru/v3/product/list"
    payload = json.dumps({
        "filter": {
            "visibility": "ALL"
        },
        "last_id": "",
        "limit": 1000
    })
    headers = {
        'Api-Key': config.API_KEY,
        'Content-Type': 'application/json',
        'Client-Id': config.Client_Id,
        'Cookie': 'abt_data=7.2EiQzJYcsK07fI1wMZhwCeVE00jM_-3hgTpL8PF2F2gDudx1fImdOzd51xOSDT9qR0Z7ZymkqYFAp1gRYE6QCZja8hDDwzFOty1_OnmffHZD-y2bRSNYFMDP9NMGazenfyOWqI31pMtUAWWqVCJS6Cw5RRvf7cT0mgjs6nD34-U9nmxjJxTpVUmXaxofbx5IwCDBm3lG6ItGrDcWWACvShFLAlc3WB81kBi1zYEBcsPnCJNb8pO_ULnVCNb2ZkWO24HQgokXejVJ60A9sTJ9LFBazXtn_dCqNSWU2YSrmRsQ0gHBBDJeutMr9bzgTREUineejj_razhNKnU_daI'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Status code {requests.status_codes}")
            sys.exit()
    except Exception as e:
        print('Error: {e}')

def save_to_file(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception as e:
        print("Error: {e}")

def get_product_ids(data: json) -> list:
    dict_products = json.loads(data)
    dict_products = dict_products['result']['items']
    productIds = []
    for i in dict_products:
        product_id = i['product_id']
        productIds.append(product_id)
    return productIds

def get_product_info(list_of_product: list):
    url = "https://api-seller.ozon.ru/v3/product/info/list"
    product_ids = [str(id) for id in list_of_product]
    payload = json.dumps({
        "product_id": product_ids
    })
    headers = {
        'Api-Key': config.API_KEY,
        'Content-Type': 'application/json',
        'Client-Id': config.Client_Id,
        'Cookie': 'abt_data=7.2EiQzJYcsK07fI1wMZhwCeVE00jM_-3hgTpL8PF2F2gDudx1fImdOzd51xOSDT9qR0Z7ZymkqYFAp1gRYE6QCZja8hDDwzFOty1_OnmffHZD-y2bRSNYFMDP9NMGazenfyOWqI31pMtUAWWqVCJS6Cw5RRvf7cT0mgjs6nD34-U9nmxjJxTpVUmXaxofbx5IwCDBm3lG6ItGrDcWWACvShFLAlc3WB81kBi1zYEBcsPnCJNb8pO_ULnVCNb2ZkWO24HQgokXejVJ60A9sTJ9LFBazXtn_dCqNSWU2YSrmRsQ0gHBBDJeutMr9bzgTREUineejj_razhNKnU_daI'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
    except Exception as e:
        print("Error: {e}")

def get_product_csv(products_json, filename = 'products.csv'):
    pr = json.loads(products_json)
    lines = []

    for item in pr['items']:
        line = [item['name'],
                item['offer_id'],
                float(item['marketing_price']),
                float(item['min_price']),
                float(item['price']),
                item['old_price'],
                item['commissions'][1]['value'],
                item['commissions'][1]['delivery_amount'],
                30, # Обработка отправления
                item['commissions'][1]['return_amount'], #  Доставка
                (float(item['price'])*1.5)/100, # Эквайринг 1.5% от price
                round((float(item['price']) * 1.5) / 100, 2) + item['commissions'][1]['return_amount'] + 30 + item['commissions'][1]['delivery_amount'] + item['commissions'][1]['value']
            ]
        lines.append(line)
    print(lines)