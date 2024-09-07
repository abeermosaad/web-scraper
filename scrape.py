#!./.venv/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import csv
import os


class DriverManager:
    """
    A class to manage the Chrome driver instance.
    """

    def __init__(self):
        self.driver = self.get_driver()

    def get_driver(self):
        """Get a Chrome driver with headless mode enabled."""

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--lang=en")

        homedir = os.path.expanduser("~")
        chrome_binary_path = os.path.join(homedir, 'chrome-linux64', 'chrome')

        if not os.path.isfile(chrome_binary_path):
            raise FileNotFoundError(
                f"Chrome binary not found at {chrome_binary_path}")

        chrome_options.binary_location = chrome_binary_path
        chromedriver_path = os.path.join(homedir, 'chromedriver')

        if not os.path.isfile(chromedriver_path):
            raise FileNotFoundError(
                f"ChromeDriver not found at {chromedriver_path}")

        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        return driver

    def close_driver(self):
        """Close the Chrome driver."""

        if self.driver:
            self.driver.quit()


class GoogleScraper:
    def __init__(self, driver):
        self.driver = driver

    def search_google(self, company_name):
        """Search Google for the company and extract the review URL."""

        search_url = f"https://www.google.com/search?q={company_name}+reviews&hl=en"
        self.driver.get(search_url)

        # url to google review page (if any)
        google_review_url = ""
        # raw google review page scraped into this column (if there's a company url)
        google_review_url_raw_data = ""

        try:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div[role="complementary"]')
                    )
                )
            except TimeoutException:
                print(
                    f"No review card found for {company_name.replace('+', ' ')} within the timeout period.")

                return google_review_url, google_review_url_raw_data

            card = self.driver.find_element(
                By.CSS_SELECTOR,
                'div[role="complementary"]'
            )
            google_review_url_raw_data = card.text

            if card:
                try:
                    review_dialog_tag = card.find_element(
                        By.CSS_SELECTOR,
                        'a[data-async-trigger="reviewDialog"]'
                    )
                except Exception as e:
                    print(f"Error while searching for review dialog tag: {e}")

                    return google_review_url, google_review_url_raw_data

                if review_dialog_tag:
                    data_fid = review_dialog_tag.get_attribute('data-fid')
                    if data_fid:
                        google_review_url = f"https://www.google.com/search?q={company_name}+reviews&hl=en#lrd={data_fid},1,,,,"

        except Exception as e:
            print(f"Error during search for {company_name}: {e}")

        return google_review_url, google_review_url_raw_data

    def fetch_review_details(self, google_review_url):
        """Fetch Google review rating and number of reviews from the review URL."""
        if not google_review_url:
            return "", ""

        self.driver.get(google_review_url)

        google_review_rating = ""
        google_reviews_number = ""

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.c9QyIf')
                )
            )

            rating_div = self.driver.find_element(
                By.CSS_SELECTOR,
                'div.c9QyIf'
            )

            if rating_div:
                google_review_rating = rating_div.find_element(
                    By.CSS_SELECTOR,
                    'span.Aq14fc'
                ).text

            reviews_div = self.driver.find_element(
                By.CSS_SELECTOR,
                'div.c9QyIf'
            )

            if reviews_div:
                reviews_text = reviews_div.find_element(
                    By.CSS_SELECTOR,
                    'span.z5jxId'
                ).text

                google_reviews_number = ''.join(
                    filter(
                        str.isdigit,
                        reviews_text
                    )
                )

        except TimeoutException:
            print(
                f"Timeout while fetching review details from {google_review_url}.")
        except Exception as e:
            print(f"Error during fetching review details: {e}")

        return google_review_rating, google_reviews_number


class YelpScraper:
    """
    A class to scrape Yelp reviews.
    """

    def __init__(self, driver):
        self.driver = driver

    def search_yelp_google(self, company_name):
        """
        Search Yelp on Google and extract the Yelp URL.
        """

        search_url = f"https://www.google.com/search?q={company_name}+Yelp&hl=en"
        self.driver.get(search_url)

        yelp_review_url = ""
        yelp_review_url_raw_data = ""

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'a[jsname="UWckNb"]')
                )
            )
        except TimeoutException:
            print(
                f"No review card found for {company_name.replace('+', ' ')} within the timeout period.")

            return yelp_review_url, yelp_review_url_raw_data

        # Similar methods to GoogleScraper but tailored for Yelp


class ThumbtackScraper:
    def __init__(self, driver):
        self.driver = driver

    # Similar methods to GoogleScraper but tailored for Thumbtack


class ReviewScraper:
    def __init__(self, input_csv):
        self.input_csv = input_csv
        self.driver_manager = DriverManager()
        self.google_scraper = GoogleScraper(self.driver_manager.driver)
        self.yelp_scraper = YelpScraper(self.driver_manager.driver)
        self.thumbtack_scraper = ThumbtackScraper(self.driver_manager.driver)

    def scrape_reviews(self):
        rows = []
        with open(self.input_csv, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            fieldnames = csv_reader.fieldnames
            for row in csv_reader:
                company_name = row['company']
                print(f"\nSearching reviews for {company_name}...")

                # Google
                google_review_url, google_review_url_raw_data = self.google_scraper.search_google(
                    company_name.replace(' ', '+'))
                google_review_rating, google_reviews_number = self.google_scraper.fetch_review_details(
                    google_review_url)

                # Yelp
                # yelp_review_url, yelp_review_url_raw_data, yelp_review_rating, yelp_reviews_number = self.yelp_scraper.scrape_yelp(company_name)

                # Thumbtack
                # thumbtack_review_url, thumbtack_review_url_raw_data, thumbtack_review_rating, thumbtack_reviews_number = self.thumbtack_scraper.scrape_thumbtack(company_name)

                # Update the row with scraped data
                row['google_review_url'] = google_review_url
                row['google_review_url_raw_data'] = google_review_url_raw_data
                row['google_review_rating'] = google_review_rating
                row['google_reviews_number'] = google_reviews_number

                # Add similar assignments for Yelp and Thumbtack fields

                rows.append(row)

        # Write updated data to the CSV file
        self.update_csv(rows, fieldnames)

        # Clean up the driver
        self.driver_manager.close_driver()

    def update_csv(self, rows, fieldnames):
        with open(self.input_csv, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(rows)


# Example usage
input_csv_path = 'data.csv'
review_scraper = ReviewScraper(input_csv_path)
review_scraper.scrape_reviews()