from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# Build settings programmatically to avoid importing the project's settings module
settings = Settings()
settings.set('CLOSESPIDER_ITEMCOUNT', 3)
settings.set('ITEM_PIPELINES', {})
settings.set('LOG_LEVEL', 'INFO')
# Point SPIDER_MODULES to the importable package (the existing capitalized one is importable)
settings.set('SPIDER_MODULES', ['Ohsnapmacros.spiders'])
settings.set('NEWSPIDER_MODULE', 'Ohsnapmacros.spiders')
settings.set('FEEDS', {'out.jl': {'format': 'jl', 'encoding': 'utf-8'}})

process = CrawlerProcess(settings)
process.crawl('ohsnap')
process.start()
