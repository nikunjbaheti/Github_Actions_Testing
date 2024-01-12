import pandas as pd
import requests
from io import StringIO

# URL for the Stock Codes CSV
stock_codes_url = "https://raw.githubusercontent.com/nikunjbaheti/MF_Holdings/main/StkCode.csv"
# URL for the original data CSV
original_data_url = "https://raw.githubusercontent.com/nikunjbaheti/MF_Holdings/main/output_data.csv"

# Fetch the Stock Codes CSV from the URL
stock_codes_response = requests.get(stock_codes_url)
stock_codes_data = stock_codes_response.text

# Fetch the original data CSV from the URL
original_data_response = requests.get(original_data_url)
original_data = original_data_response.text

# Read the CSV data into DataFrames
stock_codes_df = pd.read_csv(StringIO(stock_codes_data))
original_df = pd.read_csv(StringIO(original_data))

# Merge the two DataFrames on the 'fincode' column
merged_df = pd.merge(original_df, stock_codes_df, left_on='fincode', right_on='Stock Number', how='left')

# Drop the redundant 'Stock Number' column
merged_df = merged_df.drop('Stock Number', axis=1)

# Keep the first occurrence and delete the rest based on 'fincode' and 'scheme'
final_df = merged_df.drop_duplicates(subset=['fincode', 'scheme'], keep='first')

# Save the updated DataFrame to a new CSV file named 'output_data.csv'
final_df.to_csv('output_data.csv', index=False)
