import requests
import os
import pandas as pd
import spacy

csv_file = "food_log.csv"
API_KEY = "9o8oUhMVRBKoL7NKjq0qUsYZYlvfsV2OlHdXwCYM"
nlp = spacy.load("en_core_web_sm")

def extract_food_items(food_sentence):
    doc = nlp(food_sentence.lower())

    food_items = []
    current_food = []

    for token in doc:
        if token.pos_ in ["NOUN", "ADJ"]:  # Keep only food-related words
            current_food.append(token.lemma_)  # Lemmatize words
        elif token.text in [",", "and"]:  # Separator found, store previous food
            if current_food:
                food_items.append(" ".join(current_food))
                current_food = []

    if current_food:  # Add last item if any
        food_items.append(" ".join(current_food))

    return food_items


#sentence = "Rice with grilled chicken and broccoli"
#detected_foods = extract_food_items(sentence)
#print("✅ Detected Food Items:", detected_foods)

def search_food_api(food_name):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&pageSize=3&dataType=Branded,Survey%20(FNDDS)&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("foods", [])


def select_food_from_results(food_results, food_name):
    print(f"\n✅ Food options found for '{food_name}':")
    
    for i, food in enumerate(food_results[:5]):
        print(f"{i + 1}. {food['description']}")

    choice = int(input("\nEnter the number of the food you want to select (1-5): ")) - 1
    return food_results[choice] if 0 <= choice < len(food_results) else None


def log_meal_to_csv(meal_name, selected_foods):
    columns = ["Date", "Meal", "Food Items", "Total Calories"]

    # Ensure CSV exists
    if not os.path.exists(csv_file):
        print("⚠️ CSV file not found. Creating a new one...")
        df = pd.DataFrame(columns=columns)
        df.to_csv(csv_file, index=False)

    # Read existing CSV
    df = pd.read_csv(csv_file)

    # Combine selected foods into one meal
    meal_foods = ", ".join([food["description"] for food in selected_foods])
    total_calories = sum(food.get("foodNutrients", [{}])[0].get("value", 0) for food in selected_foods)

    # Append new meal
    new_entry = pd.DataFrame([[pd.Timestamp.today().strftime("%Y-%m-%d"), meal_name, meal_foods, total_calories]], columns=columns)
    df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(csv_file, index=False)
    print("✅ Meal logged successfully!")


def food_tracking():
    user_input = input("🍽️ Enter everything you ate in one sentence: ")
    
    detected_foods = extract_food_items(user_input)
    selected_foods = []

    for food_name in detected_foods:
        food_results = search_food_api(food_name)

        if food_results:
            selected_food = select_food_from_results(food_results, food_name)
            if selected_food:
                selected_foods.append(selected_food)
        else:
            print(f"❌ No results found for '{food_name}'.")

    if selected_foods:
        log_meal_to_csv(user_input, selected_foods)

# Run the program
food_tracking()
