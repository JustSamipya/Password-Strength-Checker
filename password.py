import streamlit as st
import re
import string
import hashlib
import requests


# -------------------------------
# Password Strength Function
# -------------------------------
def check_password_strength(password):
    strength = 0
    feedback = []

    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Use at least 8 characters.")

    if re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
        strength += 1
    else:
        feedback.append("Include both uppercase and lowercase letters.")

    if re.search(r'\d', password):
        strength += 1
    else:
        feedback.append("Add at least one number (0-9).")

    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        strength += 1
    else:
        feedback.append("Include at least one special character (!@#$...).")

    if strength <= 1:
        label = "Weak 🔴"
    elif strength <= 3:
        label = "Medium 🟠"
    else:
        label = "Strong 🟢"

    return strength, label, feedback


# -------------------------------
# Crack Time Estimation
# -------------------------------
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
    guesses_per_second = 1_000_000_000

    return combinations / guesses_per_second


# -------------------------------
# Format Time
# -------------------------------
def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"


# -------------------------------
# HIBP Breach Check (SAFE METHOD)
# -------------------------------
def check_pwned(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    hashes = (line.split(":") for line in res.text.splitlines())

    for h, count in hashes:
        if h == suffix:
            return int(count)

    return 0




# -------------------------------
# UI
# -------------------------------
st.title("🔐 Advanced Password Security Analyzer")

show_password = st.checkbox("Show Password")

password = st.text_input(
    "Enter Password",
    type="default" if show_password else "password"
)

common_passwords = ["123456", "password", "qwerty", "admin", "abc123"]

# -------------------------------
# MAIN
# -------------------------------
if password:
    strength, label, feedback = check_password_strength(password)

    st.subheader("Strength Meter")
    st.progress(strength / 4)

    st.write(f"Password Strength: **{label}**")

    if password.lower() in common_passwords:
        st.error("⚠️ This is a very common password!")

    # Feedback
    if feedback:
        st.subheader("💡 Suggestions")
        for f in feedback:
            st.write(f"- {f}")

    # Crack time
    seconds = estimate_crack_time(password)
    st.write(f"⏳ Crack Time: **{format_time(seconds)}**")

    # -------------------------------
    # 🌐 BREACH CHECK
    # -------------------------------
    st.subheader("🌐 Data Breach Check")

    breach_count = check_pwned(password)

    if breach_count is None:
        st.warning("Could not check breach database.")
    elif breach_count > 0:
        st.error(f"⚠️ This password has been found {breach_count} times in data breaches!")
    else:
        st.success("✅ This password was NOT found in known breaches.")



# -------------------------------
if __name__ == "__main__":
    pass