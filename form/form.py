import streamlit as st
import pandas as pd
import os
from datetime import date

# Load courses data for competencies dropdown
courses_file = "courses.csv"
if os.path.exists(courses_file):
    courses_df = pd.read_csv(courses_file)
    courses_df["Display"] = courses_df["Course Code"] + " - " + courses_df["Course Name"]
    course_options = courses_df["Display"].tolist()
else:
    st.error("Courses file not found. Please upload 'courses.csv'!")
    course_options = []

# Define the new clients ledger file
new_clients_file = "new_clients.csv"

# Create the form
st.title("Client Registration Form")

with st.form("registration_form"):
    name = st.text_input("Full Name", placeholder="Enter your name")
    dob = st.date_input(
        "Date of Birth",
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )
    phone = st.text_input("Phone Number", placeholder="Enter your phone number")
    email = st.text_input("Email Address", placeholder="Enter your email")
    competencies = st.multiselect(
        "Select Prior Competencies Achieved",
        options=course_options,
        help="Search and select all applicable competencies. Format: Course Code - Course Name"
    )
    
    # Submit button
    submitted = st.form_submit_button("Register")

st.write("Current working directory:", os.getcwd())

if submitted:
    # Validate inputs
    if not name or not email:
        st.error("Name and Email are required fields.")
    elif len(phone) < 10:
        st.error("Please enter a valid phone number.")
    else:
        # Prepare data for saving
        client_data = {
            "Name": name,
            "DOB": dob.strftime("%Y-%m-%d"),
            "Phone": phone,
            "Email": email,
            "Competencies": "; ".join(competencies)
        }
        
        # Save data to the new_clients file
        if not os.path.exists(new_clients_file):
            pd.DataFrame([client_data]).to_csv(new_clients_file, index=False)
        else:
            new_clients_df = pd.read_csv(new_clients_file)
            new_clients_df = new_clients_df.append(client_data, ignore_index=True)
            new_clients_df.to_csv(new_clients_file, index=False)
        
        st.success("Registration successful!")
        st.write("Your details have been submitted for review.")
