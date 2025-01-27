import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# File paths
file_path = r'C:\Users\negin\YC-Job-Analytics\result\job_post_counts.json'
output_excel_path = r'C:\Users\negin\YC-Job-Analytics\result\seasonal_job_postings.xlsx'
output_chart_path = r'C:\Users\negin\YC-Job-Analytics\result\seasonal_change_job_postings.png'

# Load the JSON file
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialize a list to store job post counts
records = []

# Extract data from the JSON structure
for month_year, job_post_count in data.items():
    # Extract the clean date from the key (e.g., "Ask HN Who is Hiring April 2011")
    cleaned_date = " ".join(month_year.split()[-2:])
    try:
        # Convert to datetime for processing
        date = datetime.strptime(cleaned_date, "%B %Y")
        records.append({"Date": date, "Job_Posts": job_post_count})
    except ValueError as e:
        print(f"Skipping invalid date entry: {cleaned_date}")

# Convert records into a DataFrame
df = pd.DataFrame(records)

# Add a "Month" and "Year" column for analysis
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# Group by month to calculate the average number of job posts
monthly_average = df.groupby('Month')['Job_Posts'].mean()

# Save the DataFrame to an Excel file
with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name="Original Data", index=False)
    monthly_average.to_excel(writer, sheet_name="Monthly Averages", index=True)

# Create a seasonal curve
plt.figure(figsize=(10, 6))
plt.plot(monthly_average.index, monthly_average.values, marker='o', linestyle='-', linewidth=2, color='blue')
plt.title("Seasonal Change in Job Postings", fontsize=16)
plt.xlabel("Month", fontsize=14)
plt.ylabel("Average Job Postings", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(range(1, 13), [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
], fontsize=10)
plt.tight_layout()

# Save the plot
plt.savefig(output_chart_path, bbox_inches="tight")
plt.show()

print(f"Results have been saved:\n- Data: {output_excel_path}\n- Chart: {output_chart_path}")
