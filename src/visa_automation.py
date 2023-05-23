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
    # visa_automation = VisaAutomation()
    # visa_automation.get_visa_site()
    # visa_automation.login()
    # cookie_token = visa_automation.get_access_token()
    # print(cookie_token)
    # visa_automation.quit_driver()
    # visa_automation.check_availability(cookie_token)

    url = "https://ais.usvisa-info.com/pt-br/niv/schedule/44103952/appointment/days/55.json?appointments\\[expedite\\]=false"

    payload = {}
    headers = {
    # 'Accept': 'application/json, text/javascript, */*; q=0.01',
    # 'Accept-Language': 'pt-BR,pt;q=0.7',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    'Cookie': '_yatri_session=RjE5Tkc4SWNqUjFML1hMM0tpb2s4WTBBdFR6OEJoS0ZBQnlIMXIzNVVKVGZGdEFkRU9mZXFVamN1djVhSkp1NmR2OWtnclY4VWtlUzI0UllmUWIyNHM0enZ3YmNQUGp0OGZ4T0wvQlRtTFZlVCsvNlRNTUtyLzk5dzBFUEdZT256cmswUS9WbUJxSjB0R2NaNDJUNGFjVmp3OEhSNUMwSGdocnVCTUl1WFB2M3U0REpERHhmQmJwZmJKbTZhNk56aWdiMG8rNzJIVVJwL2pzeEJHWGU1NFFGL1l2aEcyd2NVL3YzaE1YRXFsRFlGZUsydFhGWkU1ZEU3WnNEZS9UUTNrTkRMZU0rZHgxSi80QXFQbU1TQndzOTVvR2wzZE1yZDk4VW1rM0tFOUoxSVlXZGZBaWlWY2pidm9qN3I0WHpVV3EvMEdKeDk1TlNGTzIzZFBaVHhJMTRob3ljQVNoTmt0RTFsZWRvaWp5MWpwSUJjZG5ZVzNJaWR6d2pXdGIxd0k1U0E0Q0FJWWNUczVjcVpkQ3lsaUN5RzUzT1BoQ0VhRllpbjRxbE9lUDNROFZPb2pQbGRTVXF6Ukp2dVVwcm5qQi8rd3p6a2d5ajVWV0ozTmZNeHlnSysrRnNOKzRaUVZRQ1owZ1Zic0hIWlViSWdNRDFjOThnenZwVW9yTW0rNER3N3dPanVmODFqNW42OGJXeVJoS2Zsd3dBN0dzQUdrejM0VllvN0NzPS0tdk4zMGZWVHNidTIvNHE2bmFMa0dDUT09--aa9cd843405bbc9fd722dbef823e84072ca01acf; _yatri_session=VUhlZEl6ZkFRMDZVOVlJL3lLNnpaVksyY1RiMzcvWmc0QWVIR1dBVDNqbzlVM2IrYWFsZmlZTmVsbEFrTzU0OTdHNklIUXJsaDRZUGlXZExLNStUdE5NVE5hekpWNmNOcklUYkl0QW45eXhCcVpYcGFVK1E0VEZCckxaNVpnK3NSaXJ4SzNRTWc0Z3BzbmhZMnEwVkxHVjFhd1JVNGhIMnFmUjRIVVRjTHA1cVFRdW1uN0RGWlZOTFhwSk1Gemp3N1RrZWkzeC8yMW8yL3BUdTMrcHd6V3I0eFliSHRGU1NPWmpTZGxhT3crUUh6R1Zmd0d3LzRyUlZGSDRiWmtLcDJGeEk1dW9JbXdnemI0dUtvalVqZDNZNUFlQ0d0MDkvNy9pRURya0tFaTIxdHN0U2pRYmdiUlJKZkt1aHd5K3BiRGZPTm9qUlFUWUF2N0dVSUpPeXU2TGlXUG9ieFQwWWVSWE95Rm1ZK3U2SkpSQXZGRWx0bS9Nc3NTaGxrRkI3dERvWnozT1gzSXl6VktEelRpU1NnVm5WeEVBbVkrY25BdTN4b21zY0RadmkzWU44b0M4SkJJYkdvdXJOMjZBZ09wYlVxcE94YTZUTXJMbkF5cDhRQ20vN1VOQ1pjOE1DVVBUVWY2cVUraXpOdklxcUZ2cEZyT1NYQXJldGd1VXhScnp0NFpyUnJiUHJLQUZxN1B3WEpuVmRBVisxVWh5bDlWSEdoSVBsMUJNPS0tOTRHajRiRmZVUHdHT1dBOXp2MThOZz09--ff630ef44818808409d495769ffa88169671316e',
    # 'Pragma': 'no-cache',
    # 'Referer': 'https://ais.usvisa-info.com/pt-br/niv/schedule/44103952/appointment?utf8=%E2%9C%93&applicants%5B%5D=51301421&applicants%5B%5D=54109027&applicants%5B%5D=54109378&applicants%5B%5D=54109436&applicants%5B%5D=54109561&confirmed_limit_message=1&commit=Continuar',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    # 'X-CSRF-Token': 'Jp0m/hhpth0U5zukTA9I6AhLGE5E63hLi0XRFAIK4GHSJb69I5y4XZB+NPjUsKMkcOhXtf+nata+WhslmG7Wow==',
    'X-Requested-With': 'XMLHttpRequest',
    # 'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
