import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# File path for the JSON dataset
file_path = r'C:\Users\negin\YC-Job-Analytics\result\job_post_counts.json'

# Load the JSON data
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialize a DataFrame to store job counts by month and year
job_counts = []

# Parse the JSON data
for key, count in data.items():
    # Extract the month and year from the key
    parts = key.split()
    if len(parts) >= 5:
        month = parts[-2]
        year = parts[-1]
        try:
            job_counts.append({"Year": int(year), "Month": month, "Count": count})
        except ValueError:
            print(f"Skipping invalid entry: {key}")

# Create a DataFrame
df = pd.DataFrame(job_counts)

# Convert month names to numbers for sorting
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
df['Month_Num'] = df['Month'].apply(lambda x: month_order.index(x) + 1)

# Pivot the DataFrame to have months as rows and years as columns
pivot_df = df.pivot(index='Month_Num', columns='Year', values='Count').sort_index()

# Plot the data with distinct colors
plt.figure(figsize=(15, 8))
colormap = plt.cm.get_cmap('tab20', len(pivot_df.columns))  # Use 'tab20' colormap
for i, year in enumerate(pivot_df.columns):
    plt.plot(
        pivot_df.index, pivot_df[year], 
        marker='o', linestyle='-', label=str(year), 
        color=colormap(i), linewidth=1.5, alpha=0.8
    )

# Format the plot
plt.title("Seasonal Changes in Job Postings (Year-by-Year)", fontsize=18, fontweight='bold')
plt.xlabel("Month", fontsize=14, labelpad=10)
plt.ylabel("Job Postings", fontsize=14, labelpad=10)
plt.xticks(ticks=range(1, 13), labels=month_order, rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title="Year", fontsize=10, title_fontsize=12, loc='upper left', ncol=2, frameon=False)
plt.grid(alpha=0.3, linestyle='--')
plt.tight_layout()

# Save and show the plot
output_chart_path = r'C:\Users\negin\YC-Job-Analytics\result\distinct_colors_seasonal_changes.png'
plt.savefig(output_chart_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"Enhanced chart with distinct colors saved to: {output_chart_path}")
