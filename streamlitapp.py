import pandas as pd
import streamlit as st
import os
import requests
from duckduckgo_search import DDGS
from fastcore.all import *
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as img 



def fetch_instrument_image(instrument_name, brand=None):
    """Fetches an image URL for a given instrument using DuckDuckGo image search."""
    query = f"{brand} {instrument_name} instrument" if brand else f"{instrument_name} instrument"
    results = ddg_images(query, max_results=1)
    
    if results:
        return results[0]['image']  # Return first image URL
    else:
        return None  # Return None if no image is found


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




df_new = pd.read_csv('/Users/charlotte_lac/Documents/Music_project/stock_neuf_accessoires_guitares_basses.csv')
term = str(df_new.loc[0]['Nom produit'])

download_images(term, 'pictures', max_images= 1)
