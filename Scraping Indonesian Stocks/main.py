import requests
import pandas as pd
from bs4 import BeautifulSoup

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

# Example usage
if __name__ == "__main__":
    try:
        # Call the function with default arguments
        df = scrape_stock_data()
        
        # Print the DataFrame
        print(df)
        
        # Optionally, save the DataFrame to a CSV file
        df.to_csv('biggest_companies.csv', index=False)
        print("Data saved to 'biggest_companies.csv'.")
    except Exception as e:
        print(e)