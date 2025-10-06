from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from protego import Protego
import json
from dotenv import load_dotenv
import os

load_dotenv()
json_lines_file = 'data.jsonl'


def neal_fun_paper_items(driver):
    title = driver.find_element(By.CSS_SELECTOR, 'div.title').text
    folds = int(driver.find_element(By.CSS_SELECTOR, 'div.fold-count').text.split()[0])
    imgs = driver.find_elements(By.XPATH, '//img')
    image = imgs[1].get_attribute('src')
    height = driver.find_element(By.CSS_SELECTOR, 'div.fold-tall span').text.split()[0]
    analogy = driver.find_element(By.CSS_SELECTOR, 'div.fold-analogy').text
    data = {
        'url': 'https://neal.fun/paper/',
        'title': title,
        'folds': folds,
        'image': image,
        'height': height,
        'analogy': analogy
    }
    json_line = json.dumps(data)
    with open(json_lines_file, 'a') as fp:
        fp.write(json_line + '\n')
    button = driver.find_element(By.CSS_SELECTOR, 'button.fold-controls-bttn.green')
    button.click()

def neal_fun_paper(driver):
    driver.get('https://neal.fun/paper/')
    time.sleep(2)
    folds = int(driver.find_element(By.CSS_SELECTOR, 'div.fold-count').text.split()[0])
    title = driver.find_element(By.CSS_SELECTOR, 'div.title').text
    imgs = driver.find_elements(By.XPATH, '//img')
    image = imgs[1].get_attribute('src')
    analogy = driver.find_element(By.CSS_SELECTOR, 'div.fold-analogy').text
    height = analogy.split()[- 2]
    data = {
        'url': 'https://neal.fun/paper/',
        'title': title,
        'folds': folds,
        'image': image,
        'height': height,
        'analogy': analogy
    }

    json_line = json.dumps(data)
    with open(json_lines_file, 'a') as fp:
        fp.write(json_line + '\n')
    
    button = driver.find_element(By.CSS_SELECTOR, 'button.fold-controls-bttn.green')
    button.click()
    for _ in range(42):
        time.sleep(1)
        neal_fun_paper_items(driver)


user_agent = os.getenv('USER_AGENT')
HEADERS = {'user-agent': user_agent}

urls = [
    ('https://neal.fun/', neal_fun_paper),
]

for url, fun in urls:
    responce = requests.get(url + '/robots.txt', headers=HEADERS)
    rp = Protego.parse(responce.text)
    crawl_delay = rp.crawl_delay(user_agent) or 0
    fetch_status = rp.can_fetch(url, user_agent=user_agent)

    if fetch_status:

        driver = webdriver.Chrome()
        try:
            fun(driver)
        except:
            print('Error happened')
        

    driver.quit()