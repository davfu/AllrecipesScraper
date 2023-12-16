import sqlite3
import json

con = sqlite3.connect("recipes.db")

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
            fat INTEGER
        )
        """
    )

def add_db_entry(connection: sqlite3.Connection, recipe):
    ingredients_str = ", ".join(recipe.ingredients)
    ingredients_len = len(recipe.ingredients)
    connection.execute(
        """
        INSERT OR REPLACE INTO recipes (
            url, title, rating, rev_count, ingredients, num_ingredients, cals, protein, carbs, fat
        ) VALUES (?,?,?,?,?,?,?,?,?,?)
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
        ),
    )

    connection.commit()