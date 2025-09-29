from selenium import webdriver
import time
import requests
from protego import Protego
from dotenv import load_dotenv
import os

load_dotenv()

user_agent = os.getenv('USER_AGENT')
HEADERS = {'user-agent': user_agent}
url = ''
responce = requests.get(url + '/robots.txt', headers=HEADERS)
rp = Protego.parse(responce.text)
crawl_delay = rp.crawl_delay(user_agent) or 0

fetch_status = rp.can_fetch(url, user_agent=user_agent)

if fetch_status:

    driver = webdriver.Chrome(url)

    driver.get(url)

    time.sleep(10)

    driver.quit()