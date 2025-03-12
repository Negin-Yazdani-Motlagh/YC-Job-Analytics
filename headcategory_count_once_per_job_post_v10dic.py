import json
import pandas as pd
import re
from collections import defaultdict, OrderedDict
from tqdm import tqdm  # For progress bar

# === FILE PATHS ===

dictionary_file = r"/Users/kriteeneup/Downloads/Dictionary of soft skills (10).xlsx"
job_posts_file = r"/Users/kriteeneup/Downloads/Feb_Nested_Job_Posts.json"

output_file = r"/Users/kriteeneup/Downloads/New_Negin_once_Headcategory_CountsByDate.json"

# === SORTING HELPERS ===
month_order = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

def extract_year_month(date_string):
    """
    Extract year and month from date string like 'Ask HN Who is Hiring April 2020'
    """
    parts = date_string.split()
    if len(parts) >= 6:
        month = parts[-2]
        year = parts[-1]
        return (int(year), month)
    return (9999, "ZZZ")

# === LOAD DICTIONARY ===
print("📚 Loading dictionary...")
df = pd.read_excel(dictionary_file)

# === BUILD MAPPING (All 3 Levels) ===
print("🔎 Mapping subcategory, third-level, and headcategory terms...")
soft_skills_mapping = {}

for _, row in df.iterrows():
    headcategory = str(row['Headcategory']).strip() if pd.notna(row['Headcategory']) else "Unknown"

    # Subcategory mapping
    sub_skill = str(row['Subcategory']).strip().lower() if pd.notna(row['Subcategory']) else None
    if sub_skill:
        soft_skills_mapping[sub_skill] = headcategory

    # Third-level classification mapping
    third_level_skill = str(row['Third-level classification']).strip().lower() if pd.notna(row['Third-level classification']) else None
    if third_level_skill:
        soft_skills_mapping[third_level_skill] = headcategory

    # Optionally include Headcategory itself (if you want to search directly for the headcategory word)
    headcategory_term = headcategory.strip().lower()
    if headcategory_term:
        soft_skills_mapping[headcategory_term] = headcategory

print(f"✅ Total unique search terms (all levels): {len(soft_skills_mapping)}")

# === COMPILE REGEX PATTERNS ===
compiled_patterns = {
    skill: re.compile(rf'\b{re.escape(skill)}\b', re.IGNORECASE)
    for skill in soft_skills_mapping
}

# === LOAD JOB POSTS ===
print("🗃️ Loading job posts...")
with open(job_posts_file, "r", encoding="utf-8") as f:
    job_posts = json.load(f)

# === PROCESS JOB POSTS ===
date_wise_counts = {}

def process_date(date, data):
    """
    Process one month worth of job posts, counting one occurrence of each headcategory per job post.
    """
    if "comments" not in data:
        print(f"⚠️ No comments found for date: {date}")
        return date, {}

    headcategory_counts = defaultdict(int)
    total_job_posts = data.get("numJobPost", len(data["comments"]))

    # Process each job post
    for job_text in data["comments"]:
        text_lower = job_text.lower()[:5000]  # Truncate text to 5000 chars for efficiency

        # Track headcategories found in this job post
        headcategories_found = set()

        # Search for ANY matching term that maps to headcategory
        for skill, pattern in compiled_patterns.items():
            if pattern.search(text_lower):  # If we find it in text
                headcategory = soft_skills_mapping[skill]
                headcategories_found.add(headcategory)

        # Count each headcategory ONCE per job post
        for category in headcategories_found:
            headcategory_counts[category] += 1

    # Store total job posts
    headcategory_counts["Total Job Posts"] = total_job_posts

    print(f"✅ Date: {date} - Job Posts: {total_job_posts} - Categories Found: {dict(headcategory_counts)}")

    return date, dict(headcategory_counts)

# === MAIN PROCESSING LOOP ===
print("🚀 Starting processing of dates...")
results = []
for date, data in tqdm(job_posts["YC"].items(), desc="Processing Dates"):
    processed_date, counts = process_date(date, data)
    results.append((processed_date, counts))

# === SORT THE RESULTS ===
sorted_dates = OrderedDict(
    sorted(
        results,
        key=lambda x: (extract_year_month(x[0])[0], month_order.get(extract_year_month(x[0])[1], 13))
    )
)

# === FINAL JSON ===
result_json = {"HeadcategoryCountsByDate": sorted_dates}

# === SAVE TO FILE ===
print(f"💾 Saving results to {output_file} ...")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result_json, f, indent=4)

print("✅ JSON generation complete!")
