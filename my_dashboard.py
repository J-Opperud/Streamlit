import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Personal Fitness Dashboard",
    page_icon="💪",
    layout="wide",
    )

# ---------------------------------------------------------
# Workout data
# ---------------------------------------------------------
workouts = {
    "Monday": {
        "category": "Calisthenics",
        "focus": "Push",
        "exercises": [
            "Push-ups",
            "Diamond Push-ups",
            "Dips",
            "Pike Push-ups",
            "Plank",
            ],
        },
    "Tuesday": {
        "category": "Calisthenics",
        "focus": "Pull",
        "exercises": [
            "Pull-ups",
            "Chin-ups",
            "Australian Rows",
            "Dead Hang",
            "Hanging Knee Raises",
            ],
        },
    "Wednesday": {
        "category": "Light Cardio",
        "focus": "Jump Rope",
        "exercises": [
            "Basic Jump Rope",
            "High Knees",
            "Side-to-Side Jumps",
            "Boxer Step",
            ],
        },
    "Thursday": {
        "category": "Calisthenics",
        "focus": "Legs",
        "exercises": [
            "Bodyweight Squats",
            "Walking Lunges",
            "Bulgarian Split Squats",
            "Glute Bridges",
            "Calf Raises",
            ],
        },
    "Friday": {
        "category": "Calisthenics",
        "focus": "Full Body",
        "exercises": [
            "Burpees",
            "Push-ups",
            "Pull-ups",
            "Bodyweight Squats",
            "Mountain Climbers",
            "Plank",
            ],
        },
    "Saturday": {
        "category": "Rest",
        "focus": "Recovery",
        "exercises": [
            "Stretching",
            "Mobility Work",
            "Light Walking",
            ],
        },
    "Sunday": {
        "category": "Cardio",
        "focus": "Running",
        "exercises": [
            "Easy Run",
            "Warm-up Walk",
            "Cool-down Walk",
            ],
        },
}

# ---------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------
st.sidebar.title("⚙️ Dashboard Controls")

selected_day = st.sidebar.selectbox(
    "Select a day",
    list(workouts.keys()),
    )

category_filter = st.sidebar.radio(
    "Workout category",
    ["All", "Calisthenics", "Cardio", "Light Cardio", "Rest"],
    )

show_exercises = st.sidebar.checkbox(
    "Show exercise details",
    value=True,
    )   

duration = st.sidebar.slider(
    "Target workout duration (minutes)",
    min_value=15,
    max_value=90,
    value=45,
    step=5,
    )

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("💪 Personal Fitness Dashboard")

st.markdown(
    "### Weekly training overview"
    )
st.caption(
    "A simple personal dashboard for tracking calisthenics, jump rope, "
    "running, and recovery."
    )

# ---------------------------------------------------------
# Filter main content based on sidebar
# ---------------------------------------------------------
selected_workout = workouts[selected_day]

if category_filter != "All":
    if selected_workout["category"] != category_filter:

        st.warning(
            f"**{selected_day}** is a "
            f"**{selected_workout['category']}** workout, "
            f"not a **{category_filter}** workout."
            )

# ---------------------------------------------------------
# Metrics row
# ---------------------------------------------------------
total_training_days = 6
calisthenics_days = 4
cardio_days = 2

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(
        "Training Days",
        total_training_days,
        delta="+1 this week",
        )   

with metric2:

    st.metric(
        "Calisthenics Days",
        calisthenics_days,
        delta="+1 day",
        )


with metric3:

    st.metric(
        "Cardio Sessions",
        cardio_days,
        delta="+30 min",
        )


with metric4:

    st.metric(
        "Target Duration",
        f"{duration} min",
        delta="+5 min",
        )


st.divider()

# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------
overview_tab, details_tab = st.tabs(
    ["📊 Overview", "📋 Details"]
    )

# ---------------------------------------------------------
# Overview tab
# ---------------------------------------------------------
with overview_tab:
    st.subheader(f"{selected_day} Workout")

    info1, info2, info3 = st.columns(3)

    with info1:

        st.markdown("**Category**")
        st.info(selected_workout["category"])

    with info2:

        st.markdown("**Focus**")
        st.info(selected_workout["focus"])

    with info3:

        st.markdown("**Target Duration**")
        st.info(f"{duration} minutes")

    st.markdown("### Weekly Schedule")

    schedule_data = []

    for day, workout in workouts.items():
        schedule_data.append(
            {
                "Day": day,
                "Category": workout["category"],
                "Focus": workout["focus"],
                "Exercises": len(workout["exercises"]),
            }
        )

    schedule_df = pd.DataFrame(schedule_data)

    if category_filter != "All":
        filtered_df = schedule_df[

            schedule_df["Category"] == category_filter
            ]

        if filtered_df.empty:
            st.info(

                f"No workouts match the **{category_filter}** filter."
                )
        else:
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                )
    else:
        st.dataframe(
            schedule_df,
            use_container_width=True,
            hide_index=True,
            )

# ---------------------------------------------------------
# Details tab
# ---------------------------------------------------------
with details_tab:
    st.subheader(f"{selected_day} Exercise List")

    if show_exercises:

        for index, exercise in enumerate(
            selected_workout["exercises"], start=1
            ):
            st.write(f"**{index}.** {exercise}")
    else:
        st.info(
            "Exercise details are hidden. Enable "
            "'Show exercise details' in the sidebar."
            )

    st.markdown("### Training Structure")

    if selected_workout["category"] == "Calisthenics":

        st.success(
            "Focus on controlled bodyweight movements, good form, "
            "and progressive overload."
            )
    elif selected_workout["category"] in ["Cardio", "Light Cardio"]:

        st.success(
            "Keep the intensity controlled and focus on consistent "
            "cardiovascular work."
            )
    else:
        st.info(
            "Use this day for recovery, mobility, and preparing "
            "for the next training session."
            )

# ---------------------------------------------------------
# Expander
# ---------------------------------------------------------
st.divider()

with st.expander("💡 Training Notes & Recommendations"):

    st.markdown(
        """
        **Weekly structure**

        - **Monday:** Calisthenics — Push
        - **Tuesday:** Calisthenics — Pull
        - **Wednesday:** Light cardio — Jump rope
        - **Thursday:** Calisthenics — Legs
        - **Friday:** Calisthenics — Full body
        - **Saturday:** Rest and recovery
        - **Sunday:** Running

        **General reminders**

        - Warm up before each workout.
        - Prioritize proper exercise technique.
        - Increase repetitions or difficulty gradually.
        - Stay hydrated throughout the day.
        - Allow adequate recovery between hard sessions.
        """
        )

