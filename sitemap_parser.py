from sys import argv
import time
import requests
from urllib.parse import urlparse
from protego import Protego
from bs4 import BeautifulSoup

HEADERS = {}
def get_robot_parser(base_url:str)-> Protego:
    global HEADERS
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
    HEADERS = {'User-Agent': user_agent}
    response = requests.get(base_url + "/robots.txt", headers=HEADERS)
    robot_parser = Protego.parse(response.text)
    return robot_parser

def parse_sitemaps(sitemaps, crawl_delay):
    url_list = []
    for sitemap in sitemaps:
        print(f"Waiting for {crawl_delay} seconds")
        print(sitemap)
        time.sleep(crawl_delay)
        response = requests.get(sitemap, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'xml')

        if soup.find('sitemapindex'):
            nested_sitemaps = [tag.text for tag in soup.find_all('loc')]
            url_list += parse_sitemaps(nested_sitemaps, crawl_delay)
        elif soup.find('urlset'):
            urls = [tag.text for tag in soup.find_all('loc')]
            for item in urls:
                parsed = urlparse(item)
                if parsed.netloc.endswith("holtonmountainrentals.com"):
                    url_list.append(item)
    return url_list


def main(domain_name):
    robot_parser = get_robot_parser(domain_name)
    crawl_delay = robot_parser.crawl_delay('*') or 0
    urls = parse_sitemaps(robot_parser.sitemaps, crawl_delay)
    print(urls)
    print(len(urls), 'urls')

if __name__ == '__main__':
    main(argv[1])
