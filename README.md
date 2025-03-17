Instrument Explorer is a **Streamlit app** that allows users to browse, view, and create a wishlist of musical instruments using a dataset stored on a public Google Drive. The app fetches instrument images from the internet with DuckDuckgo and enables users to download their wishlist as a CSV file.

## Features
- **Select an instrument** from a dropdown list.
- **View instrument details** including reference, category, brand, price, and quantity.
- **Fetch instrument images** from the internet using DuckDuckGo image search.
- **Add instruments to a wishlist** to keep track of favorites.
- **Download the wishlist** as a CSV file for future reference.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Instrument-Explorer.git
cd Instrument-Explorer
```

### 2. Install Dependencies
Make sure you have **Python >= 3.** installed. Then, install required packages:
```bash
pip install -r requirements.txt
```

The app requires the following libraries:
```bash
streamlit
pandas
requests
PIL
fastcore
duckduckgo-search
```

### 3. Run the Streamlit App
```bash
streamlit run app.py
```

## Configuration
- **Google Drive Data**: The app loads instrument data from Google Drive using public CSV links. Ensure that the correct file IDs are used in the script.
- **Image Fetching**: The app uses DuckDuckGo to find images of the instruments. You must have an internet connection for this feature.

## File Structure
```
Instrument-Explorer/
│-- streamlitapp.py                # Main Streamlit application
│-- requirements.txt      # Required Python dependencies
│-- README.md             # Project documentation
│-- streamlit_pictures/   # Folder for locally stored images
```

## How to Use the app
**Run the app** with `streamlit run app.py`.
**View instrument details** and image (if available).
**Click Next** to view the following items.
**Click "Add to Wishlist"** to save an instrument.
**Click "Download Wishlist"** to export the selection as a CSV.

## License 
This project is open-source and available under the **MIT License**.

---
🔗 **Developed by Charlotte L**

