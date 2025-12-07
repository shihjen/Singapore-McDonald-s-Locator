## 🍟 Singapore McDonald's Locator
This repository contains a simple Python script to scrape and geolocate the addresses of all McDonald's restaurants in Singapore. The final output is a CSV file containing the restaurant name, address, postal code, latitude, and longitude.

### ⚙️ How It Works
The script performs two main steps:

1. Data Scraping: It scrapes the list of addresses from the official McDonald's Singapore website using pandas.read_html(). It then cleans the data and extracts the 6-digit postal code using a regular expression.

2. Geocoding: It uses the extracted postal codes to query the OneMap API (a Singapore government mapping service) to retrieve the Latitude and Longitude for each location. This process is accelerated using multi-threading (concurrent.futures) to efficiently handle the API calls.

### 🛠️ Prerequisites
Before running the script, ensure you have Python 3.x installed and the required packages are present.

1. Requirements
You can install the necessary packages using pip:
```
pip install -r requirements.txt
```

