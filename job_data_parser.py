import json
import pandas as pd
import re
import os

# File Paths (Update with actual JSON file path)
input_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Feb_Nested_Job_Posts.json"
output_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Extracted_Job_Posts.xlsx"

# Load the JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Regex patterns for extraction
title_pattern = r"(?i)(?:hiring|join|looking for|we are hiring|position:|role:|opening for)\s+([A-Za-z ]+)"
company_pattern = r"(?i)\b(?:at|for|join|with)\s+([A-Z][A-Za-z0-9&. -]+)"
salary_pattern = r'(?:USD\s*)?\$?\d{1,3}(?:,\d{3})*(?:[Kk]|\.\d+)?(?:-\$?\d{1,3}(?:,\d{3})*(?:[Kk]|\.\d+)?)?|\d+%|\$?\d{1,3}(?:,\d{3})*(?:[Kk]|\.\d+)?(?:-\$?\d{1,3}(?:,\d{3})*(?:[Kk]|\.\d+)?)?'
experience_pattern = r'(\d+)\+?\s?(?:years?|yrs)|\b(\d+-\d+)\s*y/o/e\b|\b(\d{1,2})\s*(?:to|-)\s*(\d{1,2})\s*(?:years?|yrs)\b'

def normalize_salary(salary_str):
    salary_str = salary_str.replace(",", "").upper()  # Remove commas and convert to uppercase
    
    if '%' in salary_str:  # Handle percentage salaries (e.g., "20% equity")
        return salary_str  # Keep it as is

    if '-' in salary_str:  # Handle salary ranges (e.g., "$80K-$120K")
        parts = salary_str.split('-')
        normalized_range = []
        for part in parts:
            num = re.sub(r'[^\d.]', '', part)  # Remove non-numeric characters
            num = float(num) * 1000 if 'K' in part else float(num)  # Convert K to full value
            normalized_range.append(num)
        return f"{normalized_range[0]:,.0f} - {normalized_range[1]:,.0f}"  # Format as "80,000 - 120,000"

    num = re.sub(r'[^\d.]', '', salary_str)  # Remove non-numeric characters
    num = float(num) * 1000 if 'K' in salary_str else float(num)  # Convert K to full value
    return f"{num:,.0f}"  # Format number

# Extracted job data list
extracted_jobs = []

# Loop through JSON data with correct date parsing
for category, year_data in data.items():  # Outer key category (e.g., "YC")
    for year_month, details in sorted(year_data.items(), key=lambda x: pd.to_datetime(x[0], errors='coerce')):
        match = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})", year_month)
        extracted_month, extracted_year = match.groups() if match else ("Unknown", "Unknown")
        
        for post in details.get("comments", []):  # Extract job descriptions from "comments"
            title_match = re.search(title_pattern, post)
            job_title = title_match.group(1).strip() if title_match else "Not Specified"

            company_match = re.search(company_pattern, post)
            company_name = company_match.group(1).strip() if company_match else "Not Specified"

            salaries = re.findall(salary_pattern, post)
            salaries = [s for s in salaries if "USD" in s.upper() or "$" in s or "%" in s]  # Filter relevant salaries
            normalized_salaries = [normalize_salary(s) for s in salaries if s]
            salary_range = ", ".join(normalized_salaries) if normalized_salaries else "Not Specified"

            experience_match = re.findall(experience_pattern, post)
            years_experience = ", ".join(filter(None, sum(experience_match, ()))) if experience_match else "Not Specified"

            extracted_jobs.append({
                "Year": extracted_year,
                "Month": extracted_month,
                "Job Title": job_title,
                "Company Name": company_name,
                "Salary Range": salary_range,
                "Required Experience (Years)": years_experience
            })

# Convert to DataFrame & Sort by Year and Month
df = pd.DataFrame(extracted_jobs)
df['Year'] = df['Year'].astype(str)
df['Month'] = pd.Categorical(df['Month'], categories=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], ordered=True)
df = df.sort_values(by=['Year', 'Month'])

# Save to Excel
df.to_excel(output_file, index=False)

print(f"✅ Extracted job details saved to: {output_file}")
