import requests
from bs4 import BeautifulSoup

def fetch_text_data(url):
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return soup.get_text(separator="\n", strip=True)
        else:
            return f"Error: Received status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    url = "https://avavioconstruction.com/"
    
    text_data = fetch_text_data(url)
    
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(text_data)
    
    print("The extracted text has been saved as 'output.txt'.")
