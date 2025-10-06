from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from protego import Protego
from dotenv import load_dotenv
import os

load_dotenv()

user_agent = os.getenv('USER_AGENT')
HEADERS = {'user-agent': user_agent}
url = 'https://neal.fun/' #Looking for a good website to sprape that had dynamic items to scrape for a challenge
responce = requests.get(url + '/robots.txt', headers=HEADERS)
rp = Protego.parse(responce.text)
crawl_delay = rp.crawl_delay(user_agent) or 0

fetch_status = rp.can_fetch(url, user_agent=user_agent)

if fetch_status:

    driver = webdriver.Chrome()

    driver.get('https://neal.fun/paper/')

    time.sleep(5)

    num_of_folds = driver.find_element(By.CSS_SELECTOR, 'div.fold-count')

    if num_of_folds:
        print(num_of_folds.text)

    imgs = driver.find_elements(By.XPATH, '//img')

    print(imgs[1].get_attribute('src'))

    height = driver.find_element(By.CSS_SELECTOR, 'div.fold-tall span')

    print(height.text)


    time.sleep(10)

    driver.quit()