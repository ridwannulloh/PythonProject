import requests
from bs4 import BeautifulSoup

html_doc = requests.get('https://www.detik.com/terpopuler?', params={'tag_from': 'wp_cb_mostPopular_more'})

soup = BeautifulSoup(html_doc.text, 'html.parser')
popular_area = soup.find(attrs={'class': "grid-row list-content"})

# titles = popular_area.find_all(attrs={'class': 'media__title'})
images = popular_area.find_all(attrs={'class': 'media__image'})

for image in images:
    print(f"Judul -- > {image.find('a').find('img')['title']}")
    print(f"Link -- > {image.find('a')['href']}")
    print(f"Image -- > {image.find('a').find('img')['src']}")
    print('-' * 20)
