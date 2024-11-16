import streamlit as st
import requests
from bs4 import BeautifulSoup

# App title
st.title("FXPro Shares Trading Information")

# Function to scrape content from the website
def scrape_fxpro_shares():
    url = "https://www.fxpro.com/trading/shares"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Example: Extract specific sections of interest
        # Modify this section based on the actual structure of the page
        header = soup.find("h1").text if soup.find("h1") else "No Header Found"
        paragraphs = soup.find_all("p")
        content = "\n\n".join([p.text for p in paragraphs])
        
        return header, content
    else:
        return None, f"Error: Unable to fetch data (Status code: {response.status_code})"

# Fetch and display content
header, content = scrape_fxpro_shares()

if header:
    st.header(header)
    st.text_area("Content", content, height=400)
else:
    st.error(content)
