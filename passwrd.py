# filename: password_strength_app.py
import streamlit as st
import re

# Function to check password strength
def check_password_strength(password):
    strength = 0

    # Length check
    if len(password) >= 8:
        strength += 1
    # Contains both lowercase and uppercase
    if re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
        strength += 1
    # Contains digits
    if re.search(r'\d', password):
        strength += 1
    # Contains special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        strength += 1

    # Determine strength
    return strength

# Streamlit UI
st.title("🔐 Password Strength Analyzer")
st.write("Enter a password to check its strength:")

password = st.text_input("Password", type="password")

if password:
    strength = check_password_strength(password)
    st.write(f"Password Strength: **{strength/5}**")