import json
import pandas as pd
from collections import defaultdict
import re
from tqdm import tqdm  # Progress bar

# Define file paths
dictionary_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Dictionary of soft skills (9).xlsx"
job_posts_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Feb_Nested_Job_Posts.json"
output_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Headcategory_Counts_All_Occurrences_V9.json"

# Load the soft skills dictionary (V9)
df = pd.read_excel(dictionary_file)

# Convert dictionary to a lookup format
soft_skills_mapping = {}
for _, row in df.iterrows():
    headcategory = str(row['Headcategory']).strip() if pd.notna(row['Headcategory']) else "Unknown"
    skill = str(row['Subcategory']).strip().lower() if pd.notna(row['Subcategory']) else None

    if skill:
        soft_skills_mapping[skill] = headcategory

# Precompile regex patterns
compiled_patterns = {skill: re.compile(rf'\b{re.escape(skill)}\b', re.IGNORECASE) for skill in soft_skills_mapping}

# Load the job postings JSON file
with open(job_posts_file, "r", encoding="utf-8") as f:
    job_posts = json.load(f)

# Initialize dictionary to store counts by date
date_wise_counts = {}

# Function to extract **ALL occurrences** of soft skills from text
def extract_skills(text):
    skill_counts = defaultdict(int)
    text_lower = text.lower()[:5000]  # Limit text processing for efficiency

    # Count all occurrences per soft skill
    for skill, pattern in compiled_patterns.items():
        matches = pattern.findall(text_lower)  # Find all occurrences
        if matches:
            skill_counts[soft_skills_mapping[skill]] += len(matches)  # Add all occurrences

    return skill_counts

# Function to process a single date's job posts
def process_date(date, data):
    if "comments" not in data:
        return date, {}

    headcategory_counts = defaultdict(int)

    # Process each job post under the respective date
    for job_text in data["comments"]:
        matched_categories = extract_skills(job_text)

        # Count **all occurrences** of each skill
        for category, count in matched_categories.items():
            headcategory_counts[category] += count  # Add full count

    return date, dict(headcategory_counts)

# Processing job posts
results = []
for item in tqdm(job_posts["YC"].items(), total=len(job_posts["YC"]), desc="Processing Dates"):
    results.append(process_date(item[0], item[1]))

# Convert results into a dictionary
date_wise_counts = dict(results)

# Convert results to JSON format
result_json = {"HeadcategoryCountsByDate": date_wise_counts}

# Save the results
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result_json, f, indent=4)

# Convert to DataFrame and fill NaN with 0 for display
result_df = pd.DataFrame.from_dict(date_wise_counts, orient="index").fillna(0)

# Display cleaned DataFrame with summary stats
print(result_df.head())  # Show first few rows
print(f"Results saved to {output_file}")
