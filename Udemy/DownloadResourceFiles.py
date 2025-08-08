import requests

# Load cookies from file (you can also copy paste your Cookie header manually here if needed)
cookies = {
    "access_token": "qRD3K7gMIf+phY7p+ZWfqlNkVKSYv4en9+SGNu+S04Y:g+C7av1pzqNxwxmJPEPQMGH9ebqHRxNR6QG8nSy8xHw",
    "client_id": "bd2565cb7b0c313f5e9bae44961e8db2",
    "csrf": "cJ0qnLjwfnaYxnxuntf7AbwC86JQGxy0"
    # Add cf_clearance, __cf_bm if needed
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': '; '.join([f"{key}={value}" for key, value in cookies.items()])
}

url = "https://www.udemy.com/api-2.0/courses/397068/subscriber-curriculum-items/?curriculum_types=chapter,lecture,practice,quiz,role-play&page_size=200&fields[lecture]=title,object_index,is_published,sort_order,created,asset,supplementary_assets,is_free&fields[quiz]=title,object_index,is_published,sort_order,type&fields[practice]=title,object_index,is_published,sort_order&fields[chapter]=title,object_index,is_published,sort_order&fields[asset]=title,filename,asset_type,status,time_estimation,is_external&caching_intent=True"

response = requests.get(url, headers=headers)
data = response.json()

section_count = 0
lecture_count = 0

for item in data['results']:
    if item['_class'] == 'chapter':
        section_count += 1
        lecture_count = 0
        print(f"\nSection {section_count:02d} - {item['title']}")
    elif item['_class'] == 'lecture':
        lecture_count += 1
        print(f"  {lecture_count:02d} - {item['title']}")
        if item.get('supplementary_assets'):
            for asset in item['supplementary_assets']:
                print(f"    - Resource: {asset.get('title', 'Untitled Resource')}")
