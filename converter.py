import jsonlines
import db
from recipes.types.output import recipe_from_dict

db.create_table(db.con)

with jsonlines.open("recipes2.jsonlines", "r") as reader:
    for item in reader:
        recipe = recipe_from_dict(item)
        db.add_db_entry(db.con, recipe)