import openai
import pandas as pd
import requests
import os

# Retrieve the OpenAI GPT-3 API key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Function to fetch CSV file from the given URL
def fetch_csv_data(url):
    response = requests.get(url)
    content = response.text
    df = pd.read_csv(pd.io.common.StringIO(content))  # Updated import
    return df
    
# Function to generate NSE Symbols or BSE Codes using GPT-3
def generate_codes_with_gpt3(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

# URL of the CSV file
csv_url = "https://raw.githubusercontent.com/nikunjbaheti/MF_Holdings/main/modified_StkCode.csv"

# Fetch CSV data
df = fetch_csv_data(csv_url)

# Create empty lists to store results
fincodes = []
company_names = []
generated_codes = []

# Iterate over rows and generate codes
for index, row in df.iterrows():
    name = row['Stock Name']
    fincode = row['Stock Number']
    prompt = f"Generate NSE Symbols or BSE Codes for {name} ({fincode}):"
    
    # Use GPT-3 to generate codes
    generated_code = generate_codes_with_gpt3(prompt)
    
    # Append to lists
    fincodes.append(fincode)
    company_names.append(name)
    generated_codes.append(generated_code)

# Create a new DataFrame with the results
result_df = pd.DataFrame({'FinCode': fincodes, 'Company Name': company_names, 'Generated Code': generated_codes})

# Save the DataFrame to a CSV file
result_df.to_csv('generated_codes_output.csv', index=False)

# Print a message indicating success
print("Generated codes saved to generated_codes_output.csv")
