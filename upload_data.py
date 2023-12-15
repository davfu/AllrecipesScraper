import json
import jsonlines
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./service_key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

jsonlines_file = 'recipes2.jsonlines'

with open(jsonlines_file, 'r') as file:
    for line in file:
        recipe_data = json.loads(line.strip())
        db.collection('recipes').add(recipe_data)

print("data upload complete.")