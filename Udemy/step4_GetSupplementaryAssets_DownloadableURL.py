import requests
import pandas as pd
import os
import json

# === CONFIGURATION ===
base_folder = r"C:\Users\giris\source\repos\nseDemoUemyPythonProject\Udemy\udemyDownloads"
input_file = os.path.join(base_folder, "udemy_supplementary_files.xlsx")
output_file = os.path.join(base_folder, "udemy_resources.xlsx")
auth_file = "Authentication.json"  # contains {"access_token": "XXXX"}

# === Load Auth Token ===
with open(auth_file, "r") as f:
    auth_data = json.load(f)
ACCESS_TOKEN = auth_data.get("access_token")

# === Headers & Cookies ===
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US",
    "x-requested-with": "XMLHttpRequest",
    "x-udemy-cache-brand": "INen_US",
    "x-udemy-cache-language": "en",
    "x-udemy-cache-logged-in": "1",
    "x-udemy-cache-marketplace-country": "IN",
    "x-udemy-cache-price-country": "IN",
    "x-udemy-cache-user": "256172910"
}

cookies = {
    "access_token": ACCESS_TOKEN
}

# === Step 1: Read Input Excel (Col A, B, C) ===
df_input = pd.read_excel(input_file, usecols="A:C", skiprows=1, names=["CourseId", "LectureId", "SupplementaryAssetId"])

# === Step 2: Fetch download URLs ===
results = []

for _, row in df_input.iterrows():
    courseId = int(row["CourseId"])
    lectureId = int(row["LectureId"])
    supplementaryAssetId = int(row["SupplementaryAssetId"])

    url = f"https://www.udemy.com/api-2.0/users/me/subscribed-courses/{courseId}/lectures/{lectureId}/supplementary-assets/{supplementaryAssetId}/?fields[asset]=download_urls"

    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code == 200:
        data = response.json()
        file_url = None
        try:
            file_url = data["download_urls"]["File"][0]["file"]
        except KeyError:
            try:
                file_url = data["asset"]["download_urls"]["File"][0]["file"]
            except Exception:
                pass

        if file_url:
            results.append({
                "CourseId": courseId,
                "LectureId": lectureId,
                "SupplementaryAssetId": supplementaryAssetId,
                "Download URL": file_url
            })
            print(f"✅ Found file for Course {courseId} | Lecture {lectureId} | Asset {supplementaryAssetId}")
        else:
            print(f"⚠️ No file URL for Course {courseId} | Lecture {lectureId} | Asset {supplementaryAssetId}")
    else:
        print(f"❌ Failed {courseId}-{lectureId}-{supplementaryAssetId}: {response.status_code}")

# === Step 3: Export Results to Excel ===
if results:
    df_output = pd.DataFrame(results)
    df_output.to_excel(output_file, index=False)
    print(f"✅ Exported {len(results)} download URLs to {output_file}")
else:
    print("⚠️ No downloadable files found.")
