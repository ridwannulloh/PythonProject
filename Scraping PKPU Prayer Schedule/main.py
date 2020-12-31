from bs4 import BeautifulSoup
import requests

def PSToday(type):
    url = 'https://jadwalsholat.pkpu.or.id/?id=308'
    contents = requests.get(url)

    response = BeautifulSoup(contents.text, 'html.parser')
    data = response.find_all('tr', 'table_highlight')
    data = (data[0])

    sholat ={}
    i = 0
    for d in data:
        if i == 1:
            sholat['Subuh'] = d.get_text()
        if i == 2:
            sholat['Dzuhur'] = d.get_text()
        if i == 3:
            sholat['Ashar'] = d.get_text()
        if i == 4:
            sholat['Magrib'] = d.get_text()
        if i == 5:
            sholat['Isya'] = d.get_text()
        i += 1

    print(f'The today schedule of {type} is at {sholat[type]}')

PSToday('Isya')