import requests
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    url = "https://westacklandscaping.com/"
    
    text_data = fetch_text_data(url)
    
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(text_data)
    
    print("The extracted text has been saved as 'output.txt'.")
