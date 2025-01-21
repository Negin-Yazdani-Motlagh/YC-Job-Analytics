import requests
import time
import json
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Input JSON and output directories
input_file = r"C:\Users\negin\Neginn\AI&Education\New Results\Who_Is_Hiring_Posts.json"  # Input file with URLs
html_output_dir = r"C:\Users\negin\Neginn\AI&Education\New Results\HTML_Content"  # Directory for HTML files
json_output_file = r"C:\Users\negin\Neginn\AI&Education\New Results\HTML_Content_Data.json"  # Consolidated JSON file

# Ensure directories exist
os.makedirs(html_output_dir, exist_ok=True)

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36"
}

# Retry and session setup
retry_strategy = Retry(
    total=5,  # Retry up to 5 times
    backoff_factor=2,  # Exponential backoff (2s, 4s, 8s, etc.)
    status_forcelist=[403, 429, 500, 502, 503, 504],  # Retry on these status codes
    allowed_methods=["GET"]  # Retry only on GET requests
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)

# List to store consolidated JSON data
consolidated_data = []

# Fetch and save HTML content for each URL
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

for entry in data:
    title = entry.get('title', 'Unknown_Title')
    url = entry.get('url')

    if not url:
        print(f"Skipping entry with missing URL: {entry}")
        continue

    try:
        print(f"Fetching: {url}")
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        html_content = response.text
        # Ensure file names are safe and descriptive
        safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
        file_name = f"{safe_title}.html"
        html_output_path = os.path.join(html_output_dir, file_name)

        # Save the HTML content to a file
        with open(html_output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(html_content)

        print(f"Saved HTML content for '{title}' to {html_output_path}")

        # Add the entry to consolidated JSON
        consolidated_data.append({
            "title": title,
            "url": url,
            "html_file_path": html_output_path,  # Path to the saved HTML file
            "html_content": html_content  # Optional: Include full HTML (can be omitted to save space)
        })

        time.sleep(2)  # Delay to prevent rate limiting
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch or save HTML for '{title}' from {url}: {e}")

# Save the consolidated JSON data
with open(json_output_file, 'w', encoding='utf-8') as json_file:
    json.dump(consolidated_data, json_file, ensure_ascii=False, indent=4)

print(f"Consolidated JSON data saved to {json_output_file}")
