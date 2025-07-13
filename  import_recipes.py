import sqlite3
import json

DB_PATH = "recipes.db"
JSON_PATH = "recipes_import.json"

def add_recipe(title, category, time=None, ingredients=None, method=None, notes=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO recipes (title, category, time, ingredients, method, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, category, time, ingredients, method, notes))
    conn.commit()
    conn.close()

def import_recipes():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        recipes = json.load(f)
    for recipe in recipes:
        add_recipe(
            title=recipe["title"],
            category=recipe["category"],
            time=recipe.get("time"),
            ingredients=recipe.get("ingredients"),
            method=recipe.get("method"),
            notes=recipe.get("notes")
        )
    print(f"Импортировано {len(recipes)} рецептов.")

if __name__ == "__main__":
    import_recipes()