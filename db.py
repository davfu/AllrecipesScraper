import sqlite3
import json
import re

con = sqlite3.connect("recipes.db")

# create the SQL table
def create_table(connection: sqlite3.Connection):
    # recipes table 
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
    # ingredients table
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            count INTEGER
        )
        """
    )
    # junction table
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            recipe_id INTEGER,
            ingredient_id INTEGER,
            PRIMARY KEY (recipe_id, ingredient_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
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

    cursor = connection.cursor()

    cursor.execute(
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

    recipe_id = cursor.lastrowid
    fill_ingredients(connection, recipe.ingredients)
    fill_junction(connection, recipe_id, recipe.ingredients)

    connection.commit()

def add_ingredients(connection: sqlite3.Connection, item):
    ingredient, count = item[0], item[1]
    connection.execute(
        """
        INSERT OR REPLACE INTO ingredients (
            name, count
        ) VALUES (?,?)
        """,
        (
            ingredient,
            count
        ),
    )

    connection.commit()

# insert the ingredients into table while interating through recipes
def fill_ingredients(connection, ingredients):
    for ingredient in ingredients:
        if not len(ingredient) == 0:
            ingredient_id = connection.execute(
                """
                SELECT id FROM ingredients WHERE name = ?
                """,
                (ingredient,)
            ).fetchone()
        
            if ingredient_id is None:
                connection.execute(
                    """
                    INSERT INTO ingredients (name, count) VALUES (?, 1)
                    """,
                    (ingredient,)
                )
            else:
                connection.execute(
                    """
                    UPDATE ingredients SET count = count + 1 WHERE id = ?
                    """,
                    (ingredient_id[0],)
                )

# many to many junction table, will be used to get recipes based on ingredients
def fill_junction(connection: sqlite3.Connection, recipe_id, ingredients):
    for ingredient in ingredients:
        if not len(ingredient) == 0:
            # get ingredient ID
            ingredient_id = connection.execute(
                """
                SELECT id FROM ingredients WHERE name = ?
                """,
                (ingredient,)
            ).fetchone()

            if ingredient_id:
                # id returns as tuple
                ingredient_id = ingredient_id[0]
                # insert keys into table
                connection.execute(
                    """
                    INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?, ?)
                    """,
                    (recipe_id, ingredient_id)
                )
    connection.commit()
