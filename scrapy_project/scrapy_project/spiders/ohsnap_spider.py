"""
Spider: ohsnap
Author: Liam Curiel
Resources used:
- https://docs.scrapy.org/
- https://realpython.com/beautiful-soup-web-scraper-python/
- Site inspected: https://ohsnapmacros.com/
"""
from urllib.parse import urlparse
import scrapy


class OhsnapSpider(scrapy.Spider):
    name = 'ohsnap'
    allowed_domains = ['ohsnapmacros.com']
    start_urls = ['https://ohsnapmacros.com/all-recipes/']

    # Ethical defaults for the assignment; can be overridden on the CLI
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 1.0,
        'AUTOTHROTTLE_ENABLED': True,
        'CONCURRENT_REQUESTS': 8,
        'USER_AGENT': 'ohsnap-scraper-example (+https://ohsnapmacros.com)'
    }

    def parse(self, response):
        """Parse an index / listing page: enqueue recipe links and follow pagination.

        This improved version explicitly follows category and pagination/listing
        pages (so we can discover many recipe pages) while filtering out admin/product
        URLs.
        """
        raw_links = response.css('a::attr(href)').getall()
        seen = set()
        for href in raw_links:
            if not href:
                continue
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)

            parsed = urlparse(url)
            if not parsed.netloc.endswith('ohsnapmacros.com'):
                continue

            path = parsed.path or '/'
            # Skip administrative and utility pages, but allow category and pagination
            skip_tokens = ['/wp-admin', '/cdn-cgi/', '/cart', '/product', '/cookbook', '/privacy', '/terms']
            if any(tok in path for tok in skip_tokens):
                continue

            # If this link looks like a listing or pagination (category, page, all-recipes), follow with parse
            if any(tok in path for tok in ['/category/', '/page/', '/all-recipes', '/recipes', '/tag/']):
                yield response.follow(url, callback=self.parse)
                continue

            # Otherwise treat it as a candidate recipe page; parse_recipe will drop non-recipe pages
            yield scrapy.Request(url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        """Extract recipe data from a recipe page. Yields one dictionary per recipe."""
        def first_text(selectors):
            for sel in selectors:
                val = response.css(sel).get()
                if val and val.strip():
                    return val.strip()
            return None

        def all_text(selectors):
            for sel in selectors:
                vals = response.css(sel).getall()
                cleaned = [v.strip() for v in vals if v and v.strip()]
                if cleaned:
                    return cleaned
            return []

        title = first_text(['h1.entry-title::text', 'h1::text'])
        # If there's no title, this probably isn't a recipe page
        if not title:
            return

        item = {
            'url': response.url,
            'title': title,
            'author': first_text(['a[rel="author"]::text', '.author a::text', '.byline a::text']),
            'publish_date': first_text(['time.entry-date::attr(datetime)', 'time::attr(datetime)', 'meta[property="article:published_time"]::attr(content)']),
            'categories': response.css('a[rel="category tag"]::text').getall() or response.css('.breadcrumb a::text').getall(),
            'image': first_text(['meta[property="og:image"]::attr(content)', 'figure img::attr(src)', '.post-thumbnail img::attr(src)']),
            'servings': first_text(['.wprm-recipe-servings::text', '.servings::text']),
            'prep_time': first_text(['.wprm-recipe-prep_time::text', '.prep-time::text']),
            'cook_time': first_text(['.wprm-recipe-cook_time::text', '.cook-time::text']),
            'total_time': first_text(['.wprm-recipe-total_time::text', '.total-time::text']),
            'ingredients': all_text(['.wprm-recipe-ingredients .wprm-recipe-ingredient-name::text', '.wprm-recipe-ingredients .wprm-recipe-ingredient::text', '.ingredients li::text', '.recipe-ingredients li::text']),
            'instructions': all_text(['.wprm-recipe-instructions li::text', '.wprm-recipe-instruction-text::text', '.instructions li::text', '.recipe-instructions li::text']),
            'nutrition': first_text(['.wprm-recipe-nutrition::text', '.nutrition::text', '.nutrition-facts::text']),
            'ratings': first_text(['.wprm-recipe-rating-average::text', '.rating::text', '.post-rating::text']),
        }

        # Ensure we have at least 10 attributes (some may be empty strings) — add scraped timestamp
        item['scraped'] = response.headers.get('Date', b'').decode('utf-8') or None

        yield item
