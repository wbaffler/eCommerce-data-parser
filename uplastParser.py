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
products_arr = []
FILENAME = 'data_uplast.csv'
input_arr = []
filename_input = 'input_uplast.txt'
URL_ACC = 'https://u-plast.by/katalog/aksessuary'

def parse_input():
    with open(filename_input) as file:
        input_arr = file.readlines()
        input_arr = [line.rstrip() for line in input_arr]
    return input_arr

def parse_product_page(url_full):
    r = requests.get(url_full, headers=headers)
    soup = bs(r.text, "html.parser")
    names = soup.find('div', class_='product-gallery-slider-big').find_all('div', class_='slider-nav__item')

    for n in names:
        name = n.find('p', class_='variation-title').find_all('span')[0].text
        id = soup.find('p', class_='variation-title').find_all('span')[1].text

        #specs = ''
        if soup.find('div', class_='d-flex flex-row flex-wrap row-cols-2'):
            specs_table = soup.find('div', class_='d-flex flex-row flex-wrap row-cols-2').find_all('div')
            specs = dict()
            for s in range(len(specs_table))[::2]:
                if s+1 != len(specs_table):
                    specs[specs_table[s].text] = specs_table[s+1].text
        elif soup.find('div', class_='woocommerce-Tabs-panel'):
            specs_table = soup.find('div', class_='woocommerce-Tabs-panel').find_all('p')
            specs = dict()
            for s in range(len(specs_table))[::2]:
                specs[specs_table[s].text] = specs_table[s + 1].text

        image = soup.find('div', class_='product-gallery-slider').find('a').get('href')

        about = ''
        if soup.find('div', class_='product-seo-block__content'):
            about = soup.find('div', class_='product-seo-block__content').text

        img_about = []
        if soup.find('div', class_='product-example-gallery__body'):
            imgs_temp = soup.find('div', class_='product-example-gallery__body').find_all('a')
            for i in imgs_temp:
                img_about.append(i.get('href'))

        options = []

        benefits = []

        documents_div = soup.find('div', class_='woocommerce-Tabs-panel woocommerce-Tabs-panel--file_tab').find_all('a')
        documents = []
        for d in documents_div:
            documents.append(d.get('href'))

        price = ''
        price_b = ''


        group_name = soup.find('h1', class_='product_title').text
        category_name = soup.find('nav', class_='woocommerce-breadcrumb').find_all('a')[2].text

        products_arr.append([id, name, specs, image, about, img_about, options, benefits, documents, price, price_b, category_name, group_name])

def parse_categories(url):
    r = requests.get(url, headers=headers)
    soup = bs(r.text, "html.parser")
    category_urls_li = soup.find_all('li', class_='product-category')
    category_urls = []
    groups_urls = []
    for c in category_urls_li:
        category_url = c.find('a').get('href')
        r_g = requests.get(category_url, headers=headers)
        soup_g = bs(r_g.text, "html.parser")
        groups_urls_li = soup_g.find_all('li', class_='product')
        for g in groups_urls_li:
            groups_urls.append(g.find('a').get('href'))
    return groups_urls


if __name__ == '__main__':

    for p in parse_input():
        print(p)
        parse_product_page(p)

    for p in parse_categories(URL_ACC):
        print(p)
        parse_product_page(p)

    write_in_file(FILENAME, products_arr)
