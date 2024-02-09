import scrapy, time
from ..items import AnimeScraperItem

class AniDBdetailSpider(scrapy.Spider):
    name = 'ADB_AnimeDetails'
    page = 0
    base_url = f"https://anidb.net/anime/?h=1&noalias=1&orderby.name=1.1&orderby.rating=0.2&page={page}&view=list"

    custom_settings = {
		'FEEDS': { 'data/ADB.csv': { 'format': 'csv',}}
		}

    def start_requests(self):
        # Starting URL for the first page of top anime results
        url = f"https://anidb.net/anime/?h=1&noalias=1&orderby.name=1.1&orderby.rating=0.2&page={self.page}&view=list"
        yield scrapy.Request(url=url, callback=self.parse)

        
    def parse(self, response):
        # Initialize the item
        output_json = {}


        # Extract anime page links from the current page
        
        anime_titles = response.css("#animelist .main a::text").getall()
        anime_types = response.css("td.type::text").getall()
        anime_episodes = response.css(".count.eps::text").getall()
        anime_ratings = response.css(".weighted::text").getall()
        anime_averages = response.css(".avg::text").getall()
        anime_reviews = response.css(".review::text").getall()
        anime_members = response.css(".members::text").getall()



        #''.join(s.split()) type ep



        # Iterate through anime links
        for i in range(30):

            output_json['title'] = anime_titles[i] 
            output_json['anime_types'] = ''.join(anime_types[i].split())
            output_json['anime_episodes'] = ''.join(anime_episodes[i].split())
            output_json['anime_ratings'] = ''.join(anime_ratings[i].split())
            output_json['anime_averages'] = ''.join(anime_averages[i].split())
            output_json['anime_reviews'] = ''.join(anime_reviews[i].split())
            output_json['anime_members'] = ''.join(anime_members[i].split())

            
            yield output_json

        
        if  self.page< 30:
            self.page+=1
            time.sleep(2)
            yield response.follow(f"https://anidb.net/anime/?h=1&noalias=1&orderby.name=1.1&orderby.rating=0.2&page={self.page}&view=list", callback=self.parse)








