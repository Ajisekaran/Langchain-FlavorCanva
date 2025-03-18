import streamlit as st
from langchain_helper import generate_restaurant_name_and_items

st.title("FlavorCanva 🎨🍽️")

cuisine = st.sidebar.selectbox("Pick a Cuisine", ["Indian", "Chinese", "Italian", "Mexican", "American"])

if cuisine:
    response = generate_restaurant_name_and_items(cuisine)
    
    print("DEBUG RESPONSE:", response)

   
    if isinstance(response, dict) and "restaurant_name" in response and "menu_items" in response:
        st.header(response["restaurant_name"])  
        st.write("**Menu Items:**")
        
        for i, item in enumerate(response["menu_items"], start=1):
            st.write(f"{i}. {item}")  
    else:
        st.error("Unexpected response format! Check console for details.")



