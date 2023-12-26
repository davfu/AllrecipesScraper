import sqlite3
import json
import re

con = sqlite3.connect("recipes.db")

# create the SQL table
def create_table(connection: sqlite3.Connection):
    connection.execute(
        """
        CREATE TABLE recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            rating REAL,
            rev_count INTEGER,
            ingredients TEXT,
            num_ingredients INTEGER,
            cals INTEGER,
            protein INTEGER,
            carbs INTEGER,
            fat INTEGER,
            image_url TEXT,
            time INTEGER
        )
        """
    )

def parse_cook_time(cook_time_str):
    # extract numeric value from cook time
    match = re.match(r'PT(\d+)M', cook_time_str)
    if match:
        return int(match.group(1))
    return 0

def add_db_entry(connection: sqlite3.Connection, recipe):
    ingredients_str = ", ".join(recipe.ingredients)
    ingredients_len = len(recipe.ingredients)
    cook_time = parse_cook_time(recipe.time)

    connection.execute(
        """
        INSERT OR REPLACE INTO recipes (
            url, title, rating, rev_count, ingredients, num_ingredients, cals, protein, carbs, fat, image_url, time
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            recipe.url,
            recipe.title,
            recipe.rating,
            recipe.rev_count,
            ingredients_str,
            ingredients_len,
            recipe.nutrition.cals,
            recipe.nutrition.protein,
            recipe.nutrition.carbs,
            recipe.nutrition.fat,
            recipe.image.url,
            cook_time
        ),
    )

    connection.commit()