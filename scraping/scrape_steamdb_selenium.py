import time
import undetected_chromedriver as uc

from selenium import webdriver
from selenium_stealth import stealth

STEAM_LOGIN_COOKIE = "put_here"


def get_driver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = False
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent={}".format(user_agent))
    driver = uc.Chrome(options=chrome_options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver

player_result = ""
viewer_result = ""

driver = get_driver()
driver.get("https://steamdb.info/app/271590/charts/#max")
driver.execute_script("window.localStorage.setItem('app-chart-show-twitch','1');")
driver.add_cookie(
    {
        "name": "__Host-steamdb",
        "value": STEAM_LOGIN_COOKIE,
        "sameSite": "Lax",
        "secure": True,
        "httpOnly": True,
    }
)

driver.refresh()
driver.implicitly_wait(10000000)
time.sleep(10)

try:
    player_result = driver.execute_script("return window.Highcharts.charts[0].getCSV()")
except Exception as e:
    driver.implicitly_wait(100000)

try:
    viewer_result = driver.execute_script("return window.Highcharts.charts[1].getCSV()")
except Exception as e:
    driver.implicitly_wait(100000)

driver.implicitly_wait(100000)

with open("gta5_steam_player_data.csv", "w") as f1:
    f1.write(player_result)

with open("gta5_twitch_viewers.csv", "w") as f2:
    f2.write(viewer_result)
