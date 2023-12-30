import jsonlines
import db as db
from recipes.types.output import recipe_from_dict

db.create_table(db.con)

with jsonlines.open("filtered.jsonlines", "r") as reader:
    for item in reader:
        recipe = recipe_from_dict(item)
        db.add_db_entry(db.con, recipe)
    print("Complete")