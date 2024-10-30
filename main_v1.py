from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    # Open a file to save the news
    with open('news.txt', 'w', encoding='utf-8') as file:
        for item in news_items:
            # Extract the title attribute from each news item
            news_text = item.get_attribute('title').strip()
            if news_text:  # Ensure it's not empty
                file.write(news_text + '\n')
                print(news_text)  # Print to console (optional)
                
    print("News items have been saved to 'news.txt'")
    
except Exception as e:
    print("Could not find the news section. Verify the HTML structure or loading time.")
    print("Error:", e)

finally:
    # Close the WebDriver
    driver.quit()
