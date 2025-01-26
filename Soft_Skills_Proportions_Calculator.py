import pandas as pd
import json

# File path for the JSON dataset
file_path = r'C:\Users\negin\YC-Job-Analytics\result\soft_skills_occurrence_analysis.json'

# Load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Convert JSON data into a DataFrame
skill_occurrence_dict = {}

# Extract the skills and their monthly counts
for year, months in data.items():
    for month, skills in months.items():
        period = f"{month} {year}"  # Combine month and year
        for skill, count in skills.items():
            if skill not in skill_occurrence_dict:
                skill_occurrence_dict[skill] = {}
            skill_occurrence_dict[skill][period] = count

# Convert the dictionary into a DataFrame
df = pd.DataFrame.from_dict(skill_occurrence_dict, orient='index').fillna(0)
df = df.reset_index().rename(columns={'index': 'Skill'})  # Reset index and rename columns

# Calculate proportions
num_job_posts = df[df['Skill'] == 'numJobPost'].iloc[0, 1:]  # Extract the numJobPost row
skills_df = df[df['Skill'] != 'numJobPost'].copy()  # Exclude the numJobPost row

# Compute proportions
for col in num_job_posts.index:
    skills_df[col] = skills_df[col] / num_job_posts[col]
skills_df = skills_df.round(2)  # Round proportions to 2 decimal places

# Save the results in a new Excel file
output_file = r'C:\Users\negin\YC-Job-Analytics\result\soft_skills_occurrence_analysis_with_proportions.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name="Original Data", index=False)  # Save original data
    skills_df.to_excel(writer, sheet_name="Proportions", index=False)  # Save proportions

    # Auto-adjust column widths
    workbook = writer.book
    for sheet_name, data in {"Original Data": df, "Proportions": skills_df}.items():
        worksheet = writer.sheets[sheet_name]
        for i, column in enumerate(data.columns):
            column_data = data[column].astype(str)
            max_length = max(column_data.map(len).max(), len(column))
            worksheet.set_column(i, i, max_length + 2)

print(f"Data with proportions has been saved to {output_file}")
