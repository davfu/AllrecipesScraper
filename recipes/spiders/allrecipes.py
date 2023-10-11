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
        # edit so that it finds the ones that has over 1000 reviews and a 4.5+ star rating
        # Check if the recipe list is not empty and if the first item is of type 'Recipe'
        if recipe and recipe[0].type and recipe[0].type[0] == 'Recipe':
            aggregate_rating = recipe[0].aggregate_rating

            # Check if aggregate_rating is not None and has the necessary attributes
            if aggregate_rating and aggregate_rating.rating_count and aggregate_rating.rating_value:
                rating_count = int(float(aggregate_rating.rating_count))
                rating_value = float(aggregate_rating.rating_value)

                if rating_count >= 1000 and rating_value >= 4.5:
                    headline = recipe[0].headline
                    print("headline: ", headline, " | rating: ", rating_value, " | count: ", rating_count)
        return
    
    #  run scrapy crawl allrecipes in terminal