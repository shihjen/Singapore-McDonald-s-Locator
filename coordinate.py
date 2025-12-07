# import libraries
import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# config
threads = 10              # Safe: 5–10 threads
retries = 5               # Retry on failures
sleep_between_tasks = 0.05   # Light throttle per call

# helper function to retrieve the latitude and longitude
def get_lat_lon(postal):
    """Query OneMap API for a single postal code."""
    url = "https://www.onemap.gov.sg/api/common/elastic/search"
    params = {
        "searchVal": postal,
        "returnGeom": "Y",
        "getAddrDetails": "Y",
        "pageNum": 1
    }

    for _ in range(retries):
        try:
            r = requests.get(url, params=params, timeout=10).json()
            results = r.get("results", [])

            if not results:
                return postal, None, None

            lat = results[0].get("LATITUDE")
            lon = results[0].get("LONGITUDE")
            return postal, lat, lon

        except:
            time.sleep(0.5)

    # Failed after retries
    return postal, None, None


if __name__ == "__main__":
    # read the data output from main.py
    df = pd.read_csv("mcd.csv")
    postal_list = df["Postal_Code"].astype(str).tolist()

    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(get_lat_lon, p): p for p in postal_list}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching coordinates"):
            postal, lat, lon = future.result()
            results.append((postal, lat, lon))
            time.sleep(sleep_between_tasks)

    # convert results to DataFrame
    res_df = pd.DataFrame(results, columns=["Postal_Code", "Latitude", "Longitude"])

    # merge the data with latitude and longtitude data
    df["Postal_Code"] = df["Postal_Code"].astype(str)
    data = df.merge(res_df, how="left", on="Postal_Code")

    # export the dataframe
    data.to_csv("Singapore_McDonald.csv",index=False)