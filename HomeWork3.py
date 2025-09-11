import requests
from bs4 import BeautifulSoup
from protego import Protego
from urllib.parse import urlparse, urljoin
import sys
import json
import os

HEADERS = {}

def get_robot_parser(base_url: str) -> Protego:
    global HEADERS
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
    HEADERS = {'User-Agent': user_agent}
    response = requests.get(base_url + "/robots.txt", headers=HEADERS)
    assert response.text.strip() != "", "robots.txt is empty!"
    robot_parser = Protego.parse(response.text)
    return robot_parser

def can_fetch_url(robot_parser, url):
    return robot_parser.can_fetch(url, HEADERS['User-Agent'])

def get_index_links(index_url):
    response = requests.get(index_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'xml')
    links = []
    for loc in soup.find_all('loc'):
        href = loc.text.strip()
        # Filter for recipe pages (adjust if needed)
        if '/recipes/' in href or '/recipe/' in href:
            links.append(href)
    return links

def load_scraped_urls(json_lines_file):
    scraped = set()
    if os.path.exists(json_lines_file):
        with open(json_lines_file, 'r') as fp:
            for line in fp:
                try:
                    data = json.loads(line)
                    scraped.add(data['url'])
                except Exception:
                    continue
    return scraped

def scrape_item_page(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract attributes
    title = soup.title.string if soup.title else ""
    entry_title = soup.find(class_='entry-title')
    entry_title = entry_title.get_text(strip=True) if entry_title else ""
    # Ingredients (may be in a list or div, adjust selector as needed)
    ingredients = []
    ing_section = soup.find(class_='wprm-recipe-ingredients-container')
    if ing_section:
        for ing in ing_section.find_all(class_='wprm-recipe-ingredient'):
            ingredients.append(ing.get_text(strip=True))
    # Instructions
    instructions = []
    inst_section = soup.find(class_='wprm-recipe-instructions-container')
    if inst_section:
        for step in inst_section.find_all(class_='wprm-recipe-instruction-text'):
            instructions.append(step.get_text(strip=True))
    # Servings
    servings = ""
    servings_tag = soup.find(class_='wprm-recipe-servings')
    if servings_tag:
        servings = servings_tag.get_text(strip=True)
    # Cook time
    cook_time = ""
    cook_time_tag = soup.find(class_='wprm-recipe-time')
    if cook_time_tag:
        cook_time = cook_time_tag.get_text(strip=True)
    # Macros (may be in a table or div, adjust selector as needed)
    macros = {}
    macro_section = soup.find(class_='wprm-nutrition-label-container')
    if macro_section:
        for row in macro_section.find_all('span', class_='wprm-nutrition-label-text'):
            label = row.get_text(strip=True)
            value = row.find_next_sibling('span')
            if value:
                macros[label] = value.get_text(strip=True)
    data = {
        "url": url,
        "title": title,
        "entry_title": entry_title,
        "ingredients": ingredients,
        "instructions": instructions,
        "servings": servings,
        "cook_time": cook_time,
        "macros": macros
    }
    return data

def main(base_url, index_url, json_lines_file):
    robot_parser = get_robot_parser(base_url)
    scraped_urls = load_scraped_urls(json_lines_file)
    item_links = get_index_links(index_url)
    for url in item_links:
        if url in scraped_urls:
            print(f"Already scraped: {url}")
            continue
        if not can_fetch_url(robot_parser, url):
            print(f"Cannot fetch (robots.txt): {url}")
            continue
        print(f"Scraping: {url}")
        data = scrape_item_page(url)
        # Only save if at least 7 attributes are present (adjust as needed)
        if len(data) >= 7:
            with open(json_lines_file, 'a', encoding='utf-8') as fp:
                fp.write(json.dumps(data, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python HomeWork3.py <base_url> <index_url> <json_lines_file>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])



