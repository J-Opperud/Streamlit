import streamlit as st

# -----------------------------
# Quiz Questions
# -----------------------------
questions = [
    {
        "question": "Which pandas method is used to count missing values in each column?",
        "options": [
            "df.duplicated().sum()",
            "df.isnull().sum()",
            "df.dropna()",
            "df.describe()"
        ],
        "answer": 1
    },
    {
        "question": "Which pandas method removes duplicate rows from a DataFrame?",
        "options": [
            "df.remove_duplicates()",
            "df.clean_duplicates()",
            "df.drop_duplicates()",
            "df.delete_duplicates()"
        ],
        "answer": 2
    },
    {
        "question": "What does errors='coerce' do when used with pd.to_numeric()?",
        "options": [
            "Deletes the entire column",
            "Converts invalid values to NaN",
            "Converts all values to strings",
            "Stops the program when it finds an invalid value"
        ],
        "answer": 1
    },
    {
        "question": "Which chart type is best for comparing discrete categories such as departments or products?",
        "options": [
            "Line chart",
            "Histogram",
            "Scatter plot",
            "Bar chart"
        ],
        "answer": 3
    },
    {
        "question": "Which chart type is best for showing how a numeric variable is distributed?",
        "options": [
            "Histogram",
            "Bar chart",
            "Line chart",
            "Pie chart"
        ],
        "answer": 0
    }
]


# -----------------------------
# Initialize Session State
# -----------------------------
if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False


# -----------------------------
# Restart Quiz
# -----------------------------
def restart_quiz():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False


# -----------------------------
# Results Screen
# -----------------------------
if st.session_state.current_question >= len(questions):
    st.title("🎉 Quiz Complete!")

    score = st.session_state.score
    total = len(questions)

    st.metric("Final Score", f"{score} / {total}")

    percentage = int((score / total) * 100)

    if percentage == 100:
        st.success("Perfect score! You know your Pandas data cleaning and visualization concepts.")
    elif percentage >= 60:
        st.success(f"Nice work! You scored {percentage}%.")
    else:
        st.error(f"You scored {percentage}%. Review the lesson and try again!")

    st.progress(score / total)

    if st.button("🔄 Restart", use_container_width=True):
        restart_quiz()
        st.rerun()

    st.stop()


# -----------------------------
# Current Question
# -----------------------------
question_number = st.session_state.current_question + 1
total_questions = len(questions)
question = questions[st.session_state.current_question]

st.title("🐼 Pandas Data Cleaning & Visuals Quiz")

st.write(f"### Question {question_number} of {total_questions}")

# Progress bar
progress = question_number / total_questions
st.progress(progress)

st.divider()

# Question text
st.subheader(question["question"])

# Answer choices
selected_answer = st.radio(
    "Choose your answer:",
    question["options"],
    index=None,
    key=f"answer_{st.session_state.current_question}"
)


# -----------------------------
# Answer Submission
# -----------------------------
if not st.session_state.answered:

    if st.button("Submit Answer", type="primary", use_container_width=True):

        if selected_answer is None:
            st.warning("Please select an answer before submitting.")
        else:
            selected_index = question["options"].index(selected_answer)
            correct_index = question["answer"]

            st.session_state.answered = True

            if selected_index == correct_index:
                st.session_state.score += 1
                st.success("✅ Correct!")
            else:
                correct_answer = question["options"][correct_index]
                st.error("❌ Incorrect!")
                st.info(f"**Correct answer:** {correct_answer}")

            st.write(
                f"**Current score:** "
                f"{st.session_state.score} / {question_number}"
            )


# -----------------------------
# Next Question
# -----------------------------
if st.session_state.answered:

    if st.session_state.current_question < total_questions - 1:
        if st.button("Next Question ➡️", use_container_width=True):
            st.session_state.current_question += 1
            st.session_state.answered = False
            st.rerun()

    else:
        if st.button("View Results 🎯", type="primary", use_container_width=True):
            st.session_state.current_question += 1
            st.rerun()
