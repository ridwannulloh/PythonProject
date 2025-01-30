import requests
from bs4 import BeautifulSoup

url = [
    'https://www.detik.com/',
    'https://www.kompas.com/',
    'https://www.viva.co.id/',
    'https://www.kontan.co.id/',
    'https://www.disway.id/',
    'https://republika.co.id/',
    'https://www.cnnindonesia.com/'
]

url_title = {}

for link in url:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, features='html.parser')
    url_title[link] = soup.title.string

for key, value in url_title.items():
    print(f'{key} --> {value}')

