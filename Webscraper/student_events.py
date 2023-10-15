from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import csv
import time

URL = "https://wustl.presence.io/events/list"
DRIVER_PATH = r"C:\Users\Corbin\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
CHROMIUM_PATH = r"C:\Users\Corbin\Downloads\chrome-win64\chrome-win64\chrome.exe"

options = webdriver.ChromeOptions()
options.binary_location = CHROMIUM_PATH  # Pointing to the CfT Chromium
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
options.add_argument('--allow-insecure-localhost')   # Allow insecure localhost
service = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(URL)

    # Give some time for the page to load
    time.sleep(5)

    events_list = []
    while True:
        rows = driver.find_elements_by_css_selector("tr.card.ng-scope")

        for row in rows:
            title = row.find_element_by_css_selector("td:nth-child(1) a").text
            organization = row.find_element_by_css_selector("td:nth-child(2) a").text
            location = row.find_element_by_css_selector("td:nth-child(3)").text
            date_time = row.find_element_by_css_selector("td:nth-child(4)").text

            events_list.append([title, organization, location, date_time])

        # Check if there's a next page and click it
        next_button = driver.find_elements_by_css_selector("i.md.md-chevron-right")
        if next_button and "has-items" in next_button[0].get_attribute("class"):
            next_button[0].click()
            time.sleep(5)
        else:
            break

    # Save details to CSV
    with open("student_events.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Event Title", "Organization", "Location", "Date/Time"])
        writer.writerows(events_list)

    print("Scraping completed and data saved to student_events.csv")

except Exception as e:
    print