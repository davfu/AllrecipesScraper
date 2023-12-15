import scrapy
import json
from recipes.types.allrecipes import recipe_from_dict
import re

# scrapes allrecipes.com
class AllrecipesSpider(scrapy.spiders.SitemapSpider):
    name = "allrecipes"
    # the sitemaps I want scrapy to go through, 
    # XML good for sharing data
    sitemap_urls = ["https://www.allrecipes.com/sitemap_1.xml",
                    "https://www.allrecipes.com/sitemap_2.xml",
                    "https://www.allrecipes.com/sitemap_3.xml",
                    "https://www.allrecipes.com/sitemap_4.xml"]

    def parse(self, response):
        # go through the page's ld+json
        script = response.css('script[type="application/ld+json"]::text').get()

        # skip the page if don't have that convention
        if script is None:
            return
        
        # load the current recipe for scraping
        recipe = recipe_from_dict(json.loads(script))
        recipe_type = recipe[0].type[0]  # Assuming it's the first item in the list

        # Check if the first item in the list is of type 'Recipe'
        # edit so that it finds the ones that has over 1000 reviews and a 4.5+ star rating
        # Check if the recipe list is not empty and if the first item is of type 'Recipe'
        if recipe and recipe_type and recipe[0].type[0] == 'Recipe':
            aggregate_rating = recipe[0].aggregate_rating

            # Check if aggregate_rating is not None and has the necessary attributes
            if aggregate_rating and aggregate_rating.rating_count and aggregate_rating.rating_value:
                rating_count = int(float(aggregate_rating.rating_count))
                rating_value = float(aggregate_rating.rating_value)
                ingredients = recipe[0].recipe_ingredient


                # Check if there are more than 500 reviews, at most 10 ingredients, and 4.5 star rating
                if rating_count >= 500 and rating_value >= 4.5 and len(ingredients) <= 10:
                    nutrition = recipe[0].nutrition
                    # use regular expression to find number in the string for nutrition
                    calories = re.search(r'\d+', nutrition.calories)
                    protein = re.search(r'\d+', nutrition.protein_content)
                    carbs = re.search(r'\d+', nutrition.carbohydrate_content)
                    fat = re.search(r'\d+', nutrition.fat_content)
                    # find the value for the rest
                    headline = recipe[0].headline
                    category = recipe[0].recipe_category
                    cuisine = recipe[0].recipe_cuisine
                    url = recipe[0].main_entity_of_page.id
                    # create yield to send it off to some entity, in this case a jsonlines file
                    yield {
                        "url": url,
                        "title": headline,
                        "rating": rating_value,
                        "rev_count": rating_count,
                        "category": category,                            
                        "cuisine": cuisine,
                        "ingredients": ingredients,
                        "nutrition": {
                            "cals": int(calories.group()),
                            "protein": int(protein.group()),
                            "carbs": int(carbs.group()),
                            "fat": int(fat.group())
                        }
                    }    
    #  run scrapy crawl allrecipes -o '/Users/davidfu/Desktop/AllrecipesScraper/filteringredients/recipes.jsonlines' in terminal