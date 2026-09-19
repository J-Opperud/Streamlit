import requests
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Data Explorer",
    page_icon="📊",
    layout="wide",
    )


@st.cache_data
def fetch_users():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        timeout=10,
        )
    response.raise_for_status()
    return response.json()



# Fetch and transform data
#-----------------------------------------------
users = fetch_users()

rows = [
    {
        "Name": user["name"],
        "City": user["address"]["city"],
        "Company": user["company"]["name"],
    }

    for user in users
    ]

df = pd.DataFrame(rows)


# Page title
#-----------------------------------------------
st.title("📊 Data Explorer")
st.write("Explore user data from JSONPlaceholder.")


# Sidebar filter
#-----------------------------------------------
st.sidebar.header("Filters")
name_filter = st.sidebar.text_input("Filter by name")

if name_filter:
    filtered_df = df[
        df["Name"].str.contains(name_filter, case=False, na=False)
        ]
else:
    filtered_df = df


# Metrics
#-----------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Users", len(df))

with col2:
    st.metric("Unique Cities", df["City"].nunique())

with col3:
    st.metric("Unique Companies", df["Company"].nunique())


# User table
#-----------------------------------------------
st.subheader("Users")
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    )


# City chart
#-----------------------------------------------
st.subheader("Users per City")

city_counts = (
    filtered_df["City"]
    .value_counts()
    .rename_axis("City")
    .reset_index(name="Users")
    )

st.bar_chart(
    city_counts,
    x="City",
    y="Users",
    )
