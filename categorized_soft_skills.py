import json
import pandas as pd
from collections import defaultdict, OrderedDict
import os

# File paths
nested_posts_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\Json_YC\Nested_Job_Posts.json'
soft_skills_excel = r'C:\Users\negin\YC-Job-Analytics\Result_YC\Excel_YC\Dictionaries\Dictionary of soft skills (8).xlsx'
output_file = r'C:\Users\negin\YC-Job-Analytics\result\categorized_soft_skills_analysis.json'

# Define month order for sorting
month_order = ["January", "February", "March", "April", "May", "June", "July", 
               "August", "September", "October", "November", "December"]

# Check if the nested JSON file exists
if not os.path.exists(nested_posts_file):
    raise FileNotFoundError(f"File not found: {nested_posts_file}")
else:
    print(f"File found: {nested_posts_file}")

# Check if the soft skills Excel file exists
if not os.path.exists(soft_skills_excel):
    raise FileNotFoundError(f"File not found: {soft_skills_excel}")
else:
    print(f"File found: {soft_skills_excel}")

# Load the nested JSON dataset
with open(nested_posts_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the dictionary of soft skills (columns: Headcategory and Subcategory)
soft_skills_df = pd.read_excel(soft_skills_excel)

# Print the columns to verify they are correctly loaded
print("Columns in Excel file:", soft_skills_df.columns)

# Create a dictionary mapping head categories to subcategories
soft_skills_dict = defaultdict(list)
for _, row in soft_skills_df.iterrows():
    # Skip rows with NaN in either column
    if pd.isna(row["Headcategory"]) or pd.isna(row["Subcategory"]):
        continue  # Skip this iteration

    # Process valid rows
    head_skill = row["Headcategory"].strip().lower()  # Ensure lowercase for matching
    sub_skill = row["Subcategory"].strip().lower()
    soft_skills_dict[head_skill].append(sub_skill)

# Initialize the output structure
result = defaultdict(OrderedDict)

# Iterate through the nested JSON structure
for key, value in data["YC"].items():
    # Extract year and month from the key
    parts = key.split()
    if len(parts) >= 3 and parts[-2] in month_order:
        month = parts[-2]
        year = parts[-1]
        if year not in result:
            result[year] = OrderedDict()
    else:
        # For "Who is Hiring Right Now", assign a placeholder year and month
        month = "Who is Hiring Right Now"
        year = "Other"
        if year not in result:
            result[year] = OrderedDict()

    if "comments" in value:
        comments = value["comments"]
        num_posts = value.get("numJobPost", len(comments))

        # Count occurrences of each head category via subcategories in comments
        head_skill_counts = defaultdict(int)
        for comment in comments:
            comment_lower = comment.lower()
            for head_skill, sub_skills in soft_skills_dict.items():
                for sub_skill in sub_skills:
                    if sub_skill in comment_lower:  # Check for sub-skill in comment
                        head_skill_counts[head_skill] += 1

        # Filter and sort head categories by count (descending)
        filtered_head_skill_counts = dict(
            sorted(
                {skill: count for skill, count in head_skill_counts.items() if count > 0}.items(),
                key=lambda x: x[1],
                reverse=True
            )
        )

        # Save the results if there are any skills with occurrences
        if filtered_head_skill_counts:
            result[year][month] = {**filtered_head_skill_counts, "numJobPost": num_posts}

# Sort the data within each year by month order
for year in result:
    if isinstance(result[year], OrderedDict):  # Only sort year-month data
        result[year] = OrderedDict(
            sorted(result[year].items(), key=lambda x: month_order.index(x[0]) if x[0] in month_order else float('inf'))
        )

# Ensure the output directory exists
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save the result to a JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4)

print(f"Analysis complete. Results saved to '{output_file}'.")
