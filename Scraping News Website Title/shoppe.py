from bs4 import BeautifulSoup

search_keyword = str(input('Masukkan kata kunci yang ingin dicari '))

url = f'https://shopee.co.id/search?keyword=jeans{search_keyword}'
html_doc = response.get(url)

soup = BeautifulSoup(html_doc.text, parser='lxml.parser')

print(soup)
