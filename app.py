import streamlit as st
from api import get_recipes, get_recipe_details


st.markdown(
    """
    <style>
        .stApp {
            background-color: #f9dbe3;
            color: #1f1f1f;
        }

        html, body, [class*="css"] {
            color: #1f1f1f !important;
        }

        label, .css-1y0tads, .stTextInput label {
            color: #1f1f1f !important;
            font-weight: 600;
        }

        .stTextInput > div > div > input {
            background-color: #fff;
            border: 1px solid #c0395f;
            padding: 10px;
            border-radius: 6px;
            color: #1f1f1f;
        }

        .stSelectbox > div {
            color: #1f1f1f !important;
            background-color: #fff;
        }

        .stButton > button {
            background-color: #c0395f;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.6em 1.2em;
        }

        .streamlit-expanderHeader, .stSidebar {
            background-color: #f6c7d5 !important;
            color: #1f1f1f !important;
        }

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #1f1f1f;
        }

        .css-1v0mbdj, .css-qrbaxs, .css-ffhzg2 {
            color: #1f1f1f !important;
        }

        hr {
            border: none;
            border-top: 1px solid #c0395f;
        }
    </style>
""",
    unsafe_allow_html=True,
)


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
                used = [i["name"] for i in recipe.get("usedIngredients", [])]
                missed = [i["name"] for i in recipe.get("missedIngredients", [])]

                st.write(f"🟢 **You have:** {', '.join(used) if used else 'None'}")
                st.write(
                    f"🔴 **You might need:** {', '.join(missed) if missed else 'Nothing!'}"
                )

                # Show instructions
                instructions = get_recipe_details(recipe_id)
                if instructions:
                    with st.expander("👨‍🍳 Show Instructions"):
                        for idx, step in enumerate(instructions, 1):
                            st.write(f"{idx}. {step}")
                else:
                    st.info("No instructions available.")


st.markdown("---")
st.markdown(
    "Made with ❤️ using [Spoonacular API](https://spoonacular.com/food-api) & Streamlit"
)
