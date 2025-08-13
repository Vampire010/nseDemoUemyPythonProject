import requests
import json
from openpyxl import Workbook


# === Load access token from Authentication.json ===
with open("Authentication.json", "r") as f:
    auth_data = json.load(f)
ACCESS_TOKEN = auth_data.get("access_token")

COURSE_ID = 397068  # Replace with actual course ID

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

url = f"https://www.udemy.com/api-2.0/courses/{COURSE_ID}/subscriber-curriculum-items/?page_size=1000"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("❌ Failed to fetch data:", response.status_code)
    exit()

data = response.json()

current_section = None
section_count = 0
lesson_count = 0
section_lesson_count = 0
section_duration = 0
section_index = 0

for item in data.get("results", []):
    item_type = item.get("_class")
    title = item.get("title")
    duration = item.get("asset", {}).get("time_estimation", 0)  # in seconds
    duration_min = f"{duration // 60}min" if duration else ""

    # If it's a section
    if item_type == "chapter":
        if current_section:
            print(f"\n    🔹 {section_lesson_count} / {section_lesson_count} | ⏱ {section_duration}min")
        section_index += 1
        section_lesson_count = 0
        section_duration = 0
        current_section = title
        print(f"\n▶ Section {section_index}: {title}")
    elif item_type == "lecture":
        section_lesson_count += 1
        lesson_count += 1
        section_duration += duration // 60
        # Simulated checkmark for published items (use real progress API if needed)
        check = "✔"
        print(f"  {check} {lesson_count}. {title}  ⏱ {duration_min}")

# Print summary for last section
print(f"\n    🔹 {section_lesson_count} / {section_lesson_count} | ⏱ {section_duration}min")
