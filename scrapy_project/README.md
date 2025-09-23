# OhSnap Macros Scrapy Project

This Scrapy project contains a spider that scrapes recipe pages from `ohsnapmacros.com`.

Run instructions (from project root where `scrapy.cfg` is located):

```powershell
.venv\Scripts\Activate.ps1
scrapy crawl ohsnap -o recipes.jl -s ROBOTSTXT_OBEY=1 -s DOWNLOAD_DELAY=1.0 -s AUTOTHROTTLE_ENABLED=1
```

The project will produce two output files if pipelines are used:

- `recipes.jl` (raw exported items from the spider when using `-o`)
- `recipes_valid.jl` (validated items written by the pipeline; only items with >=10 non-empty fields are kept)

Notes:

- The spider respects `robots.txt` by default and uses a download delay and AutoThrottle to be polite.
- If you need to adjust selectors, edit `scrapy_project/spiders/ohsnap_spider.py` and re-run the spider.
