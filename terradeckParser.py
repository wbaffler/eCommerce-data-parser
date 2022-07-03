import requests
from bs4 import BeautifulSoup as bs
from Form_CSV import write_in_file


headers = {
    'authority': 'www.terradeck.ru',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en-US,en;q=0.9',
}

url_terradeck = 'https://www.terradeck.ru'
data_matrix = []
FILENAME = 'data_terradeck4.csv'

def find_categories():
    url = 'https://www.terradeck.ru/catalog/'
    r = requests.get(url, headers=headers)
    print(r.status_code)

    soup = bs(r.text, "html.parser")
    categories = soup.find_all('div', class_='item')

    category_arr = []
    for category in categories:
        category_h5 = category.find('h5')
        if category_h5:
            category_name = category_h5.text.replace('\t', '').replace('\n', '')
            categury_url = category_h5.find('a').get('href')
            category_arr.append([category_name, categury_url])
    #print(category_names)
    #print(categury_urls)
    return category_arr

def parse_category(url, category_name):
    url_full = 'https://www.terradeck.ru' + url
    r = requests.get(url_full, headers=headers)

    product_urls = []
    index_page = 0
    status = 200

    while status == 200:
        status = 404
        url_full = 'https://www.terradeck.ru' + url + '?page=' + str(index_page)
        r = requests.get(url_full, headers=headers)

        soup = bs(r.text, "html.parser")
        if soup.find('ul', class_='ul-goods ul-goods-tree'):
            products = soup.find('ul', class_='ul-goods ul-goods-tree').find_all('li')

            for product in products:
                product_url = product.find('a').get('href')
                product_urls.append(product_url)
                status = 200
            index_page += 1


    for p in product_urls:
        arr = parse_product(p, product_urls)
        arr.append(category_name)
        data_matrix.append(arr)

    print(product_urls)





def parse_product(product_url, product_urls):
    url_full = 'https://www.terradeck.ru' + product_url
    print(url_full)

    r = requests.get(url_full, headers=headers)
    soup = bs(r.text, "html.parser")

    name = soup.find('div', class_='top-goods').find('h1').text.replace('\t', '').replace('\n', '')

    specs_table = soup.find('table', class_='table-characteristic').find_all('tr')
    specs = dict()
    for s in specs_table:
        specs[s.find_all('span')[0].text.replace('\t', '').replace('\n', '')] = s.find_all('span')[1].text.replace('\t', '').replace('\n', '')

    image = soup.find('div', class_='big-slider').find('img').get('src')

    about_div = soup.find('div', class_='textContainer_Truncate')
    about = about_div.find('p').text
    img_about = ''
    if about_div.find('img'):
        img_about = url_terradeck + about_div.find('img').get('src')

    option_selector_div = soup.find('div', class_='mobile-select-line')
    options = []
    if option_selector_div:
        options_l = option_selector_div.find_all('label', class_='select-line')
        for o in options_l:
            options.append(o.text)
        option_selector = dict()
        option_selector[option_selector_div.find('div', class_='title').text] = options

    benefits_div = soup.find('div', class_='benefist-items').find_all('div', class_='item')
    benefits = []
    for b in benefits_div:
        benefits.append(b.text.replace('\t', '').replace('\n', ''))

    documents_div = soup.find('div', class_='link-download').find_all('div', class_='item')
    documents = []
    for d in documents_div:
        documents.append(d.find('a').get('href'))

    price = soup.find('div', class_='price').text.replace('\t', '').replace('\n', '').replace('р./м2', '').replace(' ', '')
    if soup.find('div', class_='price-b'):
        price_b = soup.find('div', class_='price-b').find('b').text.replace('\t', '').replace('\n', '').replace(' ', '').replace('р.', '')
    else:
        price_b = ''

    hidden_products_all = soup.find_all('div', class_='left-slider')
    if len(hidden_products_all) > 1:
        hidden_products = hidden_products_all[1].find_all('div', class_='item')
        for hp in hidden_products:
            new_product = hp.find('a').get('href')
            if new_product not in product_urls:
                product_urls.append(new_product)


    return [name, specs, image, about, img_about, options, benefits, documents, price, price_b]



if __name__ == '__main__':
    categories = find_categories()
    for c in categories:
        parse_category(c[1], c[0])
    write_in_file(FILENAME, data_matrix)