import pandas as pd
import streamlit as st
import os
import requests
from duckduckgo_search import DDGS
from fastcore.all import *
from PIL import Image
import numpy as np


def search_images(term, max_images=1):
    print(f"Searching for '{term}'")
    with DDGS() as ddgs:
        search_results = ddgs.images(keywords=term)
        image_data = list(search_results)
        image_urls = [item.get("image") for item in image_data[:max_images]]
        return L(image_urls)
    

def download_images(keyword, folder_path, max_images=1):
    urls = search_images(keyword, max_images)
    os.makedirs(folder_path, exist_ok=True)
    for i, url in enumerate(urls):
        image_filename = f"{keyword}_{i + 1}.jpg"
        image_path = os.path.join(folder_path, image_filename)
        try:
            img_data = requests.get(url).content
            img = Image.open(io.BytesIO(img_data))
            img.verify()
            with open(image_path, "wb") as f:
                f.write(img_data)
            print(f"Downloaded: {image_filename}")
        except Exception as e:
            print(f"Error downloading {image_filename}: {e}")


# Create Streamlit app 
df_new = pd.read_csv('stock_neuf_accessoires_guitares_basses.csv')

df = df_new.copy()

# Streamlit app title
st.title("Instrument Explorer")

# Dropdown to select an instrument
instrument_name = st.selectbox("Select an instrument:", df["Nom produit"].unique())

# Get the selected instrument details
instrument_data = df[df["Nom produit"] == instrument_name].iloc[0]

# Display instrument details
st.subheader("Instrument Details")
st.write(f"**Reference:** {instrument_data['Reference']}")
st.write(f"**Category:** {instrument_data['Categorie']}")
st.write(f"**Brand:** {instrument_data['Marque']}")
st.write(f"**Price (Euros):** {instrument_data['Prix']}")
st.write(f"**Quantite:** {instrument_data['Quantite']}")

# Get the instrument image
folder_path = '/Users/charlotte_lac/Documents/Music_project/pictures'

term = str(instrument_name)
download_images(term, 'streamlit_pictures', max_images= 1)
image_filename = f"{term}_{1}.jpg"
image_path = os.path.join('streamlit_pictures', image_filename)

# Display instrument image if it exists
if os.path.exists(image_path):
    st.image(image_path, caption=instrument_name)
else:
    st.write("No image available.")


# Display instrument image
#if "Image URL" in instrument_data and pd.notna(instrument_data["image_path"]):
#    st.image(instrument_data["image_path"], caption=instrument_name)
#else:
#    st.write("No image available.")