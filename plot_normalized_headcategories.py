import json
import pandas as pd
import matplotlib.pyplot as plt

# File paths
input_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\Json_YC\categorized_soft_skills_by_headcategory.json'
output_folder = r'C:\Users\negin\YC-Job-Analytics\Result_YC\Headcategory_Plots'

# Load JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare data for plotting
time_series_data = []
for year, months in data.items():
    if year.isdigit():
        for month, categories in months.items():
            for headcategory, count in categories.items():
                if headcategory != "numJobPost":
                    time_series_data.append({
                        "Year": int(year),
                        "Headcategory": headcategory,
                        "Count": count
                    })

# Convert to DataFrame
df = pd.DataFrame(time_series_data)

# Group data by year and headcategory
df_grouped = df.groupby(["Year", "Headcategory"]).sum().reset_index()

# Calculate normalized percentages by year
df_grouped["Total"] = df_grouped.groupby("Year")["Count"].transform("sum")
df_grouped["Percentage"] = (df_grouped["Count"] / df_grouped["Total"]) * 100

# Plot each headcategory separately
headcategories = df_grouped["Headcategory"].unique()
for headcategory in headcategories:
    df_head = df_grouped[df_grouped["Headcategory"] == headcategory]

    # Plot the data
    plt.figure(figsize=(10, 6))
    pre_ai = df_head[df_head["Year"] <= 2022]
    post_ai = df_head[df_head["Year"] > 2022]

    # Plot pre-2022 in default color and post-2022 in green
    plt.plot(pre_ai["Year"], pre_ai["Percentage"], label="Pre-2022", color="blue")
    plt.plot(post_ai["Year"], post_ai["Percentage"], label="Post-2022", color="green")

    plt.title(f"Trend for {headcategory}")
    plt.xlabel("Year")
    plt.ylabel("Percentage of Mentions")
    plt.xticks(range(df_grouped["Year"].min(), df_grouped["Year"].max() + 1), rotation=45)
    plt.legend()
    plt.grid(True)

    # Save the plot
    output_file = f"{output_folder}/{headcategory}_normalized_headcategories_trends.png"
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

print(f"Plots saved to: {output_folder}")
