import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_text_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return soup.get_text(separator="\n", strip=True)
        else:
            return f"Error: Received status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def process_csv(input_csv):
    df = pd.read_csv(input_csv)

    if 'company_url' not in df.columns:
        print("Error: 'company_url' column not found in CSV")
        return

    df['company_url_raw_data'] = df['company_url'].apply(lambda url: fetch_text_data(url) if pd.notna(url) else "No URL")

    df.to_csv(input_csv, index=False)
    print(f"Raw data has been updated and saved in {input_csv}")

if __name__ == "__main__":
    input_csv = "output.csv"  
    
    process_csv(input_csv)
 
