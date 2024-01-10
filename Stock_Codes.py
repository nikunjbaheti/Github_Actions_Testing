import pandas as pd
import requests
import logging

# Set up logging
logging.basicConfig(filename='ticker_search.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'QI9PFYE7SQUB9X0Q'

# Replace 'path/to/your/csvfile.csv' with the actual path to your CSV file
csv_file_path = 'modified_StkCode.csv'
output_csv_file = 'Tickers.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

def get_ticker_by_company_name(company_name):
    try:
        # Replace 'demo' with your actual Alpha Vantage API key
        api_url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={api_key}'
        response = requests.get(api_url)
        data = response.json()

        # Extract the first result (you can modify this logic based on your requirements)
        if 'bestMatches' in data:
            first_result = data['bestMatches'][0]
            return first_result.get('1. symbol', None)
        else:
            return None
    except Exception as e:
        logging.error(f"Error searching for ticker for {company_name}: {str(e)}")
        return None

# Add a new column 'Ticker' to the DataFrame to store the tickers
df['Ticker'] = df['Stock Name'].apply(get_ticker_by_company_name)

# Log the results
logging.info('Ticker search results:')
logging.info(df)

# Store the DataFrame with added Ticker column in a CSV file
df.to_csv(output_csv_file, index=False)

# Log the file path where the output data is stored
logging.info(f'Ticker data stored in {output_csv_file}')
