import streamlit as st
import pickle
import json
import numpy as np

# Load the model and feature columns
with open('model.pickle', 'rb') as f:
    model = pickle.load(f)

with open('columns.json', 'r') as f:
    columns = json.load(f)

# Extract location names (assuming first 3 columns are sqft, bath, bhk)
location_columns = columns[3:]

# UI Design Improvements
st.set_page_config(page_title="House Price Predictor", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏡 House Price Prediction</h1>", unsafe_allow_html=True)

# User Inputs
st.sidebar.header("Enter Property Details")
total_sqft = st.sidebar.number_input("📏 Total Square Feet", min_value=1.0, value=1000.0)
bath = st.sidebar.number_input("🛁 Bathrooms", min_value=1, step=1, value=2)
bhk = st.sidebar.number_input("🛏 Bedrooms (BHK)", min_value=1, step=1, value=2)
location = st.sidebar.selectbox("📍 Location", location_columns)

# Prediction Logic
if st.sidebar.button("🔮 Predict Price"):
    x = [0] * len(columns)
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk

    # Find the index of the selected location
    loc_index = columns.index(location)
    x[loc_index] = 1

    # Make prediction
    predicted_price = model.predict([x])[0] * 100000  # Convert Lakhs to INR
    formatted_price = f"{predicted_price:,.0f}"  # Format with commas

    # Display the Result
    st.markdown(f"""
    <div style="text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
        <h2>🏠 Estimated Price: <span style="color: #d9534f;">₹ {formatted_price}</span></h2>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><p style='text-align: center;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
