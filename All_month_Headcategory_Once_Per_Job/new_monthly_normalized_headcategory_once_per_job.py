import json
import pandas as pd
import re

# File Paths (Update with your locations)
soft_skills_path = r"/Users/kriteeneup/Downloads/Dictionary of soft skills (9).xlsx"
job_posts_path = r"/Users/kriteeneup/Downloads/Feb_Nested_Job_Posts.json"
output_json_path = r"/Users/kriteeneup/Downloads/All_Months_Soft_Skills_Counts.json"

# Load Soft Skills Dictionary
soft_skills_df = pd.read_excel(soft_skills_path)
soft_skills_dict = {}

# Create Mapping from Subcategories to Head Categories
for _, row in soft_skills_df.iterrows():
    subcategory = str(row["Subcategory"]).strip().lower()
    head_category = str(row["Headcategory"]).strip()
    soft_skills_dict[subcategory] = head_category

# Load Job Posts JSON
with open(job_posts_path, "r", encoding="utf-8") as f:
    job_data = json.load(f)

# Extract all available months
all_results = []
processed_months = 0

# Optimize Skill Matching by Pre-Compiling Regex Patterns
compiled_patterns = {skill: re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE) for skill in soft_skills_dict}

for month, data in job_data.get("YC", {}).items():
    processed_months += 1
    print(f"Processing {processed_months}: {month}")

    job_posts = data.get("comments", [])
    head_category_counts = {}

    # Process each job post
    for job in job_posts:
        job_text = job.lower()
        seen_head_categories = set()

        # Fast Matching: Only Check Necessary Patterns
        for skill, pattern in compiled_patterns.items():
            if pattern.search(job_text):
                seen_head_categories.add(soft_skills_dict[skill])

        # Count Each Head Category Only Once Per Job
        for category in seen_head_categories:
            head_category_counts[category] = head_category_counts.get(category, 0) + 1

    # Store results for the current month
    all_results.append({
        "month": month,
        "year": re.search(r"(\d{4})", month).group(1) if re.search(r"(\d{4})", month) else "Unknown",
        "total_job_posts": len(job_posts),
        "soft_skills_analysis": [{"head_category": cat, "count": count} for cat, count in head_category_counts.items()]
    })

# Sort Results by Year & Month
def sort_months(item):
    month_order = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    match = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})", item["month"])
    if match:
        return (int(match.group(2)), month_order[match.group(1)])
    return (9999, 13)

all_results.sort(key=sort_months)

# Save Results as JSON
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=4)

print(f"Successfully saved results to {output_json_path}")
