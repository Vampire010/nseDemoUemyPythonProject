import requests
from openpyxl import load_workbook
from docx import Document

# Load Excel file
excel_file = "udemy_courses.xlsx"
wb = load_workbook(excel_file)
ws = wb.active

# Word document setup
document = Document()
document.add_heading("Udemy Course Curriculums", level=1)

# Cookies and headers setup
cookies = {
    "access_token": "qRD3K7gMIf+phY7p+ZWfqlNkVKSYv4en9+SGNu+S04Y:g+C7av1pzqNxwxmJPEPQMGH9ebqHRxNR6QG8nSy8xHw",
    "client_id": "bd2565cb7b0c313f5e9bae44961e8db2",
    "csrf": "cJ0qnLjwfnaYxnxuntf7AbwC86JQGxy0"
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': '; '.join([f"{key}={value}" for key, value in cookies.items()])
}

# Iterate over column B from row 2 to the last row with data
for row in range(2, ws.max_row + 1):
    course_id = ws[f"B{row}"].value
    course_name = ws[f"C{row}"].value
    if not course_id:
        continue  # Skip empty cells

    print(f"📘 Fetching Course ID: {course_id}" + " " +f"{course_name}")
    document.add_page_break()
    document.add_heading(f"Course ID: {course_id}" + " " +f"{course_name}", level=2)

    # Build API URL
    url = f"https://www.udemy.com/api-2.0/courses/{course_id}/subscriber-curriculum-items/?" \
          "curriculum_types=chapter,lecture,practice,quiz,role-play&page_size=200" \
          "&fields[lecture]=title,object_index,is_published,sort_order,created,asset,supplementary_assets,is_free" \
          "&fields[quiz]=title,object_index,is_published,sort_order,type" \
          "&fields[practice]=title,object_index,is_published,sort_order" \
          "&fields[chapter]=title,object_index,is_published,sort_order" \
          "&fields[asset]=title,filename,asset_type,status,time_estimation,is_external" \
          "&caching_intent=True"

    # Request Udemy API
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        document.add_paragraph(f"❌ Failed to fetch course. Status: {response.status_code}")
        continue

    data = response.json()
    section_count = 0
    lecture_count = 0

    for item in data.get('results', []):
        if item['_class'] == 'chapter':
            section_count += 1
            lecture_count = 0
            section_title = f"Section {section_count:02d} - {item['title']}"
            document.add_heading(section_title, level=3)
        elif item['_class'] == 'lecture':
            lecture_count += 1
            lecture_title = f"{lecture_count:02d} - {item['title']}"
            document.add_paragraph(lecture_title)

            # Add supplementary resources
            if item.get('supplementary_assets'):
                for asset in item['supplementary_assets']:
                    resource_title = asset.get('title', 'Untitled Resource')
                    document.add_paragraph(f"Resource: {resource_title}")

print("\n💾 Saving all course details into Word file...")
output_file = "all_udemy_courses_curriculum.docx"
document.save(output_file)
print(f"✅ Word file saved: {output_file}")
