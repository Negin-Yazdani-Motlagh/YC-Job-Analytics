import pandas as pd
import json

# File path for the input JSON file
file_path = r'C:\Users\negin\YC-Job-Analytics\result\soft_skills_occurrence_analysis.json'

# Load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Create a dictionary to store the results
skill_occurrence_dict = {}

# Iterate through the JSON structure
for year, months in data.items():
    for month, skills in months.items():
        period = f"{month} {year}"  # Combine month and year as a column header
        for skill, count in skills.items():
            if skill not in skill_occurrence_dict:
                skill_occurrence_dict[skill] = {}
            skill_occurrence_dict[skill][period] = count

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(skill_occurrence_dict, orient='index').fillna(0)

# Save the DataFrame to an Excel file
output_file = r'C:\Users\negin\YC-Job-Analytics\result\soft_skills_monthly_occurrence_restructured.xlsx'
df.to_excel(output_file, index=True, index_label="Skill")

print(f"Data has been saved to {output_file}")
