import jsonlines
import db as db
import get_ingredients as ingredients
from recipes.types.output import recipe_from_dict

db.create_table(db.con)

with jsonlines.open("FINAL.jsonlines", "r") as reader:
    for item in reader:
        recipe = recipe_from_dict(item)
        db.add_db_entry(db.con, recipe)
    print("Completed recipes")