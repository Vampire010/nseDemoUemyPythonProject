import requests

# Your bearer token from browser cookies
ACCESS_TOKEN = 'qRD3K7gMIf+phY7p+ZWfqlNkVKSYv4en9+SGNu+S04Y:g+C7av1pzqNxwxmJPEPQMGH9ebqHRxNR6QG8nSy8xHw'

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

base_url = "https://www.udemy.com/api-2.0/users/me/subscribed-courses?page_size=50"
all_courses = []
course_count = 1  # start numbering from 1
page = 1 

while base_url:
    print(f"Fetching page {page}...")
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        all_courses.extend(results)

        # Print course titles and IDs with count
        for course in results:
            print(f"{course_count}. {course['title']} - {course['id']}")
            course_count += 1

        # Get next page URL
        base_url = data.get("next")
        page += 1
    else:
        print("Failed to fetch courses:", response.status_code, response.text)
        break

print(f"\n✅ Total courses fetched: {len(all_courses)}")
