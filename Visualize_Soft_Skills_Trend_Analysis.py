import json
import pandas as pd
import matplotlib.pyplot as plt
import re

# Load the results JSON file
result_json_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\All_Months_Soft_Skills_Counts.json"

with open(result_json_path, "r", encoding="utf-8") as f:
    all_results = json.load(f)

# Convert the data into a structured format
data = []
for month_data in all_results:
    raw_month = month_data["month"]
    
    # Extract "Month Year" from the text (e.g., "Ask HN Who is Hiring April 2011" -> "April 2011")
    match = re.search(r"(\b[A-Za-z]+\s\d{4}\b)", raw_month)
    if match:
        clean_month = match.group(1)  # Extract the matched "Month Year"
    else:
        continue  # Skip if no valid date found

    total_jobs = month_data["total_job_posts"]
    for skill in month_data["soft_skills_analysis"]:
        head_category = skill["head_category"]
        count = skill["count"]
        data.append([clean_month, total_jobs, head_category, count])

# Create a DataFrame
df = pd.DataFrame(data, columns=["Month", "Total Job Posts", "Head Category", "Count"])

# Normalize skill counts by total job posts
df["Normalized Count (%)"] = (df["Count"] / df["Total Job Posts"]) * 100

# Convert month column to datetime format for proper sorting
df["Month"] = pd.to_datetime(df["Month"], format="%B %Y")
df = df.sort_values("Month")  # Sort chronologically

# Pivot table for plotting
pivot_df = df.pivot(index="Month", columns="Head Category", values="Normalized Count (%)")

# Apply a rolling mean to smooth fluctuations
rolling_window = 6  # Adjust this value for more/less smoothing
smoothed_df = pivot_df.rolling(window=rolling_window, min_periods=1).mean()

# Plot
plt.figure(figsize=(14, 7))
smoothed_df.plot(kind="line", marker="o", linestyle="-", alpha=0.75, figsize=(14, 7))

# Format the x-axis for better readability
plt.xlabel("Month", fontsize=12)
plt.ylabel("Normalized Count (%)", fontsize=12)
plt.title("Soft Skill Demand Over Time (Normalized by Total Job Posts, Smoothed)", fontsize=14)
plt.xticks(rotation=45)

# Adjust x-axis to show monthly intervals
plt.xticks(smoothed_df.index[::6], smoothed_df.index[::6].strftime('%b %Y'), rotation=45)  # Every 6 months

# Improve readability of legend
plt.legend(title="Soft Skill Categories", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.6)

# Show plot
plt.show()
