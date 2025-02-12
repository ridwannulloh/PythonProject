from lxml import html
import requests
from datetime import datetime

url = "https://finance.yahoo.com/quote/NVDA/history/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Failed to retrieve data")
else:
    tree = html.fromstring(response.content)
    
    try:
        headers = tree.xpath('//table//th/text()')
        first_row = [td.text_content().strip() for td in tree.xpath('//table//tr[2]/td')]
        
        if first_row:
            stock_data = dict(zip(headers, first_row))
            
            # Convert Date column to yyyy-mm-dd format
            if "Date" in stock_data:
                try:
                    stock_data["Date"] = datetime.strptime(stock_data["Date"], "%b %d, %Y").strftime("%Y-%m-%d")
                except ValueError:
                    print("Date format error")
            
            # Add scraped_date column
            stock_data["Scraped Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for key, value in stock_data.items():
                print(f"{key}: {value}")
        else:
            print("No data found in the first row.")
    except IndexError:
        print("Could not find the historical data table.")