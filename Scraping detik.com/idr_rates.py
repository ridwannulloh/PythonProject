import requests

json_data = requests.get('http://www.floatrates.com/daily/idr.json')

json_data = {"usd":{"code":"USD","alphaCode":"USD","numericCode":"840","name":"U.S. Dollar","rate":7.12392528532e-5,"date":"Fri, 1 Jan 2021 12:00:02 GMT","inverseRate":14037.205051275},"eur":{"code":"EUR","alphaCode":"EUR","numericCode":"978","name":"Euro","rate":5.8106697591367e-5,"date":"Fri, 1 Jan 2021 12:00:02 GMT","inverseRate":17209.720074482}}

for data in json_data.values():
    print(data['code'])
    print(data['name'])
    print(data['date'])
    print(data['inverseRate'])
    print('\n')