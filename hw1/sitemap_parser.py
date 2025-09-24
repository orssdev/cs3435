from sys import argv
import time
import requests
from protego import Protego
from bs4 import BeautifulSoup

# one line for constant global headers (fix its value)
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15'}


def get_robot_parser(base_url):
    response = requests.get(base_url + '/robots.txt', headers=HEADERS)
    return Protego.parse(response.text)


def parse_sitemaps(sitemaps, crawl_delay):
    URLs = []
    maps = list(sitemaps)
    for site in maps:
        print(site)
        start_time = time.time()
        time.sleep(crawl_delay)
        response = requests.get(site, headers=HEADERS)
        duration = time.time() - start_time
        print(f'Waiting for {int(duration)} seconds')
        soup = BeautifulSoup(response.text, 'xml')
        if soup.sitemapindex is not None:
            URLs += parse_sitemaps([tag.find('loc').text for tag in soup.find_all('sitemap')], crawl_delay)
        else:
            URLs += [tag.text for tag in soup.find_all('loc')]
    return URLs


def main(domain_name):
    # Do not edit this function.
    robot_parser = get_robot_parser(domain_name)
    crawl_delay = robot_parser.crawl_delay('*') or 0
    urls = parse_sitemaps(robot_parser.sitemaps, crawl_delay)
    print(urls)
    print(len(urls), 'urls')


if __name__ == '__main__':
    main(argv[1])

# There should not be any other code left aligned to the margin.
