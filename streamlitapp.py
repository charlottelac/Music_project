import pandas as pd
import streamlit as st
import os
import requests
import io
from duckduckgo_search import DDGS
from fastcore.all import *
from PIL import Image
import numpy as np

@st.cache_data  # Cache function to avoid re-fetching images
def search_images(term, max_images=1):
    print(f"Searching for '{term}'")
    with DDGS() as ddgs:
        search_results = ddgs.images(keywords=term)
        image_data = list(search_results)
        image_urls = [item.get("image") for item in image_data[:max_images]]
        return L(image_urls)
    
@st.cache_data  # Cache function to avoid re-downloading images
def download_images(keyword, folder_path, max_images=1):
    urls = search_images(keyword, max_images)
    os.makedirs(folder_path, exist_ok=True)
    image_paths = []
    
    for i, url in enumerate(urls):
        image_filename = f"{keyword}_{i + 1}.jpg"
        image_path = os.path.join(folder_path, image_filename)
        
        if not os.path.exists(image_path):  # Check if image already exists
            try:
                img_data = requests.get(url).content
                img = Image.open(io.BytesIO(img_data))
                img.verify()
                with open(image_path, "wb") as f:
                    f.write(img_data)
                print(f"Downloaded: {image_filename}")
            except Exception as e:
                print(f"Error downloading {image_filename}: {e}")
        image_paths.append(image_path)
    return image_paths

# Create Streamlit app 
df_2 = pd.read_csv('https://drive.google.com/uc?id=1Y8O8WElfZOcwU9ISZ6p1tWlsPbH4R5Fy',delimiter=",") #guitares_etbasses

df_1 = pd.read_csv('https://drive.google.com/uc?id=1pfzDTY7KK_mRaYZdW7EODKhGR1Dmo6hd',delimiter=",") #accessoires

df = pd.concat([df_1, df_2], axis = 0)

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
st.write(f"**Price:** {instrument_data['Prix']} Euros")
st.write(f"**Quantity:** {instrument_data['Quantite']}")

# Add to wish list button
# wish_list is a list, appened when button is clicked on, 
# then when download is clicked on the list is changed into a dataframe
wish_list = []
if st.button("Add to wish list", icon=":material/add_shopping_cart:"):
    wish_list.append(instrument_data)
    
st.button("Download wishlist", icon=":material/download:")


# Get the instrument image
folder_path = 'streamlit_pictures'
image_paths = download_images(str(instrument_name), folder_path, max_images=1)

# Display instrument image if it exists
if image_paths and os.path.exists(image_paths[0]):
    st.image(image_paths[0], caption=instrument_name)
else:
    st.write("No image available.")
