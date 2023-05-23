from dotenv import load_dotenv
import time
import os

from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import requests


CITY_IDS = {
    "SP": 56,
    "POA": 128,
    "BRA": 54,
    "REC": 57,
    "RJ": 55
}

load_dotenv(".env")

class VisaAutomation:

    def __init__(self):
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.driver = self.get_chrome_driver()

    def get_chrome_driver(self) -> Chrome:
        options = ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-browser-side-navigation")
        driver = Chrome(options=options)
        return driver

    def get_visa_site(self) -> None:
        self.driver.get("https://ais.usvisa-info.com/pt-br/niv/users/sign_in")

    def login(self):
        self.driver.find_element(By.ID, "user_email").send_keys(self.email)
        self.driver.find_element(By.ID, "user_password").send_keys(self.password)
        policy_check = self.driver.find_element(By.ID, "policy_confirmed")
        actions = ActionChains(self.driver)
        actions.move_to_element(policy_check).click().perform()
        self.driver.find_element(By.NAME, "commit").click()

    def get_access_token(self):
        access_cookie = self.driver.get_cookie("_yatri_session")
        return access_cookie
    
    def quit_driver(self):
        self.driver.quit()
    
    def check_availability(self, access_cookie) -> bool:
        headers = {
            "Cookie": f"{access_cookie['name']}={access_cookie['value']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        print(headers)
        
        for city in CITY_IDS:

            url = f"https://ais.usvisa-info.com/pt-br/niv/schedule/44103952/appointment/days/{CITY_IDS[city]}.json?appointments\[expedite\]=false"
            print(url)

            response = requests.get(url,
                                    headers=headers)
            print(response.json())


if __name__ == "__main__":
    visa_automation = VisaAutomation()
    visa_automation.get_visa_site()
    visa_automation.login()
    cookie_token = visa_automation.get_access_token()
    print(cookie_token)
    visa_automation.quit_driver()
    visa_automation.check_availability(cookie_token)
