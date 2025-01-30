import pandas as pd
import requests
from bs4 import BeautifulSoup

targetccy = ['IDR','USD','EUR']
url = 'https://www.iban.com/currency-codes'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]

listcountry = df['Country'].values.tolist()
listccy = df['Code'].values.tolist()

data = pd.DataFrame(columns = ['country','currency','rates','target'])

for j in range(len(targetccy)):
	target = targetccy[j]

	for i in range(len(listccy)):
		ccy = listccy[i]
		country = listcountry[i]


		if (str(ccy) == 'nan'):
			pass 
		else : 
			URL = "https://www.google.com/finance/quote/{0}-{1}" .format(ccy,target)
			page = requests.get(URL, headers={'Cache-Control': 'no-cache'})
			soup = BeautifulSoup(page.content, "html.parser")
			
			results = soup.find(class_="YMlKec fxKbKc")
			rawdata = str(results).replace(",","")
			rawdata = rawdata.split(">")

			if (str(rawdata[0]) == "None"):
				pass 
			else : 
				rawdata = rawdata[1]
				rawdata = str(rawdata).replace("</div","")
				
				##prepare data
				country = country
				currency = ccy
				rates = rawdata

				data = pd.concat([pd.DataFrame([[country,currency,rates,target]], columns=data.columns), data], ignore_index=True)

data = pd.concat([pd.DataFrame([['Indonesia','IDR','1','IDR']], columns=data.columns), data], ignore_index=True)
data = pd.concat([pd.DataFrame([['United States Of America (The)','USD','1','USD']], columns=data.columns), data], ignore_index=True)

data = data[['country','currency','target','rates']]
print(data)
data.to_csv('curr.csv', sep='|', encoding='utf-8' , index=False, header=False)