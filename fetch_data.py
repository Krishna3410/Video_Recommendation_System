import requests
import csv
import os
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Define API URLs and headers
API_URLS = {
    'viewed_posts': "https://api.socialverseapp.com/posts/view?page={page}&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    'liked_posts': "https://api.socialverseapp.com/posts/like?page={page}&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    'inspired_posts': "https://api.socialverseapp.com/posts/inspire?page={page}&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    'rated_posts': "https://api.socialverseapp.com/posts/rating?page={page}&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    'summary_posts': "https://api.socialverseapp.com/posts/summary/get?page={page}&page_size=1000",
    'all_users': "https://api.socialverseapp.com/users/get_all?page={page}&page_size=1000"
}
HEADERS = {
    "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
}

# Map API names to the relevant key in their response
DATA_KEYS = {
    'viewed_posts': 'posts',
    'liked_posts': 'posts',
    'inspired_posts': 'posts',
    'rated_posts': 'posts',
    'summary_posts': 'posts',
    'all_users': 'users'
}

# Directory to save CSV files
OUTPUT_DIR = "fetched_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set up retries for requests
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

# Function to fetch data from an API and save directly to CSV
def fetch_and_save_to_csv(api_name, api_url_template, max_pages=100):
    all_records = []  # List to store all fetched records
    for page in range(1, max_pages + 1):
        api_url = api_url_template.format(page=page)
        print(f"Fetching page {page} from {api_name}...")

        try:
            response = session.get(api_url, headers=HEADERS)
            if response.status_code != 200:
                print(f"Failed to fetch page {page} for {api_name}. HTTP Status: {response.status_code}")
                break

            # Parse the response as JSON
            data = response.json()

            # Extract the relevant data key
            key = DATA_KEYS.get(api_name)
            if not key or key not in data:
                print(f"No relevant data key '{key}' found in page {page} for {api_name}.")
                break

            # Extract the relevant records
            records = data[key]
            if not records:
                print(f"No data found on page {page} for {api_name}. Stopping.")
                break

            # Add records to the list
            all_records.extend(records)
            print(f"Fetched {len(records)} records from page {page}. Total records: {len(all_records)}.")

        except Exception as e:
            print(f"Error fetching data from page {page} for {api_name}: {e}")
            break

        #  Add delay to avoid overwhelming the server
        time.sleep(1)

    # Save all records to CSV
    if all_records:
        save_to_csv(all_records, os.path.join(OUTPUT_DIR, f"{api_name}.csv"))
    else:
        print(f"No data to save for {api_name}.")

# Function to save data to a CSV file
def save_to_csv(data, output_file):
    if not data:
        print(f"No data available to save for {output_file}.")
        return

    # Determine the CSV headers from the first record
    headers = data[0].keys() if isinstance(data[0], dict) else []
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {output_file}")

# Main function to fetch data from all APIs
def fetch_all_data():
    for api_name, api_url_template in API_URLS.items():
        print(f"Starting data fetch for {api_name}...")
        fetch_and_save_to_csv(api_name, api_url_template)
    print("Data fetching complete.")

if __name__ == "__main__":
    fetch_all_data()
