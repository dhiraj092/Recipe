import streamlit as st
from openai import OpenAI

api_key = st.secrets['api_key']

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)

# App title and description
st.title("AI Recipe Finder")
st.write("Let's find a recipe based on what you have!")

# Main ingredients input
main_ingredients = st.text_input("What main ingredients do you have?")

# Common pantry items checklist
st.write("Do you have these common ingredients?")
col1, col2 = st.columns(2)

with col1:
    has_salt = st.checkbox("Salt", value=True)
    has_pepper = st.checkbox("Pepper", value=True)
    has_oil = st.checkbox("Cooking Oil", value=True)
    has_garlic = st.checkbox("Garlic", True)

with col2:
    has_onion = st.checkbox("Onion")
    has_butter = st.checkbox("Butter")
    has_herbs = st.checkbox("Common Herbs")
    has_stock = st.checkbox("Stock/Broth")

# Generate recipe button
if st.button("Find Recipe"):
    if main_ingredients:
        with st.spinner("Creating your personalized recipe..."):
            # Build the ingredient list
            available_basics = []
            if has_salt: available_basics.append("salt")
            if has_pepper: available_basics.append("pepper")
            if has_oil: available_basics.append("cooking oil")
            if has_garlic: available_basics.append("garlic")
            if has_onion: available_basics.append("onion")
            if has_butter: available_basics.append("butter")
            if has_herbs: available_basics.append("herbs")
            if has_stock: available_basics.append("stock")

            try:
                # Create the prompt
                prompt = f"""
                Main ingredients available: {main_ingredients}
                Basic ingredients available: {', '.join(available_basics)}

                Please create a recipe that:
                1. Uses the main ingredients
                2. Only uses the basic ingredients listed as available
                3. Suggests simple substitutes for any important missing ingredients
                4. Specifies cuisine type
                
                Format as:
                CUISINE TYPE:
                RECIPE NAME:
                COOKING TIME:
                DIFFICULTY:
                
                INGREDIENTS:
                (list ingredients)
                
                POSSIBLE SUBSTITUTIONS:
                (if any ingredient is missing)
                
                INSTRUCTIONS:
                (step by step)
                """

                # Get recipe from OpenAI
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a creative chef who specializes in making flexible recipes with available ingredients."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                # Display the recipe
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error generating recipe: {str(e)}")
    else:
        st.warning("Please enter your main ingredients first!")