from api import get_recipes, get_recipe_details



def clean_input(raw_input):
    # Split by comma, strip whitespace, and remove empty entries
    ingredients = [item.strip() for item in raw_input.split(",") if item.strip()]
    return ", ".join(ingredients)


def main():
    print("👋 Welcome to the Recipe Recommender Bot!")

    while True:
        user_input = input("\nEnter ingredients you have (comma-separated): ").strip()

        if not user_input:
            print("⚠️ You entered nothing. Please provide some ingredients.")
            continue

        cleaned_ingredients = clean_input(user_input)

        if not cleaned_ingredients:
            print("⚠️ No valid ingredients found. Try again.")
            continue

        print("🔍 Searching for recipes...")
        recipes = get_recipes(cleaned_ingredients)

        if recipes is None:
            print("❌ There was an error fetching recipes. Please try again later.")
        elif len(recipes) == 0:
            print("😕 No recipes found with those ingredients. Try different ones.")
        else:
            print(f"\n🍽️ Found {len(recipes)} recipe(s):\n")
            for i, recipe in enumerate(recipes, 1):
                title = recipe.get("title", "Unknown Recipe")
                id = recipe.get("id", "")
                url = f"https://spoonacular.com/recipes/{'-'.join(title.lower().split())}-{id}"
                print(f"{i}. {title}\n   👉 {url}")

                # Fetch detailed instructions
                instructions = get_recipe_details(id)
                if instructions:
                    print("   🧑‍🍳 Instructions:")
                    for step_num, step in enumerate(instructions, 1):
                        print(f"     {step_num}. {step}")
                else:
                    print("   ⚠️ No detailed instructions found.")

                print()  # newline for spacing


        # Ask if user wants to try again
        again = input("Would you like to search again? (y/n): ").strip().lower()
        if again != "y":
            print("👋 Thanks for using Recipe Bot! Goodbye!")
            break


if __name__ == "__main__":
    main()
