import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
URL = "https://happenings.wustl.edu/calendar"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'}

# Try to get the content from the URL
try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()  # raise an exception for HTTP errors
    soup = BeautifulSoup(response.content, 'html.parser')
except requests.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

# Find all events
events = soup.find_all("div", class_="item event_item vevent")

# List to hold all event details
events_list = []

for event in events:
    # Get event name
    name_element = event.find("h3", class_="summary").a
    name = name_element.text.strip() if name_element else "N/A"

    # Get event date
    day_element = event.find("span", class_="day")
    day = day_element.text.strip() if day_element else "N/A"

    month_element = event.find("span", class_="month")
    month = month_element.text.strip() if month_element else "N/A"

    date = f"{day} {month}"  # you can format this as needed

    # Get event place
    place_element = event.find("div", class_="location").a
    place = place_element.text.strip() if place_element else "N/A"

    # Append details to the list
    events_list.append([name, date, place])

# Save details to CSV
try:
    with open("events.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Event Name", "Event Date", "Event Place"])
        writer.writerows(events_list)
    print("Scraping completed and data saved to events.csv")
except Exception as e:
    print(f"Error writing to CSV: {e}")