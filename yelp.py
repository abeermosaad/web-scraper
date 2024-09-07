import requests
from bs4 import BeautifulSoup

def search_yelp_google(company_name):
    search_url = f"https://www.google.com/search?q={company_name.replace(' ', '+')}+Yelp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a', href=True):
        href = a['href']
            
        if "yelp.com" in href:
            return href
    
    return None


def get_yelp_data(company_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    response = requests.get(company_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # check first if yelp have the same website link as the one we are looking for.
    
    rating_tag = soup.find('span', class_='y-css-1o34y7f')
    rating = rating_tag.get_text() if rating_tag else None

    reviews_tag = soup.find('a', class_='y-css-12ly5yx')
    reviews_text = reviews_tag.get_text() if reviews_tag else None

    if reviews_text:
        reviews_number = reviews_text.split()[0].strip("()")
    else:
        reviews_number = None
    return {
        'yelp_review_url': company_url,
        'rating': rating,
        'reviews': reviews_number,
    }

company_name = "Cal Vasquez Handyman"
yelp_url = search_yelp_google(company_name)
if yelp_url:
    company_data = get_yelp_data(yelp_url)
    print(company_data)
