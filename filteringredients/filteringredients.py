import json
import re

# Define the list of words to delete
delete_list = ['cups', 'cup', 'teaspoons', 'teaspoon', 'tablespoons', 'tablespoon', 'ounces', 'ounce', 'grams', 'gram',
               'and', 'or', 'inch', 'inches', 'as', 'divded', 'peeled', 'melted', 'pounds', 'pound', 'into', 'chopped',
               'ground', 'to', 'taste', 'large', 'sliced', 'softened', 'shredded', 'cut', 'diced', 'beaten', 'grated',
               'for', 'medium', 'drained', 'thawed', 'crushed', 'finely', 'packages', 'halves', 'seasoned', 'fresh',
               'package', 'minced', 'pounded','dash','thickness','pinch','slices','cans','rinsed', 'slightly','can',
               'bits','more','cold','with','leaves','frozen','container','quarts','quart','mashed', 'jars']

# Open the original JSONLines file
file_path = '/Users/davidfu/Desktop/AllrecipesScraper/filteringredients/recipes.jsonlines'

# Create a new JSONLines file for the modified data
output_file_path = '/Users/davidfu/Desktop/AllrecipesScraper/filteringredients/recipes_modified.jsonlines'

with open(file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    for line in input_file:
        recipe = json.loads(line)

        # Process the list of ingredients for the current recipe
        ingredients = recipe.get('ingredients', [])
        new_ingredients = []

        for ingredient in ingredients:
            # Remove numbers, symbols, and unwanted words
            cleaned_ingredient = ' '.join([word for word in re.split(r'[\s/()]+', ingredient) if word.lower() not in delete_list and not word.replace('.', '', 1).isdigit()]).rstrip(',')
            new_ingredients.append(cleaned_ingredient)

        # Update the recipe's ingredients
        recipe['ingredients'] = new_ingredients

        # Write the modified recipe to the new JSONLines file
        output_file.write(json.dumps(recipe) + '\n')

print("Recipe modification complete. Modified data saved to 'recipes_modified.jsonlines'")
