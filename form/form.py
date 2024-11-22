import streamlit as st
import pandas as pd
import os
import yagmail
from datetime import date

# Configure email credentials (replace with your own email and app password)
EMAIL_ADDRESS = "your_email@gmail.com"
BUSINESS_EMAIL = "business_email@gmail.com"
yag = yagmail.SMTP(EMAIL_ADDRESS)

# Define the new clients ledger file
new_clients_file = "new_clients.csv"

# Load courses data for competencies dropdown
courses_file = "/mount/src/skills/data/courses.csv"
if os.path.exists(courses_file):
    courses_df = pd.read_csv(courses_file)
    courses_df["Display"] = courses_df["Course Code"] + " - " + courses_df["Course Name"]
    course_options = courses_df["Display"].tolist()
else:
    st.error("Courses file not found. Please upload 'courses.csv'!")
    course_options = []

# Email Sending Function
def send_email(to, subject, content):
    try:
        yag.send(to=to, subject=subject, contents=content)
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Confirmation Email for Client
def send_confirmation_email(client_email, client_name):
    subject = "Thank you for your submission!"
    content = f"""
    Hi {client_name},

    Thank you for registering with us! We have received your details and will get back to you shortly.

    Best regards,
    Your Business Team
    """
    send_email(client_email, subject, content)

# Notification Email for Business
def send_notification_email(client_data):
    subject = "New Client Registration"
    content = f"""
    A new client has submitted their details:

    Name: {client_data['Name']}
    DOB: {client_data['DOB']}
    Phone: {client_data['Phone']}
    Email: {client_data['Email']}
    Competencies: {client_data['Competencies']}

    Please review their details in the new_clients.csv file.
    """
    send_email(BUSINESS_EMAIL, subject, content)

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
        
        # Send emails
        send_confirmation_email(client_data["Email"], client_data["Name"])
        send_notification_email(client_data)
        
        st.success("Registration successful! A confirmation email has been sent.")
