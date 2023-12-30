import jsonlines
from recipes.types.output import recipe_from_dict
from collections import Counter
import re

def get_ingredients():
    with jsonlines.open("FINAL.jsonlines", "r") as recipes:
        word_counts = parse_ingredients(recipes)
    return word_counts

def parse_ingredients(recipes):
    ingredient_counter = Counter()

    for recipe in recipes: 
        ingredients = recipe.get("ingredients", [])

        for ingredient in ingredients:
            words = re.findall(r'\b[A-Za-z]+\b', ingredient) # remove numeric values
            words_lower = [word.lower() for word in words]
            ingredient_counter.update(words_lower)

    sorted_items = sorted(ingredient_counter.items(), key=lambda x: x[1], reverse=True)
    return sorted_items

print(get_ingredients())




