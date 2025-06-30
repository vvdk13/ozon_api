import get_ozon

def main():
    data = get_ozon.get_products_list()
    get_ozon.save_to_file(data, 'product_list.json')
    ids = get_ozon.get_product_ids(data)
    dataset = get_ozon.get_product_info(ids)
    get_ozon.save_to_file(dataset, 'products.json')
    get_ozon.get_product_csv(dataset, 'products.csv')

if __name__ == '__main__':
    main()