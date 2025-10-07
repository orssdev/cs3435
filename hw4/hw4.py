from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests
from protego import Protego
import json
from dotenv import load_dotenv
import random
import os
import string

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
    height = analogy.split()[-2]
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

def neal_fun_trolly(driver):
    driver.get('https://neal.fun/absurd-trolley-problems/')
    for _ in range(28):
        time.sleep(5)
        level_info = driver.find_element(By.CSS_SELECTOR, 'div.level').text.split()
        level = int(level_info[1][:-1])
        level_name = ' '.join(level_info[2:])
        wavy_text_words = driver.find_elements(By.CSS_SELECTOR, 'div.wavy-text span.wavy-text-word')
        words = []
        for wavy_word in wavy_text_words[3:]:
            words.append(''.join([x.text for x in wavy_word.find_elements(By.CSS_SELECTOR, 'span.letter')]))
        dilemma = ' '.join(words).strip()
        button = driver.find_elements(By.CSS_SELECTOR, 'button.action')[0]
        button.click()
        time.sleep(5)
        votes_info_spans = driver.find_elements(By.CSS_SELECTOR, 'div.next-wrapper div.stat span.wavy-text-word')
        pulled_level = ''.join([x.text for x in votes_info_spans[0].find_elements(By.CSS_SELECTOR, 'span.letter')])
        not_pulled_level = ''.join([x.text for x in votes_info_spans[6].find_elements(By.CSS_SELECTOR, 'span.letter')])
        votes = int(''.join([x.text for x in votes_info_spans[8].find_elements(By.CSS_SELECTOR, 'span.letter') if x.text != '(' and x.text != ',']))
        data = {
            'url': 'https://neal.fun/absurd-trolley-problems/',
            'title': 'Absurd Trolley Problems',
            'level': level,
            'level name': level_name,
            'dilemma': dilemma,
            'pulled lever': pulled_level,
            'not pulled lever': not_pulled_level,
            'votes': votes
        }
        json_line = json.dumps(data)
        with open(json_lines_file, 'a') as fp:
            fp.write(json_line + '\n')
        next_button = driver.find_element(By.CSS_SELECTOR, 'button.action.action-next')
        next_button.click()

def monkey_type(driver):
        for _ in range(1):
            driver.get('https://monkeytype.com/')
            actions = ActionChains(driver)
            time.sleep(1)
            reject = driver.find_elements(By.CSS_SELECTOR, 'button.rejectAll')
            if reject:
                reject[0].click()
            words_container = driver.find_element(By.CSS_SELECTOR, 'div#words')
            words = words_container.find_elements(By.CSS_SELECTOR, 'div.word')
            letters = []
            for word in words:
                letters += [x.text for x in word.find_elements(By.CSS_SELECTOR, 'letter')]
                letters.append(' ')
            timeout = 30.0
            start = time.time()
            typing_speed = round(random.uniform(0.1, 2), 2)
            for c in letters:
                if time.time() - start >= timeout:
                    break
                ms = round(random.uniform(0.001, typing_speed), 3)
                time.sleep(ms)
                if random.randint(1,random.randint(10,20)) <= random.randint(10,20):
                    actions.send_keys(c)
                else:
                    error_c = random.choice(string.ascii_uppercase)
                    actions.send_keys(error_c)
                    ms = round(random.uniform(0.001, typing_speed), 2)
                    time.sleep(ms)
                    actions.perform()
                    actions.send_keys(Keys.BACKSPACE)
                    ms = round(random.uniform(0.001, typing_speed), 2)
                    time.sleep(ms)
                    actions.perform()
                    actions.send_keys(c)
                actions.perform()
            time.sleep(3)
            results = driver.find_element(By.CSS_SELECTOR, 'div#result')
            bottoms = results.find_elements(By.CSS_SELECTOR, 'div.bottom')
            wpm = bottoms[0].text
            acc = bottoms[1].text
            raw = results.find_element(By.CSS_SELECTOR, 'div.group.raw div.bottom').text
            consistency = results.find_element(By.CSS_SELECTOR, 'div.group.flat.consistency div.bottom').text
            correct = results.find_element(By.CSS_SELECTOR, 'div.group.key div.bottom').text.split('/')[0]
            data = {
                'url': 'https://monkeytype.com/',
                'wpm': wpm,
                'accuracy': acc,
                'raw': raw,
                'consistency': consistency,
                'correct': correct
            }
            json_line = json.dumps(data)
            with open(json_lines_file, 'a') as fp:
                fp.write(json_line + '\n')
        


user_agent = os.getenv('USER_AGENT')
HEADERS = {'user-agent': user_agent}
driver = webdriver.Chrome()

urls = [
    # ('https://neal.fun/', 'https://neal.fun/paper/', neal_fun_paper),
    # ('https://neal.fun/', 'https://neal.fun/absurd-trolley-problems/', neal_fun_trolly),
    ('https://monkeytype.com/', 'https://monkeytype.com/', monkey_type)
]

for url, index, fun in urls:
    responce = requests.get(url + '/robots.txt', headers=HEADERS)
    rp = Protego.parse(responce.text)
    crawl_delay = rp.crawl_delay(user_agent) or 0
    fetch_status = rp.can_fetch(index, user_agent=user_agent)

    if fetch_status:
        fun(driver)

driver.quit()