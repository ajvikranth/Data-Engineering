import scrapy
from ..items import AnimeScraperItem

class ProductLinkSpider(scrapy.Spider):
    name = 'MAL_AnimeLinks'
    page_count = 50

    custom_settings = {
        'ITEM_PIPELINES': {
            "anime_scraper.pipelines.AnimeLinkScraperPipeline": 300,
        }
    }

    def start_requests(self):
        # Starting URL for the first page of top anime results
        url = 'https://myanimelist.net/topanime.php?limit=0'
        yield scrapy.Request(url=url, callback=self.parse)

        
    def parse(self, response):
        # Initialize the item
        item = AnimeScraperItem()

        # Extract anime page links from the current page
        
        anime_links = set(response.css(".hoverinfo_trigger::attr(href)").extract())


        # Iterate through anime links
        for product_link in anime_links:

            item["link"] = product_link

            yield item

        # Prepare URL for the next page
        next_page = 'https://myanimelist.net/topanime.php?limit='+ str(self.page_count)

        # set limit
        if  self.page_count<1000: 
            self.page_count+=50
            yield response.follow(next_page, callback=self.parse)






