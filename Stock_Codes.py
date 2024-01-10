import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import logging

# Set up logging
logging.basicConfig(filename='ticker_search.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'QI9PFYE7SQUB9X0Q'

# Initialize the TimeSeries object with your API key
ts = TimeSeries(key=api_key)

# Read the CSV file into a DataFrame
csv_file_path = 'modified_StkCode.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

def get_ticker_by_company_name(company_name):
    # Search for stock symbols by company name
    search_results, _ = ts.search_symbol(keywords=company_name)
    
    # Extract the first result (you can modify this logic based on your requirements)
    if search_results:
        first_result = search_results[0]
        return first_result['1. symbol']
    else:
        return None

# Add a new column 'Ticker' to the DataFrame to store the tickers
df['Ticker'] = df['Stock Name'].apply(get_ticker_by_company_name)

# Log the results
logging.info('Ticker search results:')
logging.info(df)

# Store the DataFrame with added Ticker column in a CSV file
output_csv_file = 'Tickers.csv'
df.to_csv(output_csv_file, index=False)

# Log the file path where the output data is stored
logging.info(f'Ticker data stored in {output_csv_file}')
