import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# File paths
input_file = r'C:\Users\negin\YC-Job-Analytics\result\Nested_Job_Posts.json'
soft_skills_file = r'C:\Users\negin\Neginn\AI&Education\Excell\Dictionary of soft skills.xlsx'
output_chart_file = r'C:\Users\negin\YC-Job-Analytics\result\soft_skills_proportion_chart.png'

# Load the nested JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the dictionary of soft skills from Excel
soft_skills_df = pd.read_excel(soft_skills_file)
soft_skills = set(soft_skills_df.stack().str.lower().dropna().tolist())  # Flatten and convert to lowercase

# Initialize data structures
dates = []
proportions = []

# Iterate through each month-year in the data
for month_year, details in data["YC"].items():
    try:
        # Extract and clean the date (e.g., "Ask HN Who is Hiring April 2011" -> "April 2011")
        cleaned_date = " ".join(month_year.split()[-2:])

        # Convert "Month Year" format to a datetime object
        date = datetime.strptime(cleaned_date, "%B %Y")

        # Total job posts
        total_job_posts = details.get("numJobPost", 0)

        # Count job posts mentioning at least one soft skill
        comments = details.get("comments", [])
        job_posts_with_soft_skills = sum(
            1 for comment in comments
            if any(skill in comment.lower() for skill in soft_skills)
        )

        # Calculate the proportion
        if total_job_posts > 0:
            proportion = job_posts_with_soft_skills / total_job_posts
            dates.append(date)
            proportions.append(proportion)

    except Exception as e:
        print(f"Skipping invalid entry for {month_year}: {e}")

# Ensure there is data to plot
if dates and proportions:
    # Sort the data by date
    sorted_dates, sorted_proportions = zip(*sorted(zip(dates, proportions)))

    # Plot the proportions over time
    plt.figure(figsize=(18, 9))
    plt.plot(sorted_dates, sorted_proportions, marker='o', linestyle='-', linewidth=2, color='blue')
    plt.title("Proportion of Job Posts Mentioning at Least One Soft Skill Over Time", fontsize=16)
    plt.xlabel("Date (Month and Year)", fontsize=14)
    plt.ylabel("Proportion (Job Posts with Soft Skills / Total Job Posts)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(sorted_dates, [date.strftime("%b %Y") for date in sorted_dates], rotation=90, fontsize=10)
    plt.tight_layout()

    # Save the chart
    plt.savefig(output_chart_file, bbox_inches="tight")
    plt.show()

    print(f"Chart saved to '{output_chart_file}'")
else:
    print("No valid data available to plot.")
