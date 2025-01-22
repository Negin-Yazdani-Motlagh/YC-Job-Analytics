import os
from bs4 import BeautifulSoup
import json

# Path to the folder containing HTML files
html_folder = "C:/Users/negin/YC-Job-Analytics/result/HTML_Content"
output_file = "C:/Users/negin/YC-Job-Analytics/result/job_post_counts.json"  # Output JSON file

# Dictionary to store job post counts
job_post_counts = {}

# Process each HTML file
for file_name in os.listdir(html_folder):
    if file_name.endswith(".html"):
        print(f"Processing {file_name}...")
        file_path = os.path.join(html_folder, file_name)

        # Open and parse the HTML file
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            articles = soup.find_all(class_="athing")

            # Count top-level comments (job posts)
            num_job_posts = sum(
                1
                for article in articles
                if article.find(class_="commtext") and article.find(class_="ind").get("indent") == "0"
            )

        # Extract the date from the file name (assumes format like "2025-01.html")
        date = file_name.replace(".html", "")

        # Store the result
        job_post_counts[date] = num_job_posts

# Save the results to a JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(job_post_counts, f, indent=4)

print(f"Job post counts saved to {output_file}")
