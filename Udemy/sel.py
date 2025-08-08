import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def load_cookies(driver, cookies_file):
    with open(cookies_file, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Skipping cookie {cookie['name']}: {e}")

def main():
    # 1. Set up browser
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)

    # 2. Go to Udemy and load cookies
    driver.get("https://www.udemy.com/")
    time.sleep(3)

    load_cookies(driver, "cookies.json")
    driver.refresh()
    time.sleep(3)

    # 3. Search for a course
    search_term = "Python automation"
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    # 4. Click on the first course in the list
    course_cards = driver.find_elements(By.CSS_SELECTOR, "a.udlite-custom-focus-visible.browse-course-card--link--3KIkQ")
    if course_cards:
        course_cards[0].click()
    else:
        print("No course found")
        return

    time.sleep(5)

    # 5. Navigate to curriculum section
    try:
        curriculum_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Show more')]")
        curriculum_button.click()
        time.sleep(3)
    except:
        pass  # In case the full curriculum is already shown

    # 6. Extract section titles and resources
    print("\n📚 Course Content and Resources:\n")
    sections = driver.find_elements(By.CSS_SELECTOR, "div.accordion-panel--panel--2Rel2")
    for section in sections:
        try:
            section_title = section.find_element(By.CLASS_NAME, "section--section-title--8blTh").text
            print(f"📘 {section_title}")
            lectures = section.find_elements(By.CLASS_NAME, "curriculum-item-link--title-container--3z3Sa")
            for lecture in lectures:
                lecture_title = lecture.text
                print(f"   🔹 {lecture_title}")
        except:
            continue

    input("\n✅ Done. Press Enter to exit and close browser.")
    driver.quit()

if __name__ == "__main__":
    main()
