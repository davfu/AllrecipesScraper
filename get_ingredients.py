import jsonlines
from recipes.types.output import recipe_from_dict
from collections import Counter

def get_full_ingredients():
    with jsonlines.open("FINAL.jsonlines", "r") as recipes:
        word_counts = get_full_name_ingredients(recipes)
    return word_counts

def get_full_name_ingredients(recipes):
    full_name = Counter()

    for recipe in recipes:
        ingredients = recipe.get("ingredients", [])

        for ingredient in ingredients:
            if not len(ingredient) == 0: 
                cleaned = ingredient.strip()
                full_name.update({cleaned.lower(): 1})

    sorted_ingredients = [(ingredient, count) for ingredient, count in full_name.items() if count >= 8]
    sorted_ingredients = sorted(sorted_ingredients, key=lambda x: x[1], reverse=True)
    return sorted_ingredients