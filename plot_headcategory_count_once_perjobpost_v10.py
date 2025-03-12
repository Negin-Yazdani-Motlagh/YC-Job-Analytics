import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# === Load JSON Data ===
with open(r"/Users/kriteeneup/Downloads/headcategory_count_once_perjobpost_v10.json"
, "r", encoding="utf-8") as f:
    data = json.load(f)

date_counts = data["HeadcategoryCountsByDate"]

# === Prepare Data ===
dates = []
headcategories = set()

# Collect all headcategories, excluding "Unknown" and blanks
for counts in date_counts.values():
    headcategories.update([
        key for key in counts.keys()
        if key not in ["Total Job Posts", "Unknown", None, "nan"]
    ])

# Initialize storage for normalized counts
counts_by_category = {cat: [] for cat in headcategories}

# Populate dates and normalized counts
for date, counts in sorted(date_counts.items(), key=lambda x: datetime.strptime(x[0].split()[-2] + " " + x[0].split()[-1], "%B %Y")):
    dt = datetime.strptime(date.split()[-2] + " " + date.split()[-1], "%B %Y")
    dates.append(dt)

    total_posts = counts.get("Total Job Posts", 1)
    for cat in headcategories:
        count = counts.get(cat, 0)
        percentage = (count / total_posts) * 100
        counts_by_category[cat].append(percentage)

# === Sort legend by latest data point ===
sorted_headcategories = sorted(
    headcategories,
    key=lambda cat: counts_by_category[cat][-1],
    reverse=True
)

# === Color Mapping (Fixed Category Name) ===
color_mapping = {
    'Interpersonal & Leadership Skills': '#1f77b4',  # Blue
    'Cognitive & Problem-Solving Skills': 'orange',  # Orange
    'Personal Effectiveness & Growth': 'green'       # Green
}

# === Plot ===
plt.figure(figsize=(18, 10))

# Plot each category
for cat in sorted_headcategories:
    color = color_mapping.get(cat, 'gray')  # Fallback to gray
    plt.plot(
        dates,
        counts_by_category[cat],
        label=cat,
        linewidth=1.5,
        color=color
    )

# === Plot Styling ===
plt.title("Normalized Soft Skill Headcategory Percentage (One Per Job Post)", fontsize=18)
plt.xlabel("Year", fontsize=16)
plt.ylabel("Percentage (%)", fontsize=16)

# Format X-axis with two-year intervals
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)

plt.grid(True, linestyle='--', alpha=0.6)

# === Legend Inside Plot ===
plt.legend(
    loc='upper right',
    fontsize=14,
    title="Headcategories (Sorted)",
    title_fontsize=15
)

plt.tight_layout()
plt.show()
