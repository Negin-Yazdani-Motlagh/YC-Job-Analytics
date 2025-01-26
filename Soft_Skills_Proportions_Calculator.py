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

# Step 1: Remove the column "Who is Hiring Right Now Other"
if "Who is Hiring Right Now Other" in df.columns:
    df = df.drop(columns=["Who is Hiring Right Now Other"])

# Step 2: Sort columns (years and months) in chronological order
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
sorted_columns = sorted(df.columns[1:], key=lambda x: (int(x.split()[-1]), month_order.index(x.split()[0])))
df = df[['Skill'] + sorted_columns]

# Step 3: Move the `numJobPost` row to the last row
num_job_posts_row = df[df['Skill'] == 'numJobPost']
df = df[df['Skill'] != 'numJobPost']  # Remove the numJobPost row
df = pd.concat([df, num_job_posts_row], ignore_index=True)  # Append numJobPost to the end

# Save the updated DataFrame into an Excel file
output_file = r'C:\Users\negin\YC-Job-Analytics\result\soft_skills_occurrence_analysis_with_proportions.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name="Original Data", index=False)  # Save original data

    # Auto-adjust column widths
    workbook = writer.book
    worksheet = writer.sheets["Original Data"]
    for i, column in enumerate(df.columns):
        column_data = df[column].astype(str)
        max_length = max(column_data.map(len).max(), len(column))
        worksheet.set_column(i, i, max_length + 2)

print(f"Data has been updated and saved to {output_file}")
