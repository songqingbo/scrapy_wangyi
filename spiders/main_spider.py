# -*- coding:utf-8 -*-

from scrapy import Spider
from scrapy import Request
from scrapy import cmdline
from items import WangyiItem
import json


class MainSpider(Spider):
    name = 'main'

    def start_requests(self):
        fn = open('request_urls.txt', 'r')
        lines = fn.readlines()
        for line in lines:
            url = line.strip()
            yield Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        try:
            response_dict = json.loads(response.body)
            item = WangyiItem()
            tracks = response_dict['result']['tracks']
            collection_name = response_dict['result']['name']
            for track in tracks:
                collection_tags = ''

                for i, each in enumerate(response_dict['result']['tags']):
                    if i == 0:
                        collection_tags += each
                    elif i >= 1:
                        collection_tags += '|' + each
                category = response_dict['result']['tags'][0]
                song_name = track['name']
                song_id = track['id']
                artists = track['artists']
                artist_name = ''
                for i, artist in enumerate(artists):
                    if i == 0:
                        artist_name += artist['name']
                    else:
                        artist_name += '|' + artist['name']
                album_name = track['album']['name']
                album_id = track['album']['id']
                album_type = track['album']['type']
                item['collection_name'] = collection_name
                item['category'] = category
                item['song_name'] = song_name
                item['song_id'] = str(song_id)
                item['artists'] = artist_name
                item['album_name'] = album_name
                item['album_id'] = str(album_id)
                item['album_type'] = album_type
                item['collection_tags'] = collection_tags
                yield item
        except Exception, e:
            print e
            fn = open('failed_urls.txt', 'a')
            fn.write(response.url)
            fn.write('\n')
            fn.flush()
            fn.close()


if __name__ == '__main__':
    cmdline.execute('scrapy crawl main'.split())
