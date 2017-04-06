# -*- coding: utf-8 -*-
import MySQLdb
import time


class WangyiPipeline(object):
    def __init__(self):
        print 'init'
        self.host = '101.200.159.42'
        self.user = 'java'
        self.pw = 'inspero'
        self.database = 'musicnew'

    def open_spider(self, spider):
        self.database = MySQLdb.connect(self.host, self.user, self.pw, self.database, charset='utf8')
        self.cursor = self.database.cursor()
        self.cursor.execute('select version()')
        data = self.cursor.fetchone()
        print int(time.time()), 'Database version : %s' % data
        del data

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        try:
            insert_timestamp = str(int(time.time()))
            for key in item.keys():
                if item[key] == None:
                    item[key] = ''
            sql = 'INSERT INTO wangyi_music(insert_timestamp,collection_name,category,song_name,song_id,artists,album_name,album_id,album_type,collection_tags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            temp_tuple = (
                insert_timestamp, item['collection_name'], item['category'], item['song_name'], item['song_id'],
                item['artists'], item['album_name'], item['album_id'], item['album_type'], item['collection_tags'])
            inserted_list = [temp_tuple]
            self.cursor.executemany(sql, inserted_list)
            self.database.commit()
        except Exception, e:
            self.database.rollback()
            print e
        return item
