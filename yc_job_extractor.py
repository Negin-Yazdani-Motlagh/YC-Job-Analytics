from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to chromedriver
driver_path = r"C:\Users\negin\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Optional: Run in headless mode
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(service=service, options=options)

# Base URL
base_url = "https://news.ycombinator.com/submitted?id=whoishiring"
driver.get(base_url)

# Initialize a set to store unique post URLs
all_urls = set()

try:
    while True:
        # Wait for the page to load
        time.sleep(3)

        # Extract job post links (adjust this XPath to capture relevant links)
        job_links = driver.find_elements(By.XPATH, '//a[contains(@href, "item?id=")]')
        for link in job_links:
            url = link.get_attribute('href')
            if url and url.startswith("https://news.ycombinator.com/item?id="):  # Ensure valid links
                all_urls.add(url)

        # Find the "More" or "Next" button and click it
        try:
            next_button = driver.find_element(By.LINK_TEXT, 'More')  # Adjust if text changes
            next_button.click()
            time.sleep(3)  # Wait for the next page to load
        except Exception:
            print("No more 'More' button found or all pages loaded.")
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Save URLs to a file
    with open("hacker_news_urls.txt", "w") as file:
        for url in sorted(all_urls):  # Sort URLs for easier debugging
            file.write(url + "\n")

    # Close the WebDriver
    driver.quit()

# Print completion message
print(f"Scraping completed. {len(all_urls)} URLs saved to hacker_news_urls.txt.")
