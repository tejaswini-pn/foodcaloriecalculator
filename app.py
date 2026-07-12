import tkinter as tk
from tkinter import ttk, messagebox
import requests
import ttkbootstrap as tb
import matplotlib.pyplot as plt

API_KEY = 'aOPJ2tH0NbV0kUbyG8K5dLTIegBhEsLjPFe4Y3vb'

current_nutrients = {}
activities = {
    "Walking (5 km/h)": 3.5,
    "Running (8 km/h)": 8.3,
    "Cycling (moderate)": 6.8,
    "Jump Rope": 12.0,
    "Yoga": 2.5
}

def search_food_usda(food_name, weight=100):
    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    headers = {'Content-Type': 'application/json'}
    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 5
    }

    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"An error occurred: {e}")
        return None

    if not results.get('foods'):
        return None

    for item in results['foods']:
        name = item.get('description', 'Unknown')
        fdc_id = item.get('fdcId')
        confirm = messagebox.askyesno("Confirm Food", f"Use data for: {name}?")
        if confirm:
            return fetch_nutrients(fdc_id, weight)
    return None

def fetch_nutrients(fdc_id, weight):
    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    nutrients = {}
    for item in data.get('foodNutrients', []):
        nutrient_info = item.get('nutrient', {})
        name = nutrient_info.get('name') or item.get('nutrientName')
        value = item.get('amount') or item.get('value')
        if name and value is not None:
            nutrients[name] = value

    factor = weight / 100
    return {
        "name": data.get('description', 'Unknown'),
        "calories": round(nutrients.get('Energy', 0) * factor, 2),
        "protein": round(nutrients.get('Protein', 0) * factor, 2),
        "fat": round(nutrients.get('Total lipid (fat)', 0) * factor, 2),
        "carbs": round(nutrients.get('Carbohydrate, by difference', 0) * factor, 2)
    }

def search_and_display():
    food = entry.get()
    try:
        weight = float(weight_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid weight.")
        return

    if not food:
        messagebox.showerror("Input Error", "Enter a food name.")
        return

    result = search_food_usda(food, weight)
    if result:
        label_result.config(
            text=f"Food: {result['name']}\n"
                 f"Calories: {result['calories']} kcal\n"
                 f"Protein: {result['protein']} g\n"
                 f"Fat: {result['fat']} g\n"
                 f"Carbs: {result['carbs']} g"
        )
        global current_nutrients
        current_nutrients = result
        button_pie.pack(pady=10)
        button_workout.pack(pady=10)
    else:
        messagebox.showinfo("No Data", "No food data found.")

def show_pie_chart():
    if not current_nutrients:
        messagebox.showerror("No Data", "Search for a food first.")
        return

    labels = ['Protein', 'Fat', 'Carbs']
    values = [
        current_nutrients['protein'],
        current_nutrients['fat'],
        current_nutrients['carbs']
    ]
    filtered_labels = [label for i, label in enumerate(labels) if values[i] > 0.1]
    filtered_values = [val for val in values if val > 0.1]

    plt.figure(figsize=(6, 6))
    plt.pie(filtered_values, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
    plt.title(f"Nutrient Breakdown for {current_nutrients['name']}")
    plt.axis('equal')
    plt.show()

def show_workout_inputs():
    if not entry_weight.winfo_ismapped():
        ttk.Label(root, text="Enter your weight (kg):", font=("Segoe UI", 12)).pack()
        entry_weight.pack(pady=5)

        ttk.Label(root, text="Select workout type:", font=("Segoe UI", 12)).pack()
        activity_choice.pack(pady=5)

        button_calculate.pack(pady=5)
        label_workout_result.pack(pady=10)

def calculate_workout_needed():
    try:
        weight = float(entry_weight.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid weight.")
        return

    activity = activity_choice.get()
    if not activity:
        messagebox.showerror("Select Activity", "Please choose an activity.")
        return

    met = activities[activity]
    calories = current_nutrients["calories"]
    cal_per_min = (met * weight * 3.5) / 200
    minutes_needed = round(calories / cal_per_min, 2)

    label_workout_result.config(
        text=f"To burn {calories} kcal from {current_nutrients['name']},\n"
             f"you need to do {activity} for approx. {minutes_needed} minutes."
    )

# --- UI Setup ---

root = tb.Window(themename="flatly")
root.title("Food Calorie and Workout Calculator")

label_food = ttk.Label(root, text="Enter Food Item", font=("Georgia", 14))
label_food.pack(pady=20)

entry = ttk.Entry(root, width=60, font=("Georgia", 12))
entry.pack(pady=10)

label_weight = ttk.Label(root, text="Enter Weight (grams)", font=("Georgia", 14))
label_weight.pack(pady=10)

weight_entry = ttk.Entry(root, width=60, font=("Georgia", 12))
weight_entry.pack(pady=10)

search_button = tb.Button(root, text="Search", command=search_and_display, width=20, bootstyle="info")
search_button.pack(pady=20)

label_result = ttk.Label(root, text="", font=("Arial", 12), anchor="w")
label_result.pack(pady=15)

button_pie = tb.Button(root, text="Show Pie Chart", bootstyle="success", command=show_pie_chart, width=20)
button_workout = tb.Button(root, text="Workout Time Estimate", bootstyle="warning", command=show_workout_inputs, width=20)

# Workout section (created once globally)

entry_weight = ttk.Entry(root, font=("Segoe UI", 12), width=20)
activity_choice = ttk.Combobox(root, values=list(activities.keys()), font=("Segoe UI", 12), state="readonly", width=40)
button_calculate = tb.Button(root, text="Calculate Workout", bootstyle="info", command=calculate_workout_needed)
label_workout_result = ttk.Label(root, text="", font=("Arial", 11))

# Start app

root.mainloop()

