import streamlit as st
import pandas as pd
import os
import yagmail
import base64
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
from datetime import date
import io

# Email configuration
EMAIL_ADDRESS = "leon.lenzo.1@gmail.com"
BUSINESS_EMAIL = "leon.lenzo.1@gmail.com"
yag = yagmail.SMTP(EMAIL_ADDRESS, st.secrets["EMAIL_PASSWORD"])

# Google Drive API setup
credentials_base64 = st.secrets["GOOGLE_CREDENTIALS"]
credentials_json = base64.b64decode(credentials_base64).decode("utf-8")
creds = service_account.Credentials.from_service_account_info(
    json.loads(credentials_json)
)

drive_service = build('drive', 'v3', credentials=creds)

# Folder and File IDs
FOLDER_ID = st.secrets["FOLDER_ID"]
existing_file_id = "1k4pPHBUvX7ubOgIdRXUCbP2T2WwuAQvGdnbUgCDYAgc"

# Load courses data for competencies dropdown
courses_file = "../data/courses.csv"
if os.path.exists(courses_file):
    courses_df = pd.read_csv(courses_file)
    courses_df["Display"] = courses_df["Course Code"] + " - " + courses_df["Course Name"]
    course_options = courses_df["Display"].tolist()
else:
    st.error("Courses file not found. Please upload 'courses.csv'!")
    course_options = []

# Function to download Google Sheets as CSV
def download_from_drive(file_id, output_path):
    try:
        # Use 'export_media' for Google Docs/Sheets
        request = drive_service.files().export_media(fileId=file_id, mimeType='text/csv')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        with open(output_path, "wb") as f:
            f.write(fh.read())
    except Exception as e:
        st.error(f"Failed to download existing data: {e}")


# Function to upload file to Google Drive
def upload_to_drive(file_path, file_name):
    file_metadata = {
        'name': file_name,
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype='text/csv')
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return uploaded_file.get('id')

# Function to append new data to the existing file
def append_to_drive(file_id, new_data, temp_csv="temp_clients.csv"):
    # Step 1: Download the existing file
    try:
        download_from_drive(file_id, temp_csv)
        existing_data = pd.read_csv(temp_csv)
    except FileNotFoundError:
        # If the file doesn't exist, create it
        existing_data = pd.DataFrame()

    # Step 2: Append new data
    updated_data = pd.concat([existing_data, pd.DataFrame([new_data])], ignore_index=True)

    # Step 3: Save and upload the updated file
    updated_data.to_csv(temp_csv, index=False)
    try:
        upload_to_drive(temp_csv, "new_clients.csv")
        os.remove(temp_csv)
        st.success("Data successfully appended to Google Drive.")
    except Exception as e:
        st.error(f"Failed to upload updated data: {e}")

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

    Please review their details in Google Drive.
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

        # Append the new client data to the existing file
        append_to_drive(existing_file_id, client_data)
        
        # Send emails
        send_confirmation_email(client_data["Email"], client_data["Name"])
        send_notification_email(client_data)
        
        st.success("Registration successful! A confirmation email has been sent.")
