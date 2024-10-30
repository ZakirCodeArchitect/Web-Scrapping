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
            writer.writerow(['Date', 'News'])  # Write header row
        
        for item in news_items:
            # Extract the title attribute from each news item
            news_text = item.get_attribute('title').strip()
            if news_text:  # Ensure it's not empty
                # You need to find the appropriate method to get the date here
                # For now, let's set a placeholder for the date
                date_text = "Date Not Found"  # Replace this with actual date extraction logic
                
                # You can adjust this extraction method based on your inspection
                try:
                    # Example of getting a date element if it exists:
                    # date_element = item.find_element(By.CLASS_NAME, 'actual-date-class-name')
                    # date_text = date_element.text.strip()  
                    
                    # If you have a specific way to derive date from the news_text, do that here
                    # Example: extract date from news_text if it's part of the title
                    # date_text = extract_date_from_news_text(news_text)  # Implement this function
                    
                    # Placeholder for formatted date
                    formatted_date = datetime.now().strftime("%Y-%m-%d")  # Replace with actual date logic
                    
                    # Write to the CSV file
                    writer.writerow([formatted_date, news_text])
                    print(f"{formatted_date}: {news_text}")  # Print to console (optional)
                    
                except Exception as date_extraction_error:
                    print("Error extracting date:", date_extraction_error)
                    continue  # Skip this item if date extraction fails
                
    print("News items have been saved to 'news.csv'")

except Exception as e:
    print("Could not find the news section. Verify the HTML structure or loading time.")
    print("Error:", e)  

finally:
    # Close the WebDriver
    driver.quit()
