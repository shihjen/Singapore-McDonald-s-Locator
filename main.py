# import libraries
import pandas as pd
import numpy as np
import urllib.request
import urllib.error
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# url of data
url = "https://custcare.mcdonalds.com.sg/hc/en-us/articles/11875954072857-McDonald-s-Store-Addresses-and-Contact-Details"

if __name__ == "__main__":
    # Set the User-Agent header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Create a Request object
    req = urllib.request.Request(url, headers=headers)

    try:
        # 1. Fetch the page with the headers
        with urllib.request.urlopen(req) as response:
            # Read the raw HTML content
            html_content = response.read()

        # 2. Pass the HTML content to pd.read_html
        tables = pd.read_html(html_content)
        
        print(f"Success! Found {len(tables)} tables.")
        df = tables[0]

        # rename the column
        col = df.iloc[0,:]
        df.columns = col.values
        df = df.iloc[1:,:].set_index(keys="No")

        # extract postal code from address column
        df["Postal_Code"] = df["Address"].str.extract(r"(\b\d{6}\b)")
        df.to_csv("mcd.csv", index=False)

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
    except Exception as e:
        print(f"An error occurred: {e}")

    