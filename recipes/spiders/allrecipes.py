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
                ingredients = recipe[0].recipe_ingredient


                # Check if there are more than 1000 reviews and 4.5 star rating
                if rating_count >= 250 and rating_value >= 4.5 and len(ingredients) <= 8:
                    nutrition = recipe[0].nutrition
                    calories = nutrition.calories
                    protein = nutrition.protein_content
                    carbs = nutrition.carbohydrate_content
                    fat = nutrition.fat_content
                    headline = recipe[0].headline
                    category = recipe[0].recipe_category
                    cuisine = recipe[0].recipe_cuisine
                    url = recipe[0].main_entity_of_page.id

                    yield {
                        "url": url,
                        "title": headline,
                        "rating": rating_value,
                        "rev_count": rating_count,
                        "category": category,                            
                        "cuisine": cuisine,
                        "ingredients": ingredients,
                        "nutrition": {
                            "cals": calories,
                            "protein": protein,
                            "carbs": carbs,
                            "fat": fat
                        }
                    }    
    #  run scrapy crawl allrecipes in terminal