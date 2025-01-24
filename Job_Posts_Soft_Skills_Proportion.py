import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# File paths
input_file = r'C:\Users\negin\YC-Job-Analytics\result\Nested_Job_Posts.json'
soft_skills_file = r'C:\Users\negin\Neginn\AI&Education\Excell\Dictionary of soft skills.xlsx'
output_chart_file = r'C:\Users\negin\YC-Job-Analytics\result\soft_skills_pre_post_chatgpt_chart.png'

# Load the nested JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the dictionary of soft skills from Excel
soft_skills_df = pd.read_excel(soft_skills_file)
soft_skills = set(soft_skills_df.stack().str.lower().dropna().tolist())  # Flatten and convert to lowercase

# Initialize data structures
pre_dates = []
pre_proportions = []
post_dates = []
post_proportions = []

# ChatGPT launch date: November 2022
chatgpt_launch_date = datetime(2022, 11, 1)

# Iterate through each month-year in the data
for month_year, details in data["YC"].items():
    try:
        # Extract and clean the date (e.g., "Ask HN Who is Hiring April 2011" -> "April 2011")
        cleaned_date = " ".join(month_year.split()[-2:])
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

            # Separate data into pre- and post-ChatGPT
            if date < chatgpt_launch_date:
                pre_dates.append(date)
                pre_proportions.append(proportion)
            else:
                post_dates.append(date)
                post_proportions.append(proportion)

    except Exception as e:
        print(f"Skipping invalid entry for {month_year}: {e}")

# Plot pre- and post-ChatGPT data
plt.figure(figsize=(18, 9))

# Pre-ChatGPT
if pre_dates and pre_proportions:
    pre_sorted_dates, pre_sorted_proportions = zip(*sorted(zip(pre_dates, pre_proportions)))
    plt.plot(pre_sorted_dates, pre_sorted_proportions, marker='o', linestyle='-', linewidth=2, color='blue', label="Pre-ChatGPT")

# Post-ChatGPT
if post_dates and post_proportions:
    post_sorted_dates, post_sorted_proportions = zip(*sorted(zip(post_dates, post_proportions)))
    plt.plot(post_sorted_dates, post_sorted_proportions, marker='o', linestyle='-', linewidth=2, color='green', label="Post-ChatGPT")

# Customize the plot
plt.title("Proportion of Job Posts Mentioning at Least One Soft Skill (Pre vs Post ChatGPT)", fontsize=16)
plt.xlabel("Date (Month and Year)", fontsize=14)
plt.ylabel("Proportion (Job Posts with Soft Skills / Total Job Posts)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(pre_sorted_dates + post_sorted_dates, 
           [date.strftime("%b %Y") for date in pre_sorted_dates + post_sorted_dates], 
           rotation=90, fontsize=10)
plt.legend(fontsize=14)
plt.tight_layout()

# Save the chart
plt.savefig(output_chart_file, bbox_inches="tight")
plt.show()

print(f"Chart saved to '{output_chart_file}'")
