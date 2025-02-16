import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File path for the categorized headcategories dataset
input_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\Json_YC\categorized_soft_skills_by_headcategory.json'
output_plot_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\normalized_headcategories_trends.png'

# Load the categorized soft skills data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare the data for plotting
time_series_data = []
for year, months in data.items():
    if year.isdigit():  # Ignore non-year keys
        for month, categories in months.items():
            for headcategory, count in categories.items():
                if headcategory != "numJobPost":
                    time_series_data.append({
                        "Year": int(year),
                        "Headcategory": headcategory,
                        "Count": count
                    })

# Convert to a DataFrame
df = pd.DataFrame(time_series_data)

# Aggregate total occurrences of each headcategory per year
agg_df = df.groupby(['Year', 'Headcategory']).agg({'Count': 'sum'}).reset_index()

# Calculate total job post mentions per year
job_post_counts = df.groupby('Year')['Count'].sum().reset_index().rename(columns={'Count': 'TotalJobPosts'})

# Merge with total job post counts for normalization
agg_df = pd.merge(agg_df, job_post_counts, on='Year')

# Compute normalized count as a percentage of total job post mentions per year
agg_df['NormalizedCount'] = (agg_df['Count'] / agg_df['TotalJobPosts']) * 100  # Convert to percentage

# Plot normalized trends of headcategories over years
plt.figure(figsize=(16, 10))
sns.lineplot(data=agg_df, x='Year', y='NormalizedCount', hue='Headcategory', palette='tab10')

# Configure plot aesthetics
plt.title("Normalized Trends of Headcategories Over Years", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Percentage of Mentions", fontsize=12)
plt.legend(title="Headcategories", fontsize=10, title_fontsize=12, loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot
plt.savefig(output_plot_file)
plt.show()

print(f"Plot saved to: {output_plot_file}")
