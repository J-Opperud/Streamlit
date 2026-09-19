import requests
import streamlit as st



# Configuration
#-----------------------------------------------

API_URL = "http://127.0.0.1:8000"



# Page configuration
#-----------------------------------------------

st.set_page_config(
    page_title="Task Manager",
    page_icon="✅",
    layout="wide",
    )


# Session state
#-----------------------------------------------

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None


# Helper functions
# ------------------------------------------------

def login(username, password):
    """Authenticate with the FastAPI backend."""

    try:
        response = requests.post(
            f"{API_URL}/auth/token",
            data={
                "username": username,
                "password": password,
            },
            timeout=10,
            )

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.username = username
            return True, None

        if response.status_code == 401:
            return False, "Invalid username or password."

        return False, f"Login failed: HTTP {response.status_code}"

    except requests.exceptions.RequestException:

        return False, "Backend is unreachable. Make sure the FastAPI server is running."


def get_headers():
    """Return authorization headers for API requests."""

    return {
        "Authorization": f"Bearer {st.session_state.token}"
        }


def get_tasks():
    """Fetch tasks for the logged-in user."""

    try:
        response = requests.get(
            f"{API_URL}/tasks",
            headers=get_headers(),
            timeout=10,
            )

        if response.status_code == 401:
            logout()
            return None, "Your session has expired. Please log in again."

        response.raise_for_status()
        return response.json(), None

    except requests.exceptions.RequestException:
        return None, "Backend is unreachable. Make sure the FastAPI server is running."


def get_stats():
    """Fetch task statistics."""

    try:
        response = requests.get(
            f"{API_URL}/stats",
            headers=get_headers(),
            timeout=10,
        )

        if response.status_code == 401:
            logout()
            return None, "Your session has expired. Please log in again."

        response.raise_for_status()
        return response.json(), None

    except requests.exceptions.RequestException:
        return None, "Backend is unreachable. Make sure the FastAPI server is running."


def add_task(title):
    """Create a new task."""

    try:
        response = requests.post(
            f"{API_URL}/tasks",
            headers=get_headers(),
            json={"title": title},
            timeout=10,
            )

        if response.status_code == 401:
            logout()
            return False, "Your session has expired. Please log in again."

        if response.status_code == 201:
            return True, None

        return False, f"Could not create task: HTTP {response.status_code}"

    except requests.exceptions.RequestException:

        return False, "Backend is unreachable. Make sure the FastAPI server is running."


def toggle_task(task_id):
    """Toggle a task's completed status."""

    try:
        response = requests.patch(
            f"{API_URL}/tasks/{task_id}",
            headers=get_headers(),
            timeout=10,
            )

        if response.status_code == 401:
            logout()
            return False, "Your session has expired. Please log in again."

        if response.status_code == 200:
            return True, None

        return False, f"Could not update task: HTTP {response.status_code}"

    except requests.exceptions.RequestException:

        return False, "Backend is unreachable. Make sure the FastAPI server is running."


def logout():
    """Clear authentication information."""
    st.session_state.token = None
    st.session_state.username = None


# Login screen
#-----------------------------------------------

if not st.session_state.token:

    st.title("🔐 Task Manager")

    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                success, error = login(username, password)

                if success:
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(error)

    st.info(
        "Demo accounts: admin / password123  or  "
        "student / learn2026"
        )

    st.stop()


# Sidebar
# ----------------------------------------------

st.sidebar.title("👤 Account")
st.sidebar.write(f"Logged in as: **{st.session_state.username}**")

if st.sidebar.button("Logout"):
    logout()
    st.rerun()


# Main application
#-----------------------------------------------

st.title("✅ Task Manager")
st.write(f"Welcome, **{st.session_state.username}**!")


# Get statistics
#-----------------------------------------------
stats, stats_error = get_stats()

if stats_error:
    st.error(stats_error)

    if not st.session_state.token:
        st.rerun()

    st.stop()

# Metrics
#-----------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Tasks",
        stats["total"],
        )

with col2:
    st.metric(
        "Completed Tasks",
        stats["done"],
        )

# Add task
#-----------------------------------------------

st.subheader("➕ Add Task")

with st.form("add_task_form"):

    task_title = st.text_input(
        "Task title",
        placeholder="Enter a new task...",
        )

    add_submitted = st.form_submit_button(
        "Add Task",
        type="primary",
        )

    if add_submitted:

        if not task_title.strip():
            st.warning("Please enter a task title.")
        else:
            success, error = add_task(task_title.strip())

            if success:
                st.success("Task added successfully!")
                st.rerun()
            else:
                st.error(error)

                if not st.session_state.token:
                    st.rerun()


# Task list
#-----------------------------------------------

st.subheader("📋 Your Tasks")

tasks, tasks_error = get_tasks()

if tasks_error:
    st.error(tasks_error)

    if not st.session_state.token:
        st.rerun()

else:
    if not tasks:
        st.info("You don't have any tasks yet.")

    else:
        for task in tasks:
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

            with col1:
                if task["done"]:
                    st.write("✅")
                else:
                    st.write("⬜")

            with col2:
                if task["done"]:
                    st.markdown(f"~~{task['title']}~~")
                    st.caption("Completed")
                else:
                    st.write(task["title"])
                    st.caption("Pending")

            with col3:
                button_label = "Undo" if task["done"] else "Complete"

                if st.button(
                    button_label,
                    key=f"toggle_{task['id']}",
                    ):
                    success, error = toggle_task(task["id"])

                    if success:
                        st.rerun()
                    else:
                        st.error(error)

                        if not st.session_state.token:
                            st.rerun()
