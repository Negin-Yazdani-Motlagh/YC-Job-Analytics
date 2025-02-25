import json
import pandas as pd
import re

# File paths
soft_skills_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Dictionary of soft skills (9).xlsx"
job_posts_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Feb_Nested_Job_Posts.json"
output_json_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\All_Months_Soft_Skills_Counts.json"

# Load the soft skills dictionary
soft_skills_df = pd.read_excel(soft_skills_path)
soft_skills_dict = {}

# Create mapping from subcategories to head categories
for _, row in soft_skills_df.iterrows():
    subcategory = str(row["Subcategory"]).strip().lower()  # Convert to lowercase for matching
    head_category = str(row["Headcategory"]).strip()
    soft_skills_dict[subcategory] = head_category

# Load job posts JSON
with open(job_posts_path, "r", encoding="utf-8") as f:
    job_data = json.load(f)

# Extract all available months
all_results = []

for month, data in job_data["YC"].items():
    print(f"Processing: {month}")

    job_posts = data.get("comments", [])
    head_category_counts = {}

    # Process each job post
    for job in job_posts:
        job_text = job.lower()  # Convert text to lowercase for matching
        seen_categories = set()

        # Check if any subcategory exists in the job description
        for skill, category in soft_skills_dict.items():
            if skill in job_text:
                seen_categories.add(category)

        # Count each head category only once per job post
        for category in seen_categories:
            head_category_counts[category] = head_category_counts.get(category, 0) + 1

    # Store results for the current month
    all_results.append({
        "month": month,
        "year": re.search(r"(\d{4})", month).group(1) if re.search(r"(\d{4})", month) else "Unknown",
        "total_job_posts": len(job_posts),
        "soft_skills_analysis": [{"head_category": cat, "count": count} for cat, count in head_category_counts.items()]
    })

# Sort results by year and month
def sort_months(item):
    month_order = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    match = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})", item["month"])
    if match:
        return (int(match.group(2)), month_order[match.group(1)])
    return (9999, 13)  # Put unknown dates at the end

all_results.sort(key=sort_months)

# Save the results as JSON
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=4)

print(f"Saved all months' results to {output_json_path}")
