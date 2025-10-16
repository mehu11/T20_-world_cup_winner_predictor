import streamlit as st
import pickle
import pandas as pd
import numpy as np
from PIL import Image

# Load the model and transformers
try:
    pipe = pickle.load(open('pipe.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model file not found. Please check the path to 'pipe.pkl'.")

# Define teams and cities
teams = ['Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 
         'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka']
cities = ['Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 
          'Cape Town', 'London', 'Pallekele', 'Barbados', 'Sydney', 
          'Melbourne', 'Durban', 'St Lucia', 'Wellington', 'Lauderhill', 
          'Hamilton', 'Centurion', 'Manchester', 'Abu Dhabi', 'Mumbai', 
          'Nottingham', 'Southampton', 'Mount Maunganui', 'Chittagong', 
          'Kolkata', 'Lahore', 'Delhi', 'Nagpur', 'Chandigarh', 'Adelaide', 
          'Bangalore', 'St Kitts', 'Cardiff', 'Christchurch', 'Trinidad']

# Streamlit layout
title = 'ICC MEN T20 WORLD CUP SCORE PREDICTOR'
st.markdown(f"<h1 style='text-align: center'>{title}</h1>", unsafe_allow_html=True)

try:
    image2 = Image.open("img2.jpg")
    st.image(image2)
except FileNotFoundError:
    st.warning("Image file 'img2.jpg' not found.")

# Input fields
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select bowling team', sorted(teams))
city = st.selectbox('Select city', sorted(cities))

col3, col4, col5 = st.columns(3)
with col3:
    current_score = st.number_input('Current Score', min_value=0)
with col4:
    overs = st.number_input('Overs done (works for over > 5)', min_value=5.0, max_value=20.0, step=0.1)
with col5:
    wickets = st.number_input('Wickets fallen', min_value=0, max_value=10)

last_five = st.number_input('Runs scored in last 5 overs', min_value=0)

if st.button('Predict Score'):
    if overs == 0:
        st.error("Overs cannot be 0. Please enter a valid number.")
    else:
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs

        # Create input DataFrame
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'current_score': [current_score],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'crr': [crr],
            'last_five': [last_five]
        })

        # Predict score
        try:
            result = pipe.predict(input_df)
            st.header("Predicted Score - " + str(int(result[0])))
        except Exception as e:
            st.error(f"Prediction failed. Error: {e}")

        # Winning team
        
            st.header("Winning team is - " + str[teams])
