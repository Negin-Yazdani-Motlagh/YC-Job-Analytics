import json
import pandas as pd
import re
from collections import defaultdict, OrderedDict
from tqdm import tqdm  # Progress bar

# File paths
dictionary_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Dictionary of soft skills (10).xlsx"
job_posts_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Feb_Nested_Job_Posts.json"
output_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Headcategory_Counts_All_Occurrences_V10.json"

# Define month order for sorting
month_order = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

# Load the soft skills dictionary (V10)
df = pd.read_excel(dictionary_file)

# Convert dictionary to a lookup format (handling both subcategory and third-level classification)
soft_skills_mapping = {}
for _, row in df.iterrows():
    headcategory = str(row['Headcategory']).strip() if pd.notna(row['Headcategory']) else "Unknown"

    sub_skill = str(row['Subcategory']).strip().lower() if pd.notna(row['Subcategory']) else None
    third_level_skill = str(row['Third-level classification']).strip().lower() if pd.notna(row['Third-level classification']) else None

    if sub_skill:
        soft_skills_mapping[sub_skill] = headcategory
    if third_level_skill:
        soft_skills_mapping[third_level_skill] = headcategory

# Precompile regex patterns for efficiency
compiled_patterns = {skill: re.compile(rf'\b{re.escape(skill)}\b', re.IGNORECASE) for skill in soft_skills_mapping}

# Load the job postings JSON file
with open(job_posts_file, "r", encoding="utf-8") as f:
    job_posts = json.load(f)

# Initialize dictionary to store counts by date
date_wise_counts = {}

# Function to extract **all occurrences** of soft skills from text
def extract_skills(text):
    skill_counts = defaultdict(int)
    text_lower = text.lower()[:5000]  # Limit text processing for efficiency

    # Count all occurrences per soft skill
    for skill, pattern in compiled_patterns.items():
        matches = pattern.findall(text_lower)  # Find all occurrences
        if matches:
            skill_counts[soft_skills_mapping[skill]] += len(matches)  # Add all occurrences

    return skill_counts

# Function to extract year and month from the date key
def extract_year_month(date_string):
    parts = date_string.split()  # Example: "Ask HN Who is Hiring April 2011"
    if len(parts) >= 6:
        month = parts[-2]  # Second to last part should be the month
        year = parts[-1]   # Last part should be the year
        return (int(year), month)
    return (9999, "ZZZ")  # If format is unexpected, push it to the end

# Function to process a single date's job posts
def process_date(date, data):
    if "comments" not in data:
        return date, {}

    headcategory_counts = defaultdict(int)

    # Extract total number of job posts for the given date
    total_job_posts = data.get("numJobPost", 0)

    # Process each job post under the respective date
    for job_text in data["comments"]:
        matched_categories = extract_skills(job_text)

        # Count **all occurrences** of each skill
        for category, count in matched_categories.items():
            headcategory_counts[category] += count  # Add full count

    # Include total job posts in the output
    headcategory_counts["Total Job Posts"] = total_job_posts

    return date, dict(headcategory_counts)

# Processing job posts
results = []
for item in tqdm(job_posts["YC"].items(), total=len(job_posts["YC"]), desc="Processing Dates"):
    results.append(process_date(item[0], item[1]))

# Convert results into a dictionary
date_wise_counts = dict(results)

# Sort the data by year and month
sorted_dates = OrderedDict(
    sorted(date_wise_counts.items(), key=lambda x: (extract_year_month(x[0])[0], month_order.get(extract_year_month(x[0])[1], 13)))
)

# Convert results to JSON format
result_json = {"HeadcategoryCountsByDate": sorted_dates}

# Save the results
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result_json, f, indent=4)

# Convert to DataFrame and fill NaN with 0 for display
result_df = pd.DataFrame.from_dict(sorted_dates, orient="index").fillna(0)

# Display cleaned DataFrame with summary stats
import ace_tools as tools
tools.display_dataframe_to_user(name="All Soft Skill Occurrences V10", dataframe=result_df)

print(f"✅ All occurrences of soft skills saved to {output_file}")
