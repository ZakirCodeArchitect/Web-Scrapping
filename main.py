from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
from datetime import datetime

# Path to your ChromeDriver
chrome_driver_path = "C:/Users/Hp/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Initialize Selenium WebDriver with your ChromeDriver path
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# URL of the website
url = 'https://ihc.gov.pk/'

# Open the webpage
driver.get(url)

try:
    # Wait for the iframe to be present and switch to it
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
    )
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)  # Switch to the iframe

    # Wait for the news div to be present in the DOM
    news_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'divnews'))
    )
    
    # Find all list items (li tags) within the news div
    news_items = news_div.find_elements(By.TAG_NAME, 'li')

    # Define the path to the CSV file
    csv_file_path = 'news.csv'

    # Prepare to write to the CSV file
    file_exists = os.path.isfile(csv_file_path)  # Check if the file exists

    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write header if the file is new
        if not file_exists:
            writer.writerow(['Case Title', 'Case Date', 'Case Details'])  # Write header row
        
        for item in news_items:
            # Extract the title attribute from each news item
            news_title = item.get_attribute('title').strip()
            if news_title:  # Ensure it's not empty
                # Extract additional details if available (adjust according to the actual HTML structure)
                details_text = item.text.strip()  # This might contain additional details

                # You need to find the appropriate method to get the date here
                date_text = "Date Not Found"  # Replace this with actual date extraction logic
                
                # Example logic to extract date from the news item
                try:
                    # This assumes there's a date element related to the news item
                    date_element = item.find_element(By.CLASS_NAME, 'news-date')  # Update with actual class if necessary
                    date_text = date_element.text.strip()
                except Exception:
                    date_text = datetime.now().strftime("%Y-%m-%d")  # Default to current date if not found

                # Write to the CSV file in a clean format
                writer.writerow([news_title, date_text, details_text])
                print(f"Title: {news_title}, Date: {date_text}, Details: {details_text}")  # Print to console (optional)

    print("News items have been saved to 'news.csv'")

except Exception as e:
    print("Could not find the news section. Verify the HTML structure or loading time.")
    print("Error:", e)  

finally:
    # Close the WebDriver
    driver.quit()
