import scrapy
import json
from recipes.types.allrecipes import recipe_from_dict

class AllrecipesSpider(scrapy.spiders.SitemapSpider):
    name = "allrecipes"
    sitemap_urls = ["https://www.allrecipes.com/sitemap_1.xml"]

    def parse(self, response):
        # go through the page's ld+json
        script = response.css('script[type="application/ld+json"]::text').get()

        # skip the page if don't have that convention
        if script is None:
            return
        
        recipe = recipe_from_dict(json.loads(script))
        recipe_type = recipe[0].type[0]  # Assuming it's the first item in the list

         # Check if the first item in the list is of type 'Recipe'
        if recipe and recipe[0].type and recipe[0].type[0] == 'Recipe':
            # Access the headline and print it
            headline = recipe[0].headline
            print(headline)

        return