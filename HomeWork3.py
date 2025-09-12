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

# This function orchestrates the process:
# 1. Downloads robots.txt from the target URL.
# 2. Parses robots.txt to find sitemap URLs.
# 3. Extracts the sitemap_index.xml URL.
# 4. Downloads the sitemap index and gets the first sitemap URL.
# 5. Parses the first sitemap to get all <loc> URLs.
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


# This function parses the robots.txt content and extracts the sitemap_index.xml URL if present.
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


# This function downloads the robots.txt file from the specified URL and prints its contents.
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
    
    
# This function downloads the sitemap index XML from the given URL,
# parses it, and returns the first sitemap URL found.
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





# This function downloads a sitemap XML from the given URL,
# parses it, and returns a list of all <loc> tag elements found.
def parse_sitemap_locs(sitemap_url):
    """
    Downloads the sitemap at the given URL and returns a list of all <loc> URL strings found.
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
            loc = url_tag.find("loc")
            if loc:
                loc_tags.append(loc.text)
        print(f"Found {len(loc_tags)} <loc> URLs in the sitemap with parse_sitemap_locs.")
        return loc_tags
    except requests.RequestException as e:
        print(f"Error downloading or parsing sitemap: {e}")
        return []
    

def extract_recipe_data(page_url):
    """
    Downloads the page and extracts recipe information such as servings, prep time, cook time, ingredients, instructions, notes, and nutrition.
    Returns a dictionary with the extracted data.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        recipe = {}

        # Title (usually in <h1>)
        recipe['title'] = soup.find('h1').get_text(strip=True) if soup.find('h1') else None

        # Servings
        servings = soup.find(class_="wprm-recipe-servings")
        recipe['servings'] = servings.get_text(strip=True) if servings else None

        # Prep time
        prep_time = soup.find(class_="wprm-recipe-prep-time")
        recipe['prep_time'] = prep_time.get_text(strip=True) if prep_time else None

        # Cook time
        cook_time = soup.find(class_="wprm-recipe-cook-time")
        recipe['cook_time'] = cook_time.get_text(strip=True) if cook_time else None

        # Ingredients
        ingredients_list = []
        ingredients_ul = soup.find("ul", class_="wprm-recipe-ingredients")
        if ingredients_ul:
            for li in ingredients_ul.find_all("li"):
                ingredients_list.append(li.get_text(strip=True))
        recipe['ingredients'] = ingredients_list

        # Instructions
        instructions_list = []
        instructions_ul = soup.find("ul", class_="wprm-recipe-instructions")
        if instructions_ul:
            for li in instructions_ul.find_all("li"):
                instructions_list.append(li.get_text(strip=True))
        recipe['instructions'] = instructions_list

        # Notes
        notes_div = soup.find("div", class_="wprm-recipe-notes")
        notes = []
        if notes_div:
            for li in notes_div.find_all("li"):
                notes.append(li.get_text(strip=True))
            # If notes are not in <li>, get the text directly
            if not notes and notes_div.get_text(strip=True):
                notes.append(notes_div.get_text(strip=True))
        recipe['notes'] = notes

        # Nutrition
        nutrition_div = soup.find("div", class_="wprm-recipe-nutrition")
        recipe['nutrition'] = nutrition_div.get_text(strip=True) if nutrition_div else None

        return recipe
    except Exception as e:
        print(f"Error extracting recipe from {page_url}: {e}")
        return {}


def print_recipe(recipe):
    print("\n--- Recipe ---")
    print(f"Title: {recipe.get('title', 'N/A')}")
    print(f"Servings: {recipe.get('servings', 'N/A')}")
    print(f"Prep Time: {recipe.get('prep_time', 'N/A')}")
    print(f"Cook Time: {recipe.get('cook_time', 'N/A')}")
    print("\nIngredients:")
    for ingredient in recipe.get('ingredients', []):
        print(f"  - {ingredient}")
    print("\nInstructions:")
    for step in recipe.get('instructions', []):
        print(f"  - {step}")
    print("\nNotes:")
    for note in recipe.get('notes', []):
        print(f"  - {note}")
    print(f"\nNutrition: {recipe.get('nutrition', 'N/A')}")
    print("--- End Recipe ---\n")


if __name__ == "__main__":
    # Get the first sitemap URL from robots.txt
    sitemap_index_url = get_sitemap_url_from_robots(target_url="https://ohsnapmacros.com/robots.txt")
    if sitemap_index_url:
        # Get the first post sitemap URL from the sitemap index
        post_sitemap_url = download_sitemap_index(sitemap_index_url)
        if post_sitemap_url:
            # Get all <loc> URLs from the post sitemap
            loc_list = parse_sitemap_locs(post_sitemap_url)
            # Iterate over the first 5 URLs (change to 100 for full test)
            for url in loc_list[:5]:
                print(f"\nExtracting recipe from: {url}")
                recipe_data = extract_recipe_data(url)
                print_recipe(recipe_data)