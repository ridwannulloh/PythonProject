from lxml import html
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def scrape_stock_data(url="https://stockanalysis.com/list/biggest-companies/", max_rows=100):
    """
    Scrape stock data (Symbol, Company Name, Market Cap) from a table on the given URL.
    """
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
    for row in table.find_all('tr')[1:max_rows + 1]:
        columns = row.find_all('td')
        if columns:
            row_data = [columns[idx].text.strip() for idx in column_indices]
            rows.append(row_data)
    
    return pd.DataFrame(rows, columns=desired_columns)

def fetch_stock_data(symbol):
    """Fetch historical stock data for a given symbol from Yahoo Finance."""
    url = f"https://finance.yahoo.com/quote/{symbol}/history/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for {symbol}")
        return None
    
    tree = html.fromstring(response.content)
    
    try:
        headers = tree.xpath('//table//th/text()')
        first_row = [td.text_content().strip() for td in tree.xpath('//table//tr[2]/td')]
        
        if first_row:
            stock_data = dict(zip(headers, first_row))
            
            if "Date" in stock_data:
                try:
                    stock_data["Date"] = datetime.strptime(stock_data["Date"], "%b %d, %Y").strftime("%Y-%m-%d")
                except ValueError:
                    print(f"Date format error for {symbol}")
            
            stock_data["Symbol"] = symbol
            stock_data["Scraped Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return stock_data
        else:
            print(f"No data found for {symbol}")
            return None
    except IndexError:
        print(f"Could not find the historical data table for {symbol}")
        return None

def fetch_multiple_stocks(df):
    """Fetch historical stock data for multiple symbols."""
    all_data = [fetch_stock_data(symbol) for symbol in df["Symbol"] if fetch_stock_data(symbol)]
    return pd.DataFrame(all_data)

# Example usage
df_symbols = scrape_stock_data()
print(df_symbols)
# df_all_stocks = fetch_multiple_stocks(df_symbols)
# df_all_stocks.to_csv("scraped_stocks.csv", index=False)
# print("Data exported to scraped_stocks.csv")