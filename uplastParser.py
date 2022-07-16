import requests
from bs4 import BeautifulSoup as bs
from Form_CSV import write_in_file
from headers import headers
products_arr = []
FILENAME = 'data_uplast_newlinks.csv'
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
            new_specs_table = '<table class="table table-striped table-condensed" <tbody>>'
            specs = dict()
            for s in range(len(specs_table))[::2]:
                if s+1 != len(specs_table):
                    new_specs_table += '<tr> <td>' + specs_table[s].text + '</td> <td>' + specs_table[s+1].text + '</td> </tr>'
                    specs[specs_table[s].text] = specs_table[s+1].text
        elif soup.find('div', class_='woocommerce-Tabs-panel'):
            specs_table = soup.find('div', class_='woocommerce-Tabs-panel').find_all('p')
            new_specs_table = '<table class="table table-striped table-condensed" <tbody>>'
            specs = dict()
            for s in range(len(specs_table))[::2]:
                new_specs_table += '<tr> <td>' + specs_table[s].text + '</td> <td>' + specs_table[
                    s + 1].text + '</td> </tr>'
                specs[specs_table[s].text] = specs_table[s + 1].text
        new_specs_table += '</table> </tbody>'

        image_url = n.find('a').get('href')
        image = "avg_" + n.find('a').get('href').rsplit('/')[-1]

        about = ''
        if soup.find('div', class_='product-seo-block__content'):
            about = soup.find('div', class_='product-seo-block__content')

            for x in about.select('a'):
                x.decompose()

        img_about_url = []
        img_about = image + ' | '
        #img_about.append(image)
        if soup.find('div', class_='product-example-gallery__body'):
            imgs_temp = soup.find('div', class_='product-example-gallery__body').find_all('a')
            for i in imgs_temp:
                img_about += "avg_" + i.get('href').rsplit('/')[-1] + '|'
                #img_about.append(i.get('href').rsplit('/')[-1])

        options = []

        benefits = []

        documents_div = soup.find('div', class_='woocommerce-Tabs-panel woocommerce-Tabs-panel--file_tab').find_all('a')
        documents = ''
        for d in documents_div:
            documents += d.get('href') + '|'
            #documents.append(d.get('href'))

        price = ''
        price_b = ''


        group_name = soup.find('h1', class_='product_title').text
        category_name = soup.find('nav', class_='woocommerce-breadcrumb').find_all('a')[2].text

        products_arr.append([id, name, new_specs_table, image, about, img_about, options, benefits, documents, price, price_b, category_name, group_name])

def parse_product_general(url_full):
    r = requests.get(url_full, headers=headers)
    soup = bs(r.text, "html.parser")
    name = soup.find('h1', class_='product_title').text
    print(name)

    if soup.find('div', class_='d-flex flex-row flex-wrap row-cols-2'):
        specs_table = soup.find('div', class_='d-flex flex-row flex-wrap row-cols-2').find_all('div')
        new_specs_table = '<table class="table table-striped table-condensed" <tbody>>'
        specs = dict()
        for s in range(len(specs_table))[::2]:
            if s+1 != len(specs_table):
                new_specs_table += '<tr> <td>' + specs_table[s].text + '</td> <td>' + specs_table[s+1].text + '</td> </tr>'
                specs[specs_table[s].text] = specs_table[s+1].text
    elif soup.find('div', class_='woocommerce-Tabs-panel'):
        specs_table = soup.find('div', class_='woocommerce-Tabs-panel').find_all('p')
        new_specs_table = '<table class="table table-striped table-condensed" <tbody>>'
        specs = dict()
        for s in range(len(specs_table))[::2]:
            new_specs_table += '<tr> <td>' + specs_table[s].text + '</td> <td>' + specs_table[
                s + 1].text + '</td> </tr>'
            specs[specs_table[s].text] = specs_table[s + 1].text
    new_specs_table += '</table> </tbody>'

    img_about = ''
    for n in soup.find('div', class_='product-gallery-slider-big').find_all('div', class_='slider-nav__item'):
        image_url = n.find('a').get('href')
        image = n.find('a').get('href').rsplit('/')[-1]
        img_about += image + ' | '

    about = ''
    if soup.find('div', class_='product-seo-block__content'):
        about = soup.find('div', class_='product-seo-block__content')

        for x in about.select('a'):
            x.decompose()

    img_about_url = []
    #img_about.append(image)
    if soup.find('div', class_='product-example-gallery__body'):
        imgs_temp = soup.find('div', class_='product-example-gallery__body').find_all('a')
        for i in imgs_temp:
            img_about += i.get('href').rsplit('/')[-1] + '|'
            #img_about.append(i.get('href').rsplit('/')[-1])

    options = []

    benefits = []

    documents_div = soup.find('div', class_='woocommerce-Tabs-panel woocommerce-Tabs-panel--file_tab').find_all('a')
    documents = ''
    for d in documents_div:
        documents += d.get('href') + '|'
        #documents.append(d.get('href'))

    price = ''
    price_b = ''

    group_name = soup.find('h1', class_='product_title').text
    category_name = soup.find('nav', class_='woocommerce-breadcrumb').find_all('a')[2].text

    connected_names = soup.find('div', class_='product-gallery-slider-big').find_all('div', class_='slider-nav__item')
    atribute = ''
    for n in connected_names:
        name_tmp = n.find('p', class_='variation-title').find_all('span')[0].text
        atribute += name_tmp + ' | '

    products_arr.append([id, name, new_specs_table, image, about, img_about, options, benefits, documents, price, price_b, category_name, group_name, atribute])


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
