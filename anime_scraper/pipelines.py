# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AnimeScraperPipeline:
    def process_item(self, item, spider):
        return item

import sqlite3


class AnimeLinkScraperPipeline:

    def __init__(self) :
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("anime.db")
        self.corr = self.conn.cursor()

    def create_table(self):
        self.corr.execute('''DROP TABLE IF EXISTS MYANIMELIST_LINKS''')
        self.corr.execute('''CREATE TABLE MYANIMELIST_LINKS (id integer primary key, 
                                          link text) ''')


    def process_item(self, item, spider):
        self.store_item(item)
        return item
    
    def store_item(self,item):
        self.corr.execute('''INSERT INTO MYANIMELIST_LINKS(link) VALUES (?)''',(item["link"],))
        self.conn.commit()


class ANN_AnimeLinkScraperPipeline:

    def __init__(self) :
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("anime.db")
        self.corr = self.conn.cursor()

    def create_table(self):
        self.corr.execute('''DROP TABLE IF EXISTS ANN_LINKS''')
        self.corr.execute('''CREATE TABLE ANN_LINKS (id integer primary key, 
                                          link text) ''')


    def process_item(self, item, spider):
        self.store_item(item)
        return item
    
    def store_item(self,item):
        self.corr.execute('''INSERT INTO ANN_LINKS(link) VALUES (?)''',(item["link"],))
        self.conn.commit()
