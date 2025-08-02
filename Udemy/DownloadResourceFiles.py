import os
import re
import requests

def sanitize(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

ACCESS_TOKEN = 'qRD3K7gMIf+phY7p+ZWfqlNkVKSYv4en9+SGNu+S04Y:g+C7av1pzqNxwxmJPEPQMGH9ebqHRxNR6QG8nSy8xHw'
COURSE_ID = 397068  # Replace with your actual course ID



headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json, text/plain, */*"
}

# Sanitize folder and file names for Windows
def clean(name):
    return re.sub(r'[<>:"/\\|?*]', '', name)

# Udemy curriculum API
url = f"https://www.udemy.com/api-2.0/courses/{COURSE_ID}/subscriber-curriculum-items/?page_size=1000"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("❌ Failed to get curriculum:", response.status_code, response.text)
    exit()

data = response.json().get("results", [])

current_section = ""
section_index = 0
lecture_index = 0

for item in data:
    if item["_class"] == "chapter":
        section_index += 1
        lecture_index = 0
        current_section = f"Section {section_index:02d} - {clean(item['title'])}"
        os.makedirs(current_section, exist_ok=True)

    elif item["_class"] == "lecture":
        lecture_index += 1
        lecture_title = clean(item["title"])
        lecture_number = f"{lecture_index:02d}"

        # Check for supplementary assets (resources)
        asset_info = item.get("asset", {})
        resources = asset_info.get("supplementary_assets", [])

        for res in resources:
            file_name = clean(res["filename"])
            download_url = res.get("download_url")
            full_file_name = f"{lecture_number} - {lecture_title} - {file_name}"
            path = os.path.join(current_section, full_file_name)

            # Skip if already downloaded
            if os.path.exists(path):
                print(f"✅ Already exists: {path}")
                continue

            # Download and save
            print(f"⬇️ Downloading: {full_file_name}")
            try:
                r = requests.get(download_url, headers=headers)
                with open(path, "wb") as f:
                    f.write(r.content)
                print(f"✅ Saved to: {path}")
            except Exception as e:
                print(f"❌ Error downloading {file_name}: {e}")