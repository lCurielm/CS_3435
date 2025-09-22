import json
from typing import Dict
from scrapy.exceptions import DropItem


class ValidateAndWritePipeline:
    """Pipeline that validates items contain at least 10 non-empty attributes
    and writes them to a JSON lines file (recipes_valid.jl) in the project root.
    """

    def open_spider(self, spider):
        self.file = open('recipes_valid.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item: Dict, spider):
        # Count non-empty attributes
        non_empty = 0
        for k, v in item.items():
            if v is None:
                continue
            if isinstance(v, (list, tuple)) and len(v) == 0:
                continue
            if isinstance(v, str) and not v.strip():
                continue
            non_empty += 1

        if non_empty < 10:
            raise DropItem(f"Dropped item with only {non_empty} non-empty fields: {item.get('url')}")

        line = json.dumps(item, ensure_ascii=False)
        self.file.write(line + "\n")
        return item
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RealEstatePipeline:
    def process_item(self, item, spider):
        return item
