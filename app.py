import streamlit as st
import openai
import os
import requests

# ✅ Directly Set Your API Keys Here (Highly Reliable)
openai.api_key = "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"
unsplash_access_key = "JqfJi40vhNDfD9x8AFzDN3KXKxwAZVZpqc0d9juf2K0RE"

# ✅ Function to Fetch Images from Unsplash
def get_recipe_images(recipes):
    if not unsplash_access_key:
        return ["https://via.placeholder.com/300?text=Image+Unavailable"] * len(recipes)
    
    img_urls = []
    for recipe in recipes:
        dish_name = recipe.split('\n')[0]
        url = f"https://api.unsplash.com/photos/random?query={dish_name}&client_id={unsplash_access_key}"
        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.json()
            if 'urls' in img_data:
                img_urls.append(img_data['urls']['regular'])
            else:
                img_urls.append("https://via.placeholder.com/300?text=Image+Unavailable")
        else:
            img_urls.append("https://via.placeholder.com/300?text=Image+Unavailable")
    
    return img_urls

# ✅ Streamlit UI
st.title("🍳 AI-Powered Food Recipe Generator")

# User Inputs
age = st.number_input("Enter your age", min_value=18, step=1)
height = st.number_input("Enter your height (in centimeters)", min_value=120, step=1)
weight = st.number_input("Enter your weight (in kilograms)", min_value=55, step=1)
fitness_goals_options = ["Weight Loss", "Muscle Gain", "Maintaining Weight", "Other"]
selected_fitness_goal = st.selectbox("Select your fitness goal", fitness_goals_options)

protein_preference_options = ["Vegetarian", "Chicken", "Fish", "Vegan", "Pork", "Mutton", "Beef"]
selected_protein_preference = st.selectbox("Select food preference", protein_preference_options)

cuisine_type_options = ["Indian", "Italian", "Asian", "Mexican", "Mediterranean", "Other"]
cuisine_type = st.selectbox("Select preferred cuisine type", cuisine_type_options)

dietary_restrictions_options = ["Low-carb", "Nut-free", "Vegan", "Vegetarian", "None"]
dietary_restrictions = st.selectbox("Select dietary restrictions or preferences", dietary_restrictions_options)

num_recipes = st.number_input("Number of recipes to generate", min_value=1, max_value=10, step=1, value=1)

# ✅ Generate Recipes Button
if st.button("Generate Recipes"):
    recipes = []

    # ✅ Generating Recipes
    with st.spinner("Generating recipes..."):
        for _ in range(num_recipes):
            prompt = (
                f"Generate a recipe suitable for a {age}-year-old with a goal of {selected_fitness_goal.lower()}, "
                f"{height} cm tall, and {weight} kg in weight, that is {selected_protein_preference.lower()} "
                f"and has a {cuisine_type.lower()} influence"
            )
            if dietary_restrictions and dietary_restrictions != "None":
                prompt += f", while being {dietary_restrictions.lower()}"
            prompt += ". Include ingredients and nutritional information."

            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful recipe generator."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=400,
                    temperature=0.7
                )

                recipe = response.choices[0].message.content.strip()
                recipes.append(recipe)
            except openai.OpenAIError as e:
                st.error(f"OpenAI API Error: {str(e)}")
                recipes.append("Error generating this recipe.")

    # ✅ Displaying Recipes and Images
    st.subheader("Generated Recipes")
    img_urls = get_recipe_images(recipes)

    for idx, (recipe, img_url) in enumerate(zip(recipes, img_urls), start=1):
        st.markdown(f"### Recipe {idx}")
        st.text(recipe)
        st.image(img_url, caption=f"Image for Recipe {idx}", width=300)
