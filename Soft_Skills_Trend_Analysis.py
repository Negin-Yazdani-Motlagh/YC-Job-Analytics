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

# Step 4: Calculate proportions
num_job_posts = num_job_posts_row.iloc[0, 1:]  # Extract the numJobPost row values
skills_df = df[df['Skill'] != 'numJobPost'].copy()  # Exclude the numJobPost row for calculation

# Compute proportions
for col in num_job_posts.index:
    skills_df[col] = skills_df[col] / num_job_posts[col]

skills_df = skills_df.round(2)  # Round proportions to 2 decimal places

# Save the updated DataFrame with proportions into an Excel file
output_file = r'C:\Users\negin\YC-Job-Analytics\result\soft_skills_occurrence_analysis_with_proportions.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    # Save original data
    df.to_excel(writer, sheet_name="Original Data", index=False)

    # Save proportions in another tab
    skills_df.to_excel(writer, sheet_name="Proportions", index=False)

    # Auto-adjust column widths
    workbook = writer.book
    for sheet_name, data in {"Original Data": df, "Proportions": skills_df}.items():
        worksheet = writer.sheets[sheet_name]
        for i, column in enumerate(data.columns):
            column_data = data[column].astype(str)
            max_length = max(column_data.map(len).max(), len(column))
            worksheet.set_column(i, i, max_length + 2)

print(f"Data with proportions has been saved to {output_file}")
