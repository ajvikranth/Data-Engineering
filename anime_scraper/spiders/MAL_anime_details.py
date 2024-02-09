import scrapy
import sqlite3,os
from scrapy.selector import Selector
import time

OUTPUT_FOLDER = os.path.join(os.getcwd(),'data')



class AnimeDetailSpider(scrapy.Spider):
    custom_settings = {
		'FEEDS': { 'data/MAL.json': { 'format': 'json',}}
		}


    name = 'MAL_AnimeDetail'
    id = 0

    # Constants and Configuration
    DB_FILE = "anime.db"
    TABLE_NAME = "MYANIMELIST_LINKS"



    def start_requests(self):
        # Connect to the database
        self.conn = sqlite3.connect(self.DB_FILE)
        self.cur = self.conn.cursor()

        # Fetch all rows from the MYANIMELIST_LINKS table
        self.cur.execute(f"SELECT * FROM {self.TABLE_NAME}")
        self.rows = self.cur.fetchall()
        self.rows_c = len(self.rows)

        # Build the URL for the first request
        url = self.rows[self.id][1]
        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        #get tabulated info as list of html snipets
        html_list = response.css(".leftside .spaceit_pad").getall()
        output_json = {}

        #extract data from each html snipet
        for html in html_list:
            element_list = Selector(text=html).css("::text").getall() 
            res =[]
            for element in element_list:
                clean_element = " ".join(element.split())
                clean_element =clean_element.replace(':','')
                clean_element =clean_element.replace(',','')
                if clean_element:
                    res.append(clean_element)
            if len(res)>2:
                output_json[res[0]]= res[1:]   
            else:
                output_json[res[0]]= res[1]

            try:
                output_json['Score'] =  float(output_json['Score'][0])
            except:
                pass 
            try:
                output_json['Ranked'] =  int(output_json['Ranked'][0][1:])
            except:
                pass 
            try:
                output_json['Popularity'] =  int(output_json['Popularity'][1:])
            except:
                pass 
            try:
                output_json['Members'] =  int(output_json['Members'])
            except:
                pass 
            try:
                output_json['Favorites'] =  int(output_json['Favorites'])
            except:
                pass 
            try:
                output_json['Episodes'] = int(output_json['Episodes'])
            except:
                pass   

            try:
                output_json["Genres"] = set(output_json["Genres"])
            except:
                pass
            
            try:
                output_json["Themes"] = set(output_json["Themes"])
            except:
                pass 

            try:
                output_json["Demographic"] = set(output_json["Demographic"])
            except:
                pass 
                
        output_json["url"] = self.rows[self.id][1]

        yield output_json

        time.sleep(1)

        self.id+=1
        
        # Check if there are more pages to scrape
        if  self.id < 5:#self.rows_c  : 
            next_page = self.rows[self.id][1]
            yield response.follow(next_page, callback=self.parse)
