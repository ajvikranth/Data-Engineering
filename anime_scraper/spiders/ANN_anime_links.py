import scrapy
from ..items import AnimeScraperItem

class ProductLinkSpider(scrapy.Spider):
    name = 'ANN_AnimeLinks'

    base_url = "https://www.animenewsnetwork.com"

    custom_settings = {
        'ITEM_PIPELINES': {
            "anime_scraper.pipelines.ANN_AnimeLinkScraperPipeline": 400,
        }
    }

    def start_requests(self):
        # Starting URL for the first page of top anime results
        url = "https://www.animenewsnetwork.com/encyclopedia/ratings-anime.php?top50=best_bayesian&n=500"
        yield scrapy.Request(url=url, callback=self.parse)

        
    def parse(self, response):
        # Initialize the item
        item = AnimeScraperItem()

        # Extract anime page links from the current page
        
        anime_links = response.css(".t a::attr(href)").extract()


        # Iterate through anime links
        for product_link in anime_links:

            item["link"] = self.base_url + product_link

            yield item








