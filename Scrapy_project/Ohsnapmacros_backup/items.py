from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class RecipeItem:
    url: str
    title: str
    author: Optional[str] = None
    publish_date: Optional[str] = None
    categories: List[str] = field(default_factory=list)
    image: Optional[str] = None
    servings: Optional[str] = None
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    total_time: Optional[str] = None
    ingredients: List[str] = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)
    nutrition: Optional[str] = None
    ratings: Optional[str] = None
    scraped: Optional[str] = None


def as_dict(item: 'RecipeItem') -> Dict:
    return {k: v for k, v in item.__dict__.items()}
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
