import requests
import pandas as pd
from bs4 import BeautifulSoup

# Function to scrape stock data (Symbol, Company Name, Market Cap) from the initial URL
def scrape_stock_data(url="https://stockanalysis.com/list/biggest-companies/", max_rows=100):
    """
    Scrape stock data (Symbol, Company Name, Market Cap) from a table on the given URL.

    Args:
        url (str): The URL of the webpage containing the stock table (default is the NYSE biggest companies list).
        max_rows (int): The maximum number of rows to scrape (default is 100).

    Returns:
        pd.DataFrame: A DataFrame containing the scraped stock data.
    """
    # Send an HTTP request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table containing the stock list
    table = soup.find('table')
    if not table:
        raise Exception("Table not found on the webpage.")
    
    # Extract the table headers
    headers = [th.text.strip() for th in table.find_all('th')]
    
    # Find the indices of the desired columns
    desired_columns = ['Symbol', 'Company Name', 'Market Cap']
    column_indices = [headers.index(col) for col in desired_columns]
    
    # Initialize a list to store the rows
    rows = []
    
    # Iterate over the rows in the table (skip the header row)
    for row in table.find_all('tr')[1:max_rows + 1]:  # Limit to max_rows
        # Extract the columns in each row
        columns = row.find_all('td')
        if len(columns) > 0:
            # Extract the data for the desired columns
            row_data = [columns[idx].text.strip() for idx in column_indices]
            rows.append(row_data)
    
    # Create a DataFrame using Pandas
    df = pd.DataFrame(rows, columns=desired_columns)
    
    return df

# Function to scrape additional stock details from Yahoo Finance
def scrape_stock_details(symbol):
    """
    Scrape stock details (price, previous close, open, volume, avg volume, market cap) from Yahoo Finance.

    Args:
        symbol (str): The stock symbol (e.g., AAPL).

    Returns:
        dict: A dictionary containing the scraped stock details.
    """
    # Construct the URL for the stock symbol
    url = f"https://finance.yahoo.com/quote/{symbol}"
    
    # Send an HTTP request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the webpage for {symbol}. Status code: {response.status_code}")
    
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the required fields
    try:
        # Stock Price
        price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text.strip()
        
        # Previous Close
        previous_close = soup.find('td', {'data-test': 'PREV_CLOSE-value'}).text.strip()
        
        # Open Price
        open_price = soup.find('td', {'data-test': 'OPEN-value'}).text.strip()
        
        # Volume
        volume = soup.find('td', {'data-test': 'TD_VOLUME-value'}).text.strip()
        
        # Avg Volume
        avg_volume = soup.find('td', {'data-test': 'AVERAGE_VOLUME_3MONTH-value'}).text.strip()
        
        # Market Cap
        market_cap = soup.find('td', {'data-test': 'MARKET_CAP-value'}).text.strip()
        
        # Return the details as a dictionary
        return {
            'Symbol': symbol,
            'Price': price,
            'Previous Close': previous_close,
            'Open': open_price,
            'Volume': volume,
            'Avg Volume': avg_volume,
            'Market Cap': market_cap
        }
    except AttributeError:
        raise Exception(f"Failed to extract data for {symbol}. The webpage structure may have changed.")

# Main script
if __name__ == "__main__":
    try:
        # Step 1: Scrape the initial stock data
        df = scrape_stock_data(max_rows=10)  # Limit to 10 rows for testing
        print("Initial stock data scraped successfully.")
        print(df)
        
        # Step 2: Scrape additional details for each stock symbol
        stock_details = []
        for symbol in df['Symbol']:
            try:
                details = scrape_stock_details(symbol)
                stock_details.append(details)
                print(f"Scraped details for {symbol}")
            except Exception as e:
                print(e)
        
        # Convert the list of details to a DataFrame
        details_df = pd.DataFrame(stock_details)
        
        # Print the details DataFrame
        print(details_df)
        
        # Optionally, save the details DataFrame to a CSV file
        details_df.to_csv('stock_details.csv', index=False)
        print("Stock details saved to 'stock_details.csv'.")
    except Exception as e:
        print(e)