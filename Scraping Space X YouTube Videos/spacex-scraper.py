import requests
from bs4 import BeautifulSoup

url = 'https://www.youtube.com/SpaceX/videos'
response = requests.get(url).text

soup = BeautifulSoup(response, 'lxml')
div_s = soup.findAll('div')
print(div_s)
