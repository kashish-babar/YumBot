import streamlit as st
from api import get_recipes, get_recipe_details

st.set_page_config(page_title="YumBot", page_icon="🍳")

st.title("🍽️ YumBot")
st.write("Enter the ingredients you have, and get delicious recipes!")

# Input from user
ingredients_input = st.text_input("📝 Ingredients (comma-separated):")

if st.button("Find Recipes"):
    if not ingredients_input.strip():
        st.warning("Please enter at least one ingredient.")
    else:
        with st.spinner("Searching for recipes..."):
            recipes = get_recipes(ingredients_input)

        if recipes is None:
            st.error("Something went wrong. Please check your internet or API key.")
        elif len(recipes) == 0:
            st.info("No recipes found. Try different ingredients.")
        else:
            st.success(f"Found {len(recipes)} recipe(s)!")
            for recipe in recipes:
                title = recipe.get("title", "No Title")
                recipe_id = recipe.get("id")
                image_url = recipe.get("image", "")
                url = f"https://spoonacular.com/recipes/{'-'.join(title.lower().split())}-{recipe_id}"

                st.markdown(f"---")
                st.image(image_url, width=250, caption=title)
                st.markdown(f"### [{title}]({url})")

                # Show used & missed ingredients
                used = [i['name'] for i in recipe.get("usedIngredients", [])]
                missed = [i['name'] for i in recipe.get("missedIngredients", [])]

                st.write(f"🟢 **You have:** {', '.join(used) if used else 'None'}")
                st.write(f"🔴 **You might need:** {', '.join(missed) if missed else 'Nothing!'}")

                # Show instructions
                instructions = get_recipe_details(recipe_id)
                if instructions:
                    with st.expander("👨‍🍳 Show Instructions"):
                        for idx, step in enumerate(instructions, 1):
                            st.write(f"{idx}. {step}")
                else:
                    st.info("No instructions available.")



st.markdown("---")
st.markdown("Made with ❤️ using [Spoonacular API](https://spoonacular.com/food-api) & Streamlit")

