import streamlit as st
import requests
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NutriFit",
    page_icon="🍎",
    layout="centered"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(135deg, #f7fbf8 0%, #eef7f3 100%);
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: #173f35 !important;
        text-align: center;
        font-weight: 800 !important;
        font-size: 3rem !important;
        margin-bottom: 0.2rem !important;
    }

    h2, h3 {
        color: #173f35 !important;
        font-weight: 750 !important;
    }

    p, label {
        color: #33443e;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        border-radius: 12px !important;
        min-height: 46px;
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        min-height: 46px;
    }

    div[data-testid="stButton"] button {
        width: 100%;
        min-height: 48px;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e1ebe5;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #6d7c76;
        font-size: 14px;
    }

    div[data-testid="stMetricValue"] {
        color: #173f35;
        font-weight: 800;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    hr {
        border: none;
        height: 1px;
        background-color: #dce7e1;
        margin: 1.7rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# ACTIVITIES
# ============================================================

activities = {
    "Walking (5 km/h)": 3.5,
    "Running (8 km/h)": 8.3,
    "Cycling (moderate)": 6.8,
    "Jump Rope": 12.0,
    "Yoga": 2.5
}

# ============================================================
# SESSION STATE
# ============================================================

if "current_nutrients" not in st.session_state:
    st.session_state.current_nutrients = None

if "show_chart" not in st.session_state:
    st.session_state.show_chart = False

if "show_workout" not in st.session_state:
    st.session_state.show_workout = False

# ============================================================
# USDA SEARCH
# ============================================================

def search_food_usda(food_name, weight):

    api_key = st.secrets["USDA_API_KEY"]

    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": api_key,
        "query": food_name,
        "pageSize": 5
    }

    try:
        response = requests.get(
            search_url,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        results = response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

    foods = results.get("foods", [])

    if not foods:
        return None

    food = foods[0]

    fdc_id = food.get("fdcId")

    if not fdc_id:
        return None

    return fetch_nutrients(fdc_id, weight)

# ============================================================
# FETCH NUTRIENTS
# ============================================================

def fetch_nutrients(fdc_id, weight):

    api_key = st.secrets["USDA_API_KEY"]

    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"

    try:
        response = requests.get(
            url,
            params={"api_key": api_key},
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

    nutrients = {}

    for item in data.get("foodNutrients", []):

        nutrient_info = item.get("nutrient", {})

        name = (
            nutrient_info.get("name")
            or item.get("nutrientName")
        )

        value = (
            item.get("amount")
            if item.get("amount") is not None
            else item.get("value")
        )

        if name and value is not None:
            nutrients[name] = value

    factor = weight / 100

    return {
        "name": data.get("description", "Unknown"),
        "calories": round(
            nutrients.get("Energy", 0) * factor,
            2
        ),
        "protein": round(
            nutrients.get("Protein", 0) * factor,
            2
        ),
        "fat": round(
            nutrients.get("Total lipid (fat)", 0) * factor,
            2
        ),
        "carbs": round(
            nutrients.get("Carbohydrate, by difference", 0) * factor,
            2
        )
    }

# ============================================================
# HEADER
# ============================================================

st.title("🍎 NutriFit")

st.markdown(
    "<p style='text-align:center; font-size:18px;'>"
    "Food Calorie & Workout Calculator"
    "</p>",
    unsafe_allow_html=True
)

st.caption(
    "Discover nutrition, understand calories, and estimate workout time."
)

st.divider()

# ============================================================
# FOOD INPUT
# ============================================================

st.subheader("🥗 Food Information")

food = st.text_input(
    "Enter Food Item",
    placeholder="Example: Apple, Rice, Chocolate"
)

weight = st.number_input(
    "Enter Weight (grams)",
    min_value=1.0,
    value=100.0,
    step=1.0
)

if st.button(
    "🔍 Search Food",
    use_container_width=True,
    type="primary"
):

    if not food.strip():

        st.warning("Please enter a food name.")

    else:

        with st.spinner("Searching USDA FoodData Central..."):

            result = search_food_usda(
                food.strip(),
                weight
            )

        if result:

            st.session_state.current_nutrients = result
            st.session_state.show_chart = False
            st.session_state.show_workout = False

        else:

            st.session_state.current_nutrients = None

            st.error(
                "No food data found. Try a more specific food name."
            )

# ============================================================
# RESULTS
# ============================================================

if st.session_state.current_nutrients:

    result = st.session_state.current_nutrients

    st.divider()

    st.success(
        f"🍽️ Selected Food: {result['name']}"
    )

    st.subheader("📊 Nutrition Information")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🔥 Calories",
            f"{result['calories']} kcal"
        )

        st.metric(
            "🥑 Fat",
            f"{result['fat']} g"
        )

    with col2:

        st.metric(
            "💪 Protein",
            f"{result['protein']} g"
        )

        st.metric(
            "🍞 Carbohydrates",
            f"{result['carbs']} g"
        )

    st.divider()

    # ========================================================
    # PIE CHART
    # ========================================================

    chart_button_label = (
        "🙈 Hide Nutrient Chart"
        if st.session_state.show_chart
        else "📊 Show Nutrient Chart"
    )

    if st.button(
        chart_button_label,
        use_container_width=True
    ):

        st.session_state.show_chart = (
            not st.session_state.show_chart
        )

    if st.session_state.show_chart:

        labels = [
            "Protein",
            "Fat",
            "Carbs"
        ]

        values = [
            result["protein"],
            result["fat"],
            result["carbs"]
        ]

        filtered = [
            (label, value)
            for label, value in zip(labels, values)
            if value > 0.1
        ]

        if filtered:

            filtered_labels = [
                item[0]
                for item in filtered
            ]

            filtered_values = [
                item[1]
                for item in filtered
            ]

            fig, ax = plt.subplots(
                figsize=(6, 6)
            )

            ax.pie(
                filtered_values,
                labels=filtered_labels,
                autopct="%1.1f%%",
                startangle=90
            )

            ax.set_title(
                f"Nutrient Breakdown\n{result['name']}"
            )

            ax.axis("equal")

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

        else:

            st.info(
                "Not enough nutrient data to build a chart."
            )

    st.divider()

    # ========================================================
    # WORKOUT SECTION
    # ========================================================

    st.subheader("🏃 Workout Time Estimate")

    st.caption(
        "Estimate how long you would need to exercise "
        "to burn the calories in this food."
    )

    body_weight = st.number_input(
        "Your Weight (kg)",
        min_value=1.0,
        value=60.0,
        step=1.0,
        key="body_weight"
    )

    activity = st.selectbox(
        "Choose Workout",
        list(activities.keys())
    )

    if st.button(
        "🏋️ Calculate Workout Time",
        use_container_width=True,
        type="primary"
    ):

        met = activities[activity]

        calories = result["calories"]

        cal_per_min = (
            met * body_weight * 3.5
        ) / 200

        if cal_per_min > 0:

            minutes_needed = round(
                calories / cal_per_min,
                2
            )

            st.session_state.show_workout = True

            st.session_state.workout_result = (
                f"To burn {calories} kcal from "
                f"{result['name']}, you would need "
                f"approximately {minutes_needed} minutes "
                f"of {activity}."
            )

    if st.session_state.show_workout:

        st.success(
            "✅ " + st.session_state.workout_result
        )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🍎 NutriFit • Nutrition data powered by USDA FoodData Central"
)