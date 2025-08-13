import time
import pickle
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


class CookieManager:
    def __init__(self, url="https://www.nseindia.com/", cookie_pkl="nseIndiaCookies.pkl"):
        self.url = url
        self.cookie_pkl = cookie_pkl
        self.driver = None

    def _init_driver(self):
        """Initialize the Selenium Chrome driver in headless mode."""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")

            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
        except WebDriverException as e:
            print(f"❌ Failed to initialize Chrome driver: {e}")
            raise

    def fetch_cookies(self):
        """Load cookies if they exist, otherwise fetch from the website."""
        try:
            self._init_driver()

            if os.path.exists(self.cookie_pkl):
                self.driver.get(self.url)
                with open(self.cookie_pkl, "rb") as file:
                    cookies = pickle.load(file)
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
                self.driver.get(self.url)
                print("✅ Cookies loaded from file.")
            else:
                cookies = self._fetch_and_save()

            # Ensure cookies are present
            current_cookies = self.driver.get_cookies()
            if not current_cookies:
                print("⚠ No cookies detected — retrying fetch.")
                current_cookies = self._fetch_and_save()

            return self._save_cookies(current_cookies)

        except Exception as e:
            print(f"❌ Error fetching cookies: {e}")
            return {}

        finally:
            if self.driver:
                self.driver.quit()

    def _fetch_and_save(self):
        """Visit the URL and save fresh cookies."""
        self.driver.get(self.url)
        time.sleep(5)  # allow page load
        cookies = self.driver.get_cookies()
        with open(self.cookie_pkl, "wb") as file:
            pickle.dump(cookies, file)
        print("✅ Cookies fetched and saved to PKL.")
        return cookies

    def _save_cookies(self, cookies):
        """Save cookies in both full JSON and name-value JSON formats."""
        try:
            # Full cookies
            with open("nseIndiaCookies.json", "w") as json_file:
                json.dump(cookies, json_file, indent=4)

            # Name-value only
            cookies_name_value = {cookie["name"]: cookie["value"] for cookie in cookies}
            with open("nseIndiaCookies_name_value.json", "w") as json_file:
                json.dump(cookies_name_value, json_file, indent=4)

            print("📄 Cookies saved to JSON files.")
            return cookies_name_value

        except Exception as e:
            print(f"❌ Error saving cookies: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    cm = CookieManager()
    cookie_dict = cm.fetch_cookies()
    print("Returned cookie dict:", cookie_dict)
