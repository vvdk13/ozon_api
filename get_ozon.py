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
    import csv
    pr = json.loads(products_json)
    lines = []

    for item in pr['items']:
        name = str(item['name']),
        offer_id = str(item['offer_id'])
        marketing_price = float(item['marketing_price'] if item['marketing_price'] != '' else 0)
        min_price = float(item['min_price'] if item['min_price'] != '' else 0)
        price = float(item['price'])
        old_price = float(item['old_price'] if item['old_price'] != '' else 0)
        ozon_commissions = round(float(item['commissions'][1]['value']))
        last_mile = item['commissions'][1]['delivery_amount']
        drop_off = 30
        delivery = item['commissions'][1]['return_amount']
        acquiring = round(float(item['price'])*1.9/100)
        total_expenses = ozon_commissions + last_mile + drop_off + delivery + acquiring
        line = [name,
                offer_id,
                marketing_price,
                min_price,
                price,
                old_price,
                ozon_commissions,
                last_mile,
                drop_off,
                delivery,
                acquiring,
                total_expenses
            ]
        lines.append(line)
        lines.sort(key=lambda x: x[1])
    print(lines)
    header = ['Name',
              'offer_id',
              'marketing_price',
              'min_price',
              'price',
              'old_price',
              'ozon commission',
              'last mile',
              'Drop off',
              'delivery',
              'Acquiring',
              'Total expenses'
              ]
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(lines)