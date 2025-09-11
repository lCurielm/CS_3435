
#I want to use requests to download the robots file from the website https://ohsnapmacros.com.
#once i get the robots file i want to print it to the console.
#after printing the robots file i want to use protego to parse the robots file and get the url of the sitemap_index.xml file.
#once i have all the url loc tag values from the site map, i need to use a separate function to go to each of those urls and from the content, create a dictionary of 
#the meta description, title, and h1 tag values.
#so far, this code gets the robots.txt file, extracts the sitemap_index.xml url, downloads the sitemap index, and prints the first sitemap url.
#i also have it able to parse the first sitemap to get all the <loc> urls and print the total number of <loc> urls found in the first site map.

import requests
from protego import Protego
from bs4 import BeautifulSoup
import urllib.robotparser

def get_sitemap_url_from_robots(target_url):
    robots_txt = download_robots_txt(target_url)
    if not robots_txt:
        print("Could not download robots.txt")
        return None
    robot_parser = Protego.parse(robots_txt)
    sitemaps = list(robot_parser.sitemaps)
    if sitemaps:
        var_sitemap_url = extract_sitemap_index_url(robots_txt)        
        print("Sitemap URL found:", var_sitemap_url)

        var_the_first_sitemap = download_sitemap_index(var_sitemap_url)
        print("First sitemap URL from sitemap index:", var_the_first_sitemap)    

        # Now parse the first sitemap to get all <loc> URLs  
        loc_list = parse_sitemap_locs(var_the_first_sitemap)
        print(f"Total <loc> URLs found: {len(loc_list)}")  

        return var_sitemap_url
    else:
        print("No sitemap URL found in robots.txt")
        return None

def extract_sitemap_index_url(robots_txt):
    """
    Extracts the sitemap_index.xml URL from the robots.txt content.
    Returns the URL as a string if found, otherwise None.
    """
    robot_parser = Protego.parse(robots_txt)
    sitemaps = list(robot_parser.sitemaps)
    for sitemap_url in sitemaps:
        if "sitemap_index.xml" in sitemap_url:
            print("sitemap_index.xml URL found:", sitemap_url)
            return sitemap_url
    print("No sitemap_index.xml URL found in robots.txt")
    return None

def download_robots_txt(url="https://ohsnapmacros.com/robots.txt"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(response.content.decode('utf-8'))
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading robots.txt: {e}")
        return None

def download_sitemap_index(sitemap_url):
    """
    Downloads the sitemap.xml (or sitemap index) from the given URL and returns a list of sitemap URLs.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(sitemap_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        sitemap_tags = soup.find_all("loc")
        sitemap_list = [tag.text for tag in sitemap_tags]
        print(f"Found {len(sitemap_list)} sitemap URLs in the download_sitemap_index.")
        return sitemap_list[0] if sitemap_list else None
    except requests.RequestException as e:
        print(f"Error downloading sitemap index: {e}")
        return []

def parse_sitemap_locs(sitemap_url):
    """
    Downloads the sitemap at the given URL and returns a list of all <loc> values found.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(sitemap_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")        

        loc_tags = []
        for url_tag in soup.find_all("url"):
            loc_tags.extend(url_tag.find_all("loc", recursive=False))


        print(f"Found {len(loc_tags)} <loc> URLs in the sitemap with parse_sitemap_locs.")
        return loc_tags
    except requests.RequestException as e:
        print(f"Error downloading or parsing sitemap: {e}")
        return []

if __name__ == "__main__":
    get_sitemap_url_from_robots(target_url="https://ohsnapmacros.com/robots.txt")