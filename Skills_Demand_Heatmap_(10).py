import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Define paths for JSON files
json_file_path_v10 = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Headcategory_Counts_All_Occurrences_V10.json"
output_heatmap_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Soft_Skills_Heatmap_V10_FIXED.png"

# Load JSON data
with open(json_file_path_v10, 'r', encoding='utf-8') as file:
    data = json.load(file)

monthly_data = data["HeadcategoryCountsByDate"]

# Extract categories dynamically
sample_entry = next(iter(monthly_data.values()))  # Get first record
categories = [key for key in sample_entry.keys() if key not in ["numJobPost", "Total Job Posts"]]

# Determine total job post key (V9 uses "numJobPost", V10 uses "Total Job Posts")
total_job_post_key = "numJobPost" if "numJobPost" in sample_entry else "Total Job Posts"

# Process data and calculate percentages
records = []
for month_key, counts in monthly_data.items():
    total_posts = counts.get(total_job_post_key, 1)  # Avoid division by zero
    date_str = month_key.lower().replace("ask hn who is hiring ", "").title()

    try:
        date_obj = datetime.strptime(date_str, "%B %Y")  # Convert to datetime
    except ValueError:
        print(f"Skipping invalid date: {month_key}")
        continue

    record = {"Date": date_obj.strftime("%Y-%m")}  # Format as YYYY-MM (removes hours)
    for category in categories:
        record[category] = (counts.get(category, 0) / total_posts) * 100  # Convert to percentage

    records.append(record)

# Convert to DataFrame and sort by Date
df = pd.DataFrame(records).sort_values("Date")

# Ensure correct date range (remove incorrect months)
df = df[df["Date"] <= "2025-02"]  # Remove unexpected months

# Pivot the DataFrame for heatmap
df_pivot = df.set_index("Date")[categories].T  # Transpose to have skills on y-axis

# Plot heatmap
plt.figure(figsize=(16, 5))
ax = sns.heatmap(df_pivot, cmap="coolwarm", cbar_kws={'label': 'Percentage of Job Postings (%)'}, linewidths=0.5)

# Format X-axis to avoid clutter
plt.xticks(rotation=45, ha="right")  # Rotate for better readability
plt.xlabel("Year-Month")
plt.ylabel("Soft Skills")
plt.title("Heatmap of Soft Skill Demand Over Time (V10 Dictionary) - Percentage")

# Save the plot
plt.tight_layout()
plt.savefig(output_heatmap_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"✅ Heatmap saved successfully at: {output_heatmap_path}")
