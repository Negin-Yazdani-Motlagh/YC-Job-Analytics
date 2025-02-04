import json
import pandas as pd
from collections import defaultdict, OrderedDict

# File paths
nested_posts_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\Json_YC\soft_skills_occurrence_analysis.json'
soft_skills_excel = r'C:\Users\negin\YC-Job-Analytics\Result_YC\Excel_YC\Dictionaries\Dictionary of soft skills (8).xlsx'
output_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\Json_YC\categorized_soft_skills_by_headcategory.json'

# Define month order for sorting
month_order = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

# Load the JSON dataset
with open(nested_posts_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the dictionary of soft skills
soft_skills_df = pd.read_excel(soft_skills_excel, sheet_name=0)  # Assuming the relevant data is in the first sheet
soft_skills_dict = defaultdict(list)

# Create a mapping of headcategories to subcategories
for _, row in soft_skills_df.iterrows():
    head_skill = str(row['Headcategory']).strip().lower()
    sub_skill = str(row['Subcategory']).strip().lower()
    soft_skills_dict[head_skill].append(sub_skill)

# Initialize the output structure
result = defaultdict(OrderedDict)

# Iterate through the JSON dataset and categorize
for year, months in data.items():
    for month, details in months.items():
        num_posts = details.get("numJobPost", 0)
        skills_count = defaultdict(int)

        for skill, count in details.items():
            if skill == "numJobPost":
                continue
            skill_lower = skill.lower()
            categorized = False

            for head_skill, sub_skills in soft_skills_dict.items():
                if skill_lower in sub_skills or skill_lower == head_skill:
                    skills_count[head_skill] += count
                    categorized = True
                    break

            # If skill is not mapped, consider it uncategorized
            if not categorized:
                skills_count["uncategorized"] += count

        # Save the categorized data
        result[year][month] = {**skills_count, "numJobPost": num_posts}

# Sort the data within each year by month order
for year in result:
    result[year] = OrderedDict(
        sorted(result[year].items(), key=lambda x: month_order.index(x[0]) if x[0] in month_order else float('inf'))
    )

# Save the result to a JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4)

print(f"Analysis complete. Results saved to '{output_file}'.")
