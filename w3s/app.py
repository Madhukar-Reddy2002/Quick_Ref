import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape HTML, CSS, SQL, or Django template tags from w3schools website
def scrape_data(selection):
    if selection.lower() == "html":
        url = 'https://www.w3schools.com/tags/default.asp'
    elif selection.lower() == "css":
        url = 'https://www.w3schools.com/cssref/default.asp'
    elif selection.lower() == "sql":
        url = 'https://www.w3schools.com/sql/sql_ref_keywords.asp'
    else:
        st.error("Invalid selection! Please select 'HTML', 'CSS', 'SQL' ")
        return None

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    tag_names = []
    descriptions = []

    # Loop through each table on the webpage
    for table in soup.find_all('table'):
        # Loop through each row in the table
        for row in table.find_all('tr'):
            tds = row.find_all('td')
            if len(tds) == 2:
                tag_names.append(tds[0].getText(strip=True))
                descriptions.append(tds[1].getText(strip=True))

    return pd.DataFrame({'Tag': tag_names, 'Description': descriptions})

# Set the page title
st.set_page_config(page_title="HTML/CSS/SQL/Django Reference", layout="wide")

# Display the title and a brief description
st.title("HTML/CSS/SQL Quick Reference")
st.write("This application provides a user-friendly reference for HTML tags, CSS properties, SQL keywords, and Django template tags.")

# Add some styling to the page
st.markdown("""
    <style>
        .stApp {
            font-family: Arial, sans-serif;
        }
        .stSelectbox, .stExpander {
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            padding: 16px;
            margin-bottom: 16px;
        }
        .stHeader {
            color: #333;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .stMarkdown {
            color: #666;
            line-height: 1.6;
        }
        .stCode {
            background-color: #f0f0f0;
            border-radius: 5px;
            padding: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Ask user to select between HTML, CSS, SQL, and Django
selection = st.sidebar.selectbox("Select a Language", ["HTML", "CSS", "SQL"])

# Load the data based on user selection
df = scrape_data(selection)

if df is not None:
    # Create a dropdown menu for tag selection
    selected_tag = st.sidebar.selectbox("Select a Tag", df['Tag'].tolist())

    # Find the description for the selected tag
    description = df.loc[df['Tag'] == selected_tag, 'Description'].iloc[0]

    # Display the description and HTML/CSS/SQL/Django tag
    st.header(f"Description of '{selected_tag}'")
    st.markdown(f"**Tag:** `{selected_tag}`")
    st.markdown(f"**Description:** {description}")
    if selection.lower() == "html":
        st.code(f"<{selected_tag}>", language='html')
    elif selection.lower() == "css":
        st.code(f"{selected_tag} ", language='css')
    elif selection.lower() == "sql":
        st.code(f"{selected_tag}", language='sql')