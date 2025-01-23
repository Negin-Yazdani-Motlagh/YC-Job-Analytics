import json
import pandas as pd
from collections import defaultdict, OrderedDict

# File paths
nested_posts_file = r'C:\Users\negin\YC-Job-Analytics\result\Nested_Job_Posts.json'
soft_skills_excel = r'C:\Users\negin\Neginn\AI&Education\Excell\Dictionary of soft skills.xlsx'
output_file = r'C:\Users\negin\YC-Job-Analytics\result\soft_skills_occurrence_analysis.json'

# Define month order for sorting
month_order = ["January", "February", "March", "April", "May", "June", "July", 
               "August", "September", "October", "November", "December"]

# Load the nested JSON dataset
with open(nested_posts_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the dictionary of soft skills
soft_skills_df = pd.read_excel(soft_skills_excel)
soft_skills = set(soft_skills_df.stack().str.lower().dropna().tolist())  # Flatten and convert to lowercase

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

        # Count occurrences of each soft skill in all comments
        skill_counts = {skill: 0 for skill in soft_skills}
        for comment in comments:
            comment_lower = comment.lower()
            for skill in soft_skills:
                skill_counts[skill] += comment_lower.count(skill)

        # Filter and sort skills by count (descending)
        filtered_skill_counts = dict(
            sorted(
                {skill: count for skill, count in skill_counts.items() if count > 0}.items(),
                key=lambda x: x[1],
                reverse=True
            )
        )

        # Save the results if there are any skills with occurrences
        if filtered_skill_counts:
            result[year][month] = {**filtered_skill_counts, "numJobPost": num_posts}

# Sort the data within each year by month order
for year in result:
    if isinstance(result[year], OrderedDict):  # Only sort year-month data
        result[year] = OrderedDict(
            sorted(result[year].items(), key=lambda x: month_order.index(x[0]) if x[0] in month_order else float('inf'))
        )

# Save the result to a JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4)

print(f"Analysis complete. Results saved to '{output_file}'.")
