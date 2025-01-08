import time
import csv

import undetected_chromedriver as uc

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By


def get_driver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = False
    #chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent={}".format(user_agent))
    driver = uc.Chrome(options=chrome_options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
    )
    return driver

dings = "egal"
driver = get_driver()
driver.get("https://steamdb.info/app/271590/charts/#max")
driver.execute_script("window.localStorage.setItem('app-chart-show-twitch','1');")
driver.add_cookie({"name": "__Host-steamdb", "value": "0%3B7221802%3Bde20d46f3c07215a70e3bc66dc2b3b8908cd2d7e", "sameSite": "Lax", 'secure': True, 'httpOnly': True})
driver.refresh()
driver.implicitly_wait(10000000)
time.sleep(10)

try:
    dings = driver.execute_script('return window.Highcharts.charts[0].getCSV()')
    print(dings)
except Exception as e:
    driver.implicitly_wait(100000)
    print(e)

driver.implicitly_wait(100000)

driver.find_element(By.CLASS_NAME, "highcharts-exporting-group").click()

with open("gta5_steam_player_data_and_twitch_viewers.csv", "w") as text_file:
    text_file.write(dings)
