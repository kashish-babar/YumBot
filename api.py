import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")

BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients"

def get_recipes(ingredients, number=3):
    try:
        params = {
            "apiKey": API_KEY,
            "ingredients": ingredients,
            "number": number,
            "ranking": 1
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        recipes = response.json()
        return recipes
    except requests.exceptions.RequestException as e:
        print("❌ Error while fetching recipes:", e)
        return None







def get_recipe_details(recipe_id):
    try:
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions"
        params = {
            "apiKey": API_KEY
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None  # No instructions found

        steps = data[0].get("steps", [])
        instructions = [step["step"] for step in steps]
        return instructions

    except requests.exceptions.RequestException as e:
        print("❌ Error fetching recipe details:", e)
        return None
