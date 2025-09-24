import requests
from protego import Protego
import time
from bs4 import BeautifulSoup
import json

try:
     scraped_episodes = []
     with open('data.jl', 'r') as lines:
          for line in lines:
               data = json.loads(line)
               scraped_episodes.append(data['url'])
except:
     scraped_episodes = []
     

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15'
HEADERS = {'user-agent': user_agent}
url = 'https://www.thenosleeppodcast.com'
responce = requests.get(url + '/robots.txt', headers=HEADERS)
rp = Protego.parse(responce.text)
crawl_delay = rp.crawl_delay(user_agent) or 0


def get_responce(inpURL):
        responce = requests.get(inpURL, headers=HEADERS)
        time.sleep(crawl_delay)
        return responce


def collect_data(inpURL):
    data = {'url': inpURL}
    responce = get_responce(inpURL)
    soup = BeautifulSoup(responce.text, 'html.parser')
    h2 = soup.find('h2')
    h2 = h2.text.split()
    date = ' '.join(h2[:2])
    title = ' '.join(h2[2:])
    desc = soup.find('p').text
    ps = soup.find_all('p')
    imgs = [p.find('img')['src'] for p in ps if p.find('img') is not None]
    img = 'No Art Cover'
    if len(imgs) != 0 and 'http://i.' not in imgs[0] and 'Banner' not in imgs[0]:
        img = imgs[0]
    num_of_comments = int(soup.find('a', {'class', 'post_comments'}).text.split()[0])
    post_author = soup.find('a', {'class', 'post_author_link'}).text
    stories = [p.text for p in ps if 'written by' in p.text]
    i = 0
    while i < len(ps) and 'sponsored' not in ps[i].text:
        i += 1          
    sponsors = []
    if i != len(ps):
        i += 1
        while i < len(ps) and 'Click here to learn more about The NoSleep Podcast team' not in ps[i].text:
            sponsors.append(ps[i].text)
            i += 1
    span = soup.find('span', {'class': 'time'})
    time_posted = span.text
    data['title'] = title
    data['date'] = date
    data['time_posted'] = time_posted
    data['description'] = desc
    data['art_cover'] = img
    data['number_of_comments'] = num_of_comments
    data['post_author'] = post_author
    data['stories'] = stories
    data['sponsors'] = sponsors

    json_line = json.dumps(data)
    json_lines_file = 'data.jl'
    with open(json_lines_file, 'a') as fp:
        fp.write(json_line + '\n')

all_episodes = []

for i in range(1, 23):
    index_site = f'https://www.thenosleeppodcast.com/s{i}'
    fetch_status = rp.can_fetch(index_site, user_agent)

    if fetch_status:
        start_time = time.time()
        responce = get_responce(index_site)
        soup = BeautifulSoup(responce.text, 'html.parser')
        anchors = [a['href'] for a in soup.find_all('a')]
        episodes = list(set(filter(lambda l: f'episodes/s{i}' in l, anchors)))
        episodes.sort()
        for e in episodes:
             if e not in scraped_episodes:
                 all_episodes.append(e)
    else:
        print(f'Could Not Scrape {index_site}')

for e in all_episodes:
    collect_data(e)
