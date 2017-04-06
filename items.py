# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field


class WangyiItem(Item):
    collection_name = Field()
    category = Field()
    song_name = Field()
    song_id = Field()
    artists = Field()
    album_name = Field()
    album_id = Field()
    album_type = Field()
    collection_tags = Field()
