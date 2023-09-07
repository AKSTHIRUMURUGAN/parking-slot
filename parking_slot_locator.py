import streamlit as st

# Set page title and icon
st.set_page_config(
    page_title="Parking Slot Locator",
    page_icon="🚗",
)

# Create a grey navbar
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create the navigation bar
nav_selection = st.sidebar.radio("Navigation", ["HOME", "ABOUT"])

# Define the content for each page
if nav_selection == "HOME":
    st.title("Parking Slot Locator - HOME")
    st.write("This is the home page content.")
    # You can add more content and code related to the home page here.

elif nav_selection == "ABOUT":
    st.title("Parking Slot Locator - ABOUT")
    st.write("This is the about page content.")
    # You can add more content and code related to the about page here.
