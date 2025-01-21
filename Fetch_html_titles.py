import requests
import json
import os

# List of URLs to extract HTML from
urls = [
    "https://news.ycombinator.com/submitted?id=whoishiring",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=39562986&n=31",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=35773707&n=61",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=31947297&n=91",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=28380661&n=121",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=24969524&n=151",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=22225313&n=181",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=19543939&n=211",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=17205866&n=241",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=14901314&n=271",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=12627853&n=301",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=10655741&n=331",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=8822808&n=361",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=7162197&n=391",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=4857717&n=421",
    "https://news.ycombinator.com/submitted?id=whoishiring&next=2949790&n=451"
]

# Dictionary to store results
results = []

# Loop through each URL, fetch HTML, and save to results
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        html_content = response.text
        results.append({"url": url, "html": html_content})
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        results.append({"url": url, "html": None, "error": str(e)})

# Save results to JSON file in the specified path
output_directory = r"C:\Users\negin\Neginn\AI&Education\New Results"
output_filename = "HTML_All_Titles.json"
output_path = os.path.join(output_directory, output_filename)

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Write results to the file
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print(f"HTML content saved to {output_path}")
