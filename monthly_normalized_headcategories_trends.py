import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# File path to the JSON data
input_file = "C:/Users/negin/YC-Job-Analytics/Result_YC/February 2025/Feb_categorized_soft_skills_by_headcategory.json"
output_plot_file = "C:/Users/negin/YC-Job-Analytics/Result_YC/February 2025/Feb_all_headcategories_trends.png"

# Define month mapping for ordering
month_mapping = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

# Load JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare data storage
time_series_data = []

# Extract and normalize mentions for all headcategories (excluding "uncategorized")
for year, months in data.items():
    if year.isdigit():  # Ensure it's a valid year
        for month, categories in months.items():
            if isinstance(categories, dict) and month in month_mapping:  # Ensure valid month
                time_key = f"{year}-{month_mapping[month]}"  # Format YYYY-MM
                total_jobs = categories.get("numJobPost", 1)  # Avoid division by zero
                
                for category, count in categories.items():
                    if category not in ["numJobPost", "uncategorized"]:  # Exclude numJobPost & uncategorized
                        normalized_value = (count / total_jobs) * 100  # Convert to percentage
                        
                        # Store data
                        time_series_data.append({
                            "Time": time_key,
                            "Category": category,
                            "NormalizedCount": normalized_value
                        })

# Convert to DataFrame
df = pd.DataFrame(time_series_data)

# Convert 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m')

# Sort by Time for proper plotting
df = df.sort_values(by="Time")

# **DEBUG: Print unique years to confirm 2025 is included**
print("Years in dataset:", df['Time'].dt.year.unique())

# Plot trends for all headcategories
plt.figure(figsize=(16, 6))
sns.lineplot(data=df, x='Time', y='NormalizedCount', hue='Category', linewidth=2)

# Configure the plot
plt.title("Normalized Trends of Headcategories Over Time (Monthly)", fontsize=16)
plt.xlabel("Time (Year-Month)", fontsize=12)
plt.ylabel("Percentage of Mentions (%)", fontsize=12)

# Format X-axis for clarity (show every 6 months)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

# Rotate labels for better readability
plt.xticks(rotation=60, fontsize=10)

# Add grid lines
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show legend
plt.legend(title="Headcategories", bbox_to_anchor=(1.05, 1), loc='upper left')

# Improve layout
plt.tight_layout()

# Save and display the plot
plt.savefig(output_plot_file)
plt.show()

print(f"Plot saved to: {output_plot_file}")
