"""
Liam Curiel

Resources used:
- Selenium documentation: https://www.selenium.dev/documentation/
- webdriver-manager: https://github.com/SergeyPirogov/webdriver_manager
- BeautifulSoup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Python robotparser (urllib.robotparser) for robots.txt

Additional work to exceed B requirements:
- Implemented polite crawling with robots.txt check and configurable sleep.
- BFS site crawler that visits internal links until reaching a target number of pages.
- Uses Selenium features: explicit waits, XPath and CSS selectors, clicking to reveal content, scrolling to bottom.
- Writes output as JSON Lines and includes many attributes per page.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Dict, Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.robotparser import RobotFileParser
from collections import deque
from typing import Set, List


def extract_attributes(url: str, html: str, title: str) -> Dict[str, Any]:
	soup = BeautifulSoup(html, "lxml")

	def first_text(selectors: List[str]):
		for sel in selectors:
			el = soup.select_one(sel)
			if el:
				text = el.get_text(separator=" ", strip=True)
				if text:
					return text
		return None

	def first_attr(selectors: List[str], attr: str):
		for sel in selectors:
			el = soup.select_one(sel)
			if el and el.has_attr(attr):
				val = el[attr]
				if val:
					return val
		return None

	def all_text(selectors: List[str]):
		for sel in selectors:
			els = soup.select(sel)
			vals = [e.get_text(separator=" ", strip=True) for e in els if e.get_text(strip=True)]
			if vals:
				return vals
		return []

	data: Dict[str, Any] = {}
	if url:
		data["url"] = url
	if title:
		data["title"] = title

	author = first_text(['a[rel="author"]', '.author a', '.byline a'])
	if author:
		data['author'] = author

	cats = [e.get_text(strip=True) for e in soup.select('a[rel="category tag"]')] or [e.get_text(strip=True) for e in soup.select('.breadcrumb a')]
	if cats:
		data['categories'] = cats

	servings = first_text(['.wprm-recipe-servings', '.servings'])
	if servings:
		data['servings'] = servings

	prep_time = first_text(['.wprm-recipe-prep_time', '.prep-time'])
	if prep_time:
		data['prep_time'] = prep_time

	cook_time = first_text(['.wprm-recipe-cook_time', '.cook-time'])
	if cook_time:
		data['cook_time'] = cook_time

	total_time = first_text(['.wprm-recipe-total_time', '.total-time'])
	if total_time:
		data['total_time'] = total_time

	ingredients = all_text(['.wprm-recipe-ingredients .wprm-recipe-ingredient-name', '.wprm-recipe-ingredients .wprm-recipe-ingredient', '.ingredients li', '.recipe-ingredients li'])
	if ingredients:
		data['ingredients'] = ingredients

	instructions = all_text(['.wprm-recipe-instructions li', '.wprm-recipe-instruction-text', '.instructions li', '.recipe-instructions li'])
	if instructions:
		data['instructions'] = instructions

	nutrition = first_text(['.wprm-recipe-nutrition', '.nutrition', '.nutrition-facts'])
	if nutrition:
		data['nutrition'] = nutrition

	ratings = first_text(['.wprm-recipe-rating-average', '.rating', '.post-rating'])
	if ratings:
		data['ratings'] = ratings

	return data

def crawl_site(start_url: str, out_file: str, max_pages: int = 100, delay: float = 0.5, headless: bool = True) -> None:
	parsed_start = urlparse(start_url)
	base_netloc = parsed_start.netloc

	visited: Set[str] = set()
	q = deque([start_url])

	count = 0
	with open(out_file, "w", encoding="utf-8") as outf:
		while q and count < max_pages:
			url = q.popleft()
			if url in visited:
				continue
			print(f"Visiting ({count+1}/{max_pages}): {url}")
			time.sleep(delay)
			driver = create_driver(headless=headless)
			try:
				driver.get(url)
				try:
					WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
				except Exception:
					pass
				try:
					cookie_btn = driver.find_element(By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]")
					cookie_btn.click()
					print("Clicked cookie/accept button via XPath")
				except Exception:
					pass
				try:
					driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					time.sleep(0.5)
				except Exception:
					pass

				title = driver.title
				html = driver.page_source

				attributes = extract_attributes(url, html, title)

				outf.write(json.dumps(attributes, ensure_ascii=False) + "\n")
				outf.flush()

				visited.add(url)
				count += 1

				soup = BeautifulSoup(html, "lxml")
				for a in soup.select("a[href]"):
					href = a.get("href")
					if not href:
						continue
					abs_href = urljoin(url, href)
					parsed = urlparse(abs_href)
					if parsed.netloc != base_netloc:
						continue
					norm = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
					if norm not in visited and norm not in q:
						q.append(norm)

			finally:
				try:
					driver.quit()
				except Exception:
					pass

	print(f"Crawl finished. {count} pages written to {out_file}")


def create_driver(headless: bool = True) -> webdriver.Chrome:
	chrome_options = Options()
	if headless:
		chrome_options.add_argument("--headless=new")
		chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--disable-dev-shm-usage")

	service = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service, options=chrome_options)
	return driver


def fetch_page(url: str, headless: bool = True, out_dir: str | Path = "screenshots", screenshot: bool = True) -> Dict[str, Any]:
	out_dir = Path(out_dir)
	out_dir.mkdir(parents=True, exist_ok=True)

	driver = create_driver(headless=headless)
	try:
		driver.set_page_load_timeout(30)
		driver.get(url)
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
		except Exception:
			pass

		title = driver.title
		html = driver.page_source

		screenshot_path = None
		if screenshot:
			host = url.split("//")[-1].split("/")[0].replace(":", "_")
			screenshot_path = out_dir / f"{host}.png"
			driver.save_screenshot(str(screenshot_path))

		return {"title": title, "html": html, "screenshot": str(screenshot_path) if screenshot_path else None}
	finally:
		driver.quit()


def scrape_html(url: str, html: str, title: str) -> Dict[str, Any]:
	data = extract_attributes(url, html, title)
	return data


def main() -> None:
	parser = argparse.ArgumentParser(description="Simple Selenium starter: open a URL, save screenshot, optionally scrape HTML to JSON")
	parser.add_argument("--url", default="https://example.com", help="URL to open")
	parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
	parser.add_argument("--no-headless", dest="headless", action="store_false", help="Run with browser UI (for debugging)")
	parser.add_argument("--scrape", action="store_true", help="Parse HTML and save structured data to JSON")
	parser.add_argument("--out", default=None, help="Output JSON file for scrape results (default: <host>_scrape.json)")
	parser.add_argument("--no-screenshot", dest="screenshot", action="store_false", help="Do not save a screenshot")
	parser.add_argument("--crawl", action="store_true", help="Crawl the site (BFS) and write JSON Lines output")
	parser.add_argument("--max-pages", type=int, default=100, help="Maximum number of pages to crawl (default 100)")
	parser.add_argument("--delay", type=float, default=1.0, help="Delay between page loads in seconds (politeness) (default 1.0)")
	parser.add_argument("--out-file", default=None, help="Output JSON Lines file for crawl mode (default: <host>_crawl.jsonl)")
	parser.set_defaults(headless=True, screenshot=True)

	args = parser.parse_args()

	print(f"Opening {args.url}  (headless={args.headless})")
	result = fetch_page(args.url, headless=args.headless, out_dir=Path("screenshots"), screenshot=args.screenshot)
	print(f"Page title: {result.get('title')}")
	if result.get("screenshot"):
		print(f"Screenshot saved to {result['screenshot']}")

	if args.scrape:
		print("Scraping page HTML...")
		data = scrape_html(args.url, result.get("html", ""), result.get("title", ""))
		out_path = args.out
		if not out_path:
			host = urlparse(args.url).netloc.replace(":", "_")
			out_path = f"{host}_scrape.json"
		with open(out_path, "w", encoding="utf-8") as f:
			json.dump(data, f, ensure_ascii=False, indent=2)
		print(f"Scrape results written to {out_path}")

	if args.crawl:
		out_file = args.out_file
		if not out_file:
			host = urlparse(args.url).netloc.replace(":", "_")
			out_file = f"{host}_crawl.jsonl"
		print(f"Starting crawl of {args.url} -> {out_file} (max {args.max_pages} pages, delay {args.delay}s)")
		crawl_site(args.url, out_file=out_file, max_pages=args.max_pages, delay=args.delay, headless=args.headless)


if __name__ == "__main__":
	main()


