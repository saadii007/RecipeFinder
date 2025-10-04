import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

st.set_page_config(page_title="Food Recipe Generator", page_icon="🍳", layout="wide")

st.title("Food Recipe Generator")

age = st.number_input("Enter your age", min_value=18, step=1)
height = st.number_input("Enter your height (in cm)", min_value=120, step=1)
weight = st.number_input("Enter your weight (in kg)", min_value=50, step=1)
fitness_goals = ["Weight Loss", "Muscle Gain", "Maintaining Weight", "Other"]
selected_goal = st.selectbox("Select your fitness goal", fitness_goals)

food_preferences = ["Hindu", "Jain", "Vegetarian", "Vegan", "Gluten-free"]
selected_food = st.selectbox("Select food preference", food_preferences)

cuisines = ["Italian", "Asian", "Mexican", "Mediterranean", "Other"]
cuisine_type = st.selectbox("Select preferred cuisine type", cuisines)

diet_restrictions = ["Low-carb", "Nut-free", "Vegan", "Vegetarian", "Other"]
diet_pref = st.selectbox("Select dietary restrictions", diet_restrictions)

num_recipes = st.number_input("Number of recipes to generate", min_value=1, max_value=10, step=1, value=1)

if st.button("Generate Recipes"):
    recipes = []
    for _ in range(num_recipes):
        prompt = f"Recipe for a {age}-year-old {selected_goal.lower()} {selected_food} {cuisine_type} dish - Ingredients:"
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(inputs, max_length=400, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
        recipe = tokenizer.decode(outputs[0], skip_special_tokens=True)
        recipes.append(recipe)

    for idx, recipe in enumerate(recipes, start=1):
        st.markdown(f"**Recipe {idx}:**")
        st.text(recipe)
