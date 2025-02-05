from lxml import html
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# Step 1: Scrape stock data (Symbol, Company Name, Market Cap) from the table
url = "https://stockanalysis.com/list/biggest-companies/"
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')
if not table:
    raise Exception("Table not found on the webpage.")

headers = [th.text.strip() for th in table.find_all('th')]
desired_columns = ['Symbol', 'Company Name', 'Market Cap']
column_indices = [headers.index(col) for col in desired_columns]

rows = []
for row in table.find_all('tr')[1:101]:  # Limit to 100 rows
    columns = row.find_all('td')
    if columns:
        row_data = [columns[idx].text.strip() for idx in column_indices]
        rows.append(row_data)

df_symbols = pd.DataFrame(rows, columns=desired_columns)

# Step 2: Fetch historical stock data for each symbol
all_data = []
headers = {"User-Agent": "Mozilla/5.0"}

for symbol in df_symbols["Symbol"]:
    url = f"https://finance.yahoo.com/quote/{symbol}/history/"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for {symbol}")
        continue
    
    tree = html.fromstring(response.content)
    
    try:
        table_headers = tree.xpath('//table//th/text()')
        first_row = [td.text_content().strip() for td in tree.xpath('//table//tr[2]/td')]
        
        if first_row:
            stock_data = dict(zip(table_headers, first_row))
            
            if "Date" in stock_data:
                try:
                    stock_data["Date"] = datetime.strptime(stock_data["Date"], "%b %d, %Y").strftime("%Y-%m-%d")
                except ValueError:
                    print(f"Date format error for {symbol}")
            
            stock_data["Symbol"] = symbol
            stock_data["Scraped Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            all_data.append(stock_data)
        else:
            print(f"No data found for {symbol}")
    except IndexError:
        print(f"Could not find the historical data table for {symbol}")

# Step 3: Export the data to a CSV file
df_all_stocks = pd.DataFrame(all_data)
df_all_stocks.to_csv("scraped_stocks.csv", index=False)
print("Data exported to scraped_stocks.csv")


