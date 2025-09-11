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
    response = requests.get(base_url, headers=HEADERS)
    robot_parser = Protego.parse(response.text)
    #print(response.text)
    return robot_parser

def parse_sitemaps(sitemaps, crawl_delay):
    url_list = []
    sitemap = list(sitemaps)[0]
    response = requests.get(sitemap, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'xml')
    url_list += [tag.text for tag in soup.find_all('loc')]
    for url in url_list:
        #print(url)
        response = requests.get(url, headers=HEADERS)
        robot_parser = Protego.parse(response.text)
        soup = BeautifulSoup(response.text, 'xml')
        url_list += [tag.text for tag in soup.find_all('loc')]
        #print(response.text)
        #robot_parser = get_robot_parser(url)
        new_url_list = parse_sitemaps(robot_parser.sitemaps, crawl_delay)
    return url_list


    #print(url_list)
    return url_list

def main(domain_name):
    robot_parser = get_robot_parser(domain_name)
    crawl_delay = robot_parser.crawl_delay('*') or 0
    urls = parse_sitemaps(robot_parser.sitemaps, crawl_delay)
    print(urls)
    print(len(urls), 'urls')

if __name__ == '__main__':
    main(argv[1])
