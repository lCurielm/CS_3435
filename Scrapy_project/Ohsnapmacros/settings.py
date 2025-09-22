"""Scrapy settings for the ohsnapmacros project.

This is the canonical lowercase package used by `scrapy.cfg`.
"""

BOT_NAME = 'ohsnapmacros'

# Where Scrapy will look for spiders
SPIDER_MODULES = ['ohsnapmacros.spiders']
NEWSPIDER_MODULE = 'ohsnapmacros.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'ohsnap-scraper-example (+https://ohsnapmacros.com)'

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Be polite to the server
DOWNLOAD_DELAY = 1.0
CONCURRENT_REQUESTS = 8

# Enable AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Pipelines: ensure pipeline module path matches package layout
ITEM_PIPELINES = {
    'ohsnapmacros.pipelines.ValidateAndWritePipeline': 300,
}

# Feed export encoding
FEED_EXPORT_ENCODING = 'utf-8'
