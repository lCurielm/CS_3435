You will use protego, requests, and Beautiful Soup to scrape item pages from your "semester project website." Make sure that the site you choose doesn't have coding examples for it by Googling: "Python scrape <your_domain_name>" (without the quotes), that it allows scraping (using protego and robots.txt), and the data is visible in the raw HTML (Ctrl-U in the browser).
 
 
On your site, find an "index" page that has links to a lot of "item" pages.
 
Use requests to download the robots file. Make sure the downloaded text matches what you see in your browser. Ask your Protego robot parser if your item page can be fetched. (Yes or No?) IF Yes, use requests to download the page. You may need to set the user-agent in the header to your real user-agent. Try http://whatsmyuseragent.org/
 
 
Use Beautiful Soup to parse the downloaded "index" page and print every link for another item.
 
Download and parse every item page and collect at least 10 attributes from each page. One attribute should be the URL of the item page. Construct a dictionary with at least 10 key/value pairs containing the attributes and their values:
data = {"url": url, "title": title, etc...}
Convert your attribute dictionary to a string using "json.dumps" and append it to your JSON lines file:
json_line = json.dumps(data)
with open(json_lines_file, 'a') as fp:
    fp.write(json_line + '\n')
 
The file should contain a different dictionary on each line.
 
