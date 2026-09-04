# Food Calorie and Workout Calculator

Mini Project — Python for Data Science Laboratory https://foodcaloriecalculator.streamlit.app/

A desktop GUI application that looks up the nutritional content of any food item using the USDA FoodData Central API, visualizes its macronutrient breakdown, and estimates how much exercise is needed to burn off those calories.

## Problem Statement

Health-conscious individuals often lack easy access to accurate nutritional data and workout recommendations tailored to specific foods and quantities. This project provides an automated tool that determines the nutritional content of a food item and estimates the workout time required to burn the consumed calories.

## Objectives

- Retrieve nutritional information (calories, protein, fat, carbs) for any given food and weight
- Visualize the nutrient breakdown using pie charts
- Suggest the amount of physical activity needed to burn the consumed calories, based on the user's weight and selected exercise

## Dataset

- **Source:** [USDA FoodData Central API](https://fdc.nal.usda.gov/api-guide.html)
- **Type:** Real-time API data (not a static dataset)
- **Features used:** Energy (kcal), Protein (g), Fat (g), Carbohydrates (g)

## Tech Stack

- **Python 3.x**
- `tkinter` and `ttkbootstrap` — GUI interface
- `requests` — USDA API calls
- `matplotlib` — pie chart visualization
- `ttk` — widget styling and layout
- `messagebox` — input/output dialogues

## Methodology

1. **Input Collection** — User enters the food item and its weight in grams
2. **API Call** — A search query is sent to the USDA FoodData Central API
3. **Data Extraction** — Nutrients are fetched and scaled based on weight
4. **GUI Display** — Nutrient values are shown in the app interface
5. **Visualization** — A pie chart shows the distribution of protein, fat, and carbs (nutrients contributing less than 0.1g are filtered out to avoid clutter)
6. **Workout Calculation** — User enters their body weight and selects a workout; calories burned per minute are calculated using MET values, and the estimated minutes needed to burn the food's calories are displayed

## Setup

1. Clone the repository and install dependencies:
   ```bash
   pip install requests ttkbootstrap matplotlib
   ```
2. Get a free API key from [USDA FoodData Central](https://fdc.nal.usda.gov/api-key-signup.html).
3. Set it as an environment variable instead of hardcoding it in the script:
   ```bash
   export USDA_API_KEY="your_api_key_here"
   ```
   and load it in code with `os.environ["USDA_API_KEY"]`.
4. Run the app:
   ```bash
   python food_calorie_workout_calculator.py
   ```

> **Note:** The original script embeds the API key directly in the source. Do not commit real API keys to a public repository — use an environment variable or a `.env` file (excluded via `.gitignore`) instead.

## Example Output
<img width="398" height="483" alt="image" src="https://github.com/user-attachments/assets/1f0f30a7-ce35-403d-aea6-00e3f1f0feed" />

For 100g of chocolate cake:
- Calories: 439.0 kcal
- Protein: 3.03 g
- Fat: 22.73 g
- Carbs: 57.58 g

At 90 kg body weight, burning this via moderate cycling takes approximately 41 minutes.

## Results and Observations

- The application fetches accurate, detailed nutritional values for thousands of food items
- Users get a clear visual breakdown of macronutrient distribution
- The workout recommendation logic helps users connect food intake with physical effort

## Limitations

- Requires an internet connection (depends on the USDA API)
- Nutrient details vary based on food preparation (e.g., boiled vs. fried)

## Future Enhancements

- Historical tracking of meals
- Support for Indian food databases
- Option to export or share reports

## References

- [USDA API Documentation](https://fdc.nal.usda.gov/api-guide.html)
- [MET Values](https://gprehab.com/articles/metabolic-equivalents-mets/)
- [Tkinter Docs](https://docs.python.org/3/library/tk.html)
- [Matplotlib Docs](https://matplotlib.org/)
