import smtplib

# Replace with your credentials
username = 'leon.lenzo.1@gmail.com'
password = 'golokpnruqcjmkcn'

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # Secure the connection
        smtp.login(username, password)  # Log in
        print("Login successful!")
except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication failed: {e}")
