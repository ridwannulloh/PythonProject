'''
    Workflow
        1. Login
        2. Collecting Data for Each Page
        3. Getting All Product URL
        4. Merging JSON Results and Create CSV or XLSX
'''

import glob
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd


session = requests.Session()


def login():
    print('Login ....')
    datas = {
        'username': 'user',
        'password': 'user12345'
    }
    res = session.post('http://167.172.70.208:9999/login', data=datas)

    soup = BeautifulSoup(res.text, 'html5lib')

    page_item = soup.find_all('li', attrs={'class': 'page-item'})
    total_pages = len(page_item) - 2
    return total_pages


def get_url(page):
    print('getting url .... page {}'.format(page))
    params = {
        'page': page
    }

    res = session.get('http://167.172.70.208:9999', params=params)

    soup = BeautifulSoup(res.text, 'html5lib')

    title = soup.find_all('h4', attrs={'class': 'card-title'})
    urls = []
    for title in titles:
        url = title.find('a')['href']
        urls.append(url)

    return urls


def get_detail(url):
    print('getting detail .... {}'.format(url))
    res = session.get('http://167.172.70.208:9999' + url)

    soup = BeautifulSoup(res.text, 'html5lib')
    title = soup.find('title').text.strip()
    price = soup.find('h4', attrs={'class': 'card-price'}).text.strip()
    stock = soup.find('span', attrs={'class': 'card-stock'}).text.strip().replace('stock: ', '')
    category = soup.find('span', attrs={'class': 'card-category'}).text.strip().replace('category: ', '')
    description = soup.find('p', attrs={'class': 'card-text'}).text.strip().replace('description: ', ''

    dict_data = {
        'Title': title,
        'Price': price,
        'Stock': stock,
        'Category': category,
        'Description': description
    }

    with open('./results/{}.json'.format(url.replace('/', '')), 'w') as outfile:
        json.dump(dict_data, outfile)


def create_csv():
    files = sorted(glob.glob('results/*.json'))

    datas = []
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)
    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)

    print('csv generated')


def run():
    total_pages = login()
    
    options = int(input('Input option number:\n1. Collecting All Urls\n2. Get Detail All Products\n3. Create CSV\n Whice one ? '))

    if options == 1:
        total_url = []
        for i in range(total_pages):
            page = i + 1
            urls = get_url(page)
            total_url += urls
        with open('all_urls.json', 'w') as outfile:
            json.dumps(total_url, outfile)

    elif options == 2:
        with open('all_urls.json') as json_file:
            all_url = json.load(json_file)

        for url in all_url:
            get_detail(url)
    else:
        create_csv()

if __name__ == '__main__':
    run()
