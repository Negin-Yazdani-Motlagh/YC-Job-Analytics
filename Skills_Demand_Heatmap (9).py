import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# File path for JSON data
json_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Headcategory_Counts_All_Occurrences_V9.json"

# Load JSON data
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract data from JSON
monthly_data = data.get("HeadcategoryCountsByDate", {})

# Convert to DataFrame
records = []
for date_str, counts in monthly_data.items():
    # Extract actual date from the string
    match = re.search(r"(\w+ \d{4})", date_str)  # Extract "April 2011"
    if not match:
        continue  # Skip if no valid date format is found

    formatted_date = match.group(1)

    try:
        date_obj = pd.to_datetime(formatted_date, errors='coerce', format='%B %Y').strftime('%Y-%m')  # Keep only YYYY-MM
        if pd.isna(date_obj):
            continue  # Skip invalid dates
    except ValueError:
        continue

    num_job_posts = counts.get("numJobPost", 1)  # Avoid division by zero
    record = {"Date": date_obj}

    for skill, count in counts.items():
        if skill != "numJobPost":
            record[skill] = (count / num_job_posts) * 100  # Normalize to percentage
    records.append(record)

# Convert records into DataFrame
df = pd.DataFrame(records)

# Check if Date column exists
if "Date" not in df.columns or df["Date"].isnull().all():
    raise ValueError("Date parsing failed. Check input JSON format.")

# Sort by Date and set index for heatmap
df = df.sort_values("Date").set_index("Date").fillna(0)

# Improve visualization: Increase figure size, rotate x-axis labels, and fix clutter
plt.figure(figsize=(16, 7))
ax = sns.heatmap(df.T, cmap="coolwarm", linewidths=0.5, annot=False)

# Rotate x-axis labels and reduce frequency
plt.xticks(range(0, len(df.index), 5), df.index[::5], rotation=45, ha="right", fontsize=10)  # Show every 5th label
plt.yticks(fontsize=12)

# Improve title and labels
plt.xlabel("Year", fontsize=14)
plt.ylabel("Soft Skills", fontsize=14)
plt.title("Heatmap of Soft Skill Demand Over Time (V9 Dictionary)", fontsize=16)

# Adjust spacing for clarity
plt.tight_layout()

# Save figure as PNG
output_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Soft_Skills_Heatmap_V9.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

# Show plot
plt.show()

print(f"Heatmap saved to {output_path}")
