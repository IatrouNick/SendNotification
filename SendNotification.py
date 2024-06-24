import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv, dotenv_values
import os

# Load environment variables from .env file
load_dotenv()

# Load recipient emails from .recipients.env file
recipient_env = dotenv_values(".recipients.env")
recipient_list = recipient_env.get("RECIPIENTS", "").split(",")

def send_email(sender_email, sender_password, receiver_email, subject, body):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Log in to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(msg)
        print(f"Email sent successfully to {receiver_email}!")

    except Exception as e:
        print(f"Failed to send email to {receiver_email}: {e}")

    finally:
        # Terminate the SMTP session and close the connection
        server.quit()

def send_emails_to_list(sender_email, sender_password, receiver_list, subject, body):
    for receiver_email in receiver_list:
        send_email(sender_email, sender_password, receiver_email.strip(), subject, body)

# Example usage
if __name__ == "__main__":
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')

    subject = "Test Email"
    body = "This is a test email sent from Python script."

    send_emails_to_list(sender_email, sender_password, recipient_list, subject, body)
