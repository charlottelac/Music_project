import pandas as pd
import streamlit as st
import os
import requests
import io
from duckduckgo_search import DDGS
from fastcore.all import *
from PIL import Image

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

# Load datasets
df_2 = pd.read_csv('https://drive.google.com/uc?id=1Y8O8WElfZOcwU9ISZ6p1tWlsPbH4R5Fy', delimiter=",") #neuf_guitares_etbasses
df_1 = pd.read_csv('https://drive.google.com/uc?id=1pfzDTY7KK_mRaYZdW7EODKhGR1Dmo6hd', delimiter=",") #neuf_accessoires_guitares_basses
df = pd.concat([df_1, df_2], axis=0)

if df.empty:
    st.write("No instruments available.")
    st.stop()

# Streamlit app title
st.title("Instrument Explorer")

# Initialize the current index
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

instrument_data = df.iloc[st.session_state.current_index]
instrument_name = instrument_data['Nom produit']

# Display instrument details
st.subheader("Instrument Details")
st.write(f"**Reference:** {instrument_data['Reference']}")
st.write(f"**Category:** {instrument_data['Categorie']}")
st.write(f"**Brand:** {instrument_data['Marque']}")
st.write(f"**Price:** {instrument_data['Prix']} Euros")
st.write(f"**Quantity:** {instrument_data['Quantite']}")

# Button to go through the list and select an instrument
if st.button("Next"): 
    st.session_state.current_index = (st.session_state.current_index + 1) % len(df)
    instrument_data = df.iloc[st.session_state.current_index]
    instrument_name = instrument_data['Nom produit']

rem = len(df)- st.session_state.current_index
st.write(f"{rem} **remaining items** ")

# Get the instrument image
folder_path = 'streamlit_pictures'
image_paths = download_images(str(instrument_name), folder_path, max_images=1)

# Display instrument image if it exists
if image_paths and os.path.exists(image_paths[0]) and image_paths[0].endswith(('.jpg', '.png', '.jpeg')):
    st.image(image_paths[0], caption=instrument_name, width=300)
else:
    st.warning("No image available or failed to fetch.")

# Initialize session state for wishlist if it doesn't exists
if "wish_list" not in st.session_state:
    st.session_state.wish_list = []

# Add to wish list button
if st.button("Add to wish list", key="add_wishlist"):
    st.session_state.wish_list.append(instrument_data.to_dict())
    st.success(f"Added {instrument_name} to your wishlist!")

# Download wishlist button
if st.button("Download wishlist", key="download_wishlist"):
    if len(st.session_state.wish_list) > 0:
        wishlist_df = pd.DataFrame(st.session_state.wish_list)
        csv = wishlist_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="wishlist.csv",
            mime="text/csv",
        )
    else:
        st.warning("Your wishlist is empty!")