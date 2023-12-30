import json
import jsonlines
import re
from recipes.types.output import recipe_from_dict
from collections import Counter


def get_ingredients():
    with jsonlines.open("firstFilter.jsonlines", "r") as recipes:
        word_counts = parse_ingredients(recipes)
    return word_counts

def parse_ingredients(recipes):
    ingredient_counter = Counter()

    for recipe in recipes: 
        ingredients = recipe.get("ingredients", [])

        for ingredient in ingredients:
            words = re.findall(r'\b[A-Za-z]+\b', ingredient)
            words_lower = [word.lower() for word in words]
            ingredient_counter.update(words_lower)
    
    sorted_items = sorted(ingredient_counter.items(), key=lambda x: x[1], reverse=True)
    return sorted_items

words = get_ingredients()

# # Define the list of words to delete
delete_list = ['cup', 'teaspoon', 'cups','ounce','tablespoons','chopped','ground','tablespoon','and','to','teaspoons','taste','fresh','can','powder','all','purpose','package','pound','sliced','minced','or','large','shredded','diced','into','cloves','cut','vegetable','peeled',
               'inch','pounds','drained','softened','boneless','ounces','divided','mix','melted','pinch','as','crushed','skinless','slices','beaten','medium','frozen','halves','cans','sour','pieces','small','finely','packed','of','cubed','cooked','italian','for','needed',
               'thinly','heavy','freshly','cooking','more','thawed','packages','leaves','half','seeded','with','style','rinsed','unsalted','semisweet','such','prepared','uncooked','halved','unsweetened','cubes','in','container','spray','light','seasoned','jar','lean','cored','crumbled','instant',
               'fluid','warm','cold','stalks','active','paste','thick','trimmed','juiced','quartered','pitted','virgin','mashed','frying','mashed','roast','fat','kosher','sweetened','wheat','flavored','topping','rolled','lightly','whipping','whipped','flaked', 'rinsed'
               'deveined','quart','removed','bottle','thin','room','temperature','coarsely','french','bite','low','toasted','f','ripe','swiss','root','dash','sea','refrigerated','c','wedges','food','taco','size','liquid','seed','sifted','quick','baby','kernel','round','weed','lengthwise','puree',
               'sodium','distrilled','pint','dark','quarts','split','florets','stalk','torn','sharp','kidney','smoked','long','dough','grain','plain','rolls','free','cube','squares','chilled','unbaked','creamy','boiling','rings','sprigs','skin','miniature','a','old','undrained','reduced','stewed',
               'processed','separated','loaf','mixed','blend','elbow','at','packet','baked','granules','reserved','filling','roasted','dusting','coloring','double','slivered','drops','mexican','hash','crescent','flat','stems','self','rising','envelope','deep','poultry','american','recipe','bag',
               'pounded','very','buttery','vegetables','broken','semi','stew','smoke','squeezed','shell','mild','stuffing','if','flavoring','cooled','shells','golden','plus','unpeeled','hard','g','seedless','sized','o''zested','on','decoration','links','coards','e','bulk','julienned','english',
               'jell','slice','pressed','preserves','jars','fried','cracked','from','spicy','rounds','powdered','blanched','mini','fine','soaked','chunky','peel','roughly','bits','new','cleaned','hulled','mandarin','brewed','granulated','unbleached','pure','firm','ears','washed','flavor','dish',
               'wrappers','tails','top','chinese','regular','top','slightly','any','real','firmly','wide','thickness','soft','piece','soft','asian','desired','dashses','nonstick','tops','fully','sticks','single','scrubbed','single','coating','eagle','brand','part','discarded','strong','sprig',
               'dinner','salted','bunches','devil','short','shelled','crunchy','color','cover','creamed','japanese','other','diagonally','colored','only','warmed','lukewarm','box','kraft','day','northern','country','irish','machine','rubbed','no','tm','covered','patted','thai','crosswise','serving',
               'meal','mccormick','husks','wild','philadelphia','containers','not','individually','based','up','pre','solid','non','aluminum','natural','pack','old','fashioned','miracle','paper','thing','well','eg','each','drop','de','overnight','liter','about','optional','minutes','choice','per',
               'eighths','liters','filled','unflavored','see','hillshire','farm','pot','ready','some','less','cook','serve','then','t','quality','milliliter','heinz','but','high','use','off','kitchen','grind','out','low-sodium','all-purpose','deveined', 'butterflied','grands', 'velveeta', 'jif', 
               'noodle', 'lawry', 'smucker', 'knorr', 'kraft', 'reynolds', 'guinness', 'splenda', 'craisins', 'chachere', 'pam', 'kellogg', 'krispies', 'marnier', 'pace', 'cola', 'goya', 'mrsdash', 'egguinness', 'jiffy', 'dew', 'gluten', 'nutella', 'use', 'libby', 'hellmann', 'crocker', 'own', 
               'style', 'oreo', 'request', 'coke', 'baker', 'karo', 'spray', 'paso', 'gulden', 'sargento', 'o', 'lettucedried', 'ray', 'crispix', 'swerve', 'hines', 'tri', 'breakstone', 'heinz', 'johnsonville', 'lean', 'dole', 'farms', 'm', 'bacardi', 'light', 'mazola', 'hunt', 'pure', 'doritos', 
               'pet', 'foods', 'rao', 'lars', 'ragu', 'mccain', 'cholula', 'quaker', 'tapatio', 'sides', 'petes', 'creations', 'egrice', 'hurst', 'coating', 'mix', 'stuffed', 'progresso', 'cattlemen', 'daniel', 'dean', 'mrs', 'mates', 'lay', 'lakes', 'melt', 'arthur', 'serve', 'rolo', 
               'shiner', 'joy', 'brewer', 'fiesta', 'top', 'ievelveeta', 'argo', 'kingsford', 'ortega', 'master', 'resistant', 'bouquet', 'emeril', 'essence', 'nestle', 'carnation', 'minute', 'fritos', 'spam', 'classico', 'zatarain', 'blend', 'whiz', 'calves', 'clamato', 'valentina', 'swan',
               'vegetable', 'prego', 'king', 'maldon', 'swanson', 'life', 'reese', 'crock', 'eat', 'lit', 'l', 'smokies', 'bush', 'seasons', 'bragg', 'balance', 'ac', 'cent', 'pato', 'brickle', 'newman', 'long', 'kikkoman', 'delight', 'can', 't', 'it', 'conecuh', 'frontera', 'nilla', 'tyson', 'ready', 'basics']

for item in words:
    if item[1] <= 5:
        delete_list.append(item[0])

# Open the original JSONLines file
file_path = '/Users/davidfu/Desktop/Projects/AllrecipesScraper/firstFilter.jsonlines'

# Create a new JSONLines file for the modified data
output_file_path = '/Users/davidfu/Desktop/Projects/AllrecipesScraper/FINAL.jsonlines'

with open(file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    for line in input_file:
        recipe = json.loads(line)

        # Process the list of ingredients for the current recipe
        ingredients = recipe.get('ingredients', [])
        new_ingredients = []

        for ingredient in ingredients:
            # Ensure a space after comma in cases like "2 green onions,chopped"
            ingredient = re.sub(r'(\d+)\s*,\s*(\w+)', r'\1 \2', ingredient)

            # Handle commas in multi-word ingredients like "green onions, sliced, white parts " 
            ingredient = re.sub(r',\s*', ' ', ingredient)

            # Remove numbers, symbols, and unwanted words
            cleaned_ingredient = ' '.join([word for word in re.split(r'[\s/()]+', ingredient) if word.lower() not in delete_list and not word.replace('.', '', 1).isdigit()])

            # Remove words with dashes
            cleaned_ingredient = re.sub(r'\b[A-Za-z]+-[A-Za-z]+\b', '', cleaned_ingredient)

            # Remove unwanted characters (comma, dash, period, parentheses) and space after them
            cleaned_ingredient = re.sub(r'(,|\-|\.|\()\s*', '', cleaned_ingredient)

            new_ingredients.append(cleaned_ingredient)

        # Update the recipe's ingredients
        recipe['ingredients'] = new_ingredients

        # Write the modified recipe to the new JSONLines file
        output_file.write(json.dumps(recipe) + '\n')

print("Recipe modification complete. Modified data saved to 'FINAL.jsonlines'")
