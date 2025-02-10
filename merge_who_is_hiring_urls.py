import json

# File paths
existing_json_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Who_is_hiring_URLs.json"
output_json_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Feb_who_is_hiring_URLs.json"

# New data to merge
new_entry = {
    "title": "Ask HN: Who is hiring? (February 2025)",
    "url": "https://news.ycombinator.com/item?id=42919502",
    "source_url": "https://news.ycombinator.com/submitted?id=whoishiring"
}

# Load the existing JSON data
try:
    with open(existing_json_path, "r", encoding="utf-8") as file:
        existing_data = json.load(file)
    print(f"Loaded {len(existing_data)} entries from the existing JSON file.")
except FileNotFoundError:
    print(f"Existing JSON file not found: {existing_json_path}. Creating a new file.")
    existing_data = []

# Check for duplicates based on the "url" field
if not any(entry["url"] == new_entry["url"] for entry in existing_data):
    # Add the new entry at the top
    updated_data = [new_entry] + existing_data
    print(f"Added new entry at the top: {new_entry['url']}")
else:
    print(f"Entry with URL {new_entry['url']} already exists. Skipping.")
    updated_data = existing_data

# Save the updated data to the new JSON file
with open(output_json_path, "w", encoding="utf-8") as file:
    json.dump(updated_data, file, ensure_ascii=False, indent=4)

print(f"Updated JSON saved to: {output_json_path}")
