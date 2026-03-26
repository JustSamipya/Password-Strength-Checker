import streamlit as st
import re
import string

# Function to check password strength
def check_password_strength(password):
    strength = 0
    feedback = []

    # Length check
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Use at least 8 characters.")

    # Lower + Upper case
    if re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
        strength += 1
    else:
        feedback.append("Include both uppercase and lowercase letters.")

    # Digits
    if re.search(r'\d', password):
        strength += 1
    else:
        feedback.append("Add at least one number (0-9).")

    # Special characters
    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        strength += 1
    else:
        feedback.append("Include at least one special character (!@#$...).")

    # Strength label
    if strength <= 1:
        label = "Weak 🔴"
    elif strength == 2 or strength == 3:
        label = "Medium 🟠"
    else:
        label = "Strong 🟢"

    return label, feedback
def estimate_crack_time(password):
    total = 0

    if any(c.islower() for c in password):
        total += 26
    if any(c.isupper() for c in password):
        total += 26
    if any(c.isdigit() for c in password):
        total += 10
    if any(c in string.punctuation for c in password):
        total += len(string.punctuation)

    length = len(password)

    if total == 0:
        return 0

    combinations = total ** length
    guesses_per_second = 1000000000  # 1 billion guesses/sec

    return combinations / guesses_per_second

# Format time nicely
def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.2f} minutes"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.2f} hours"
    days = hours / 24
    if days < 365:
        return f"{days:.2f} days"
    years = days / 365
    return f"{years:.2f} years"

# Streamlit UI
st.title("🔐 Password Strength Analyzer")
st.write("Enter a password to check its strength and crack time:")

password = st.text_input("Password", type="password")

if password:
    strength = check_password_strength(password)
    st.write(f"Password Strength: **{strength}**")

    crack_time_seconds = estimate_crack_time(password)
    formatted_time = format_time(crack_time_seconds)

    st.write(f"⏳ Estimated Time to Crack: **{formatted_time}**")
if __name__ == "__main__":
    pass
