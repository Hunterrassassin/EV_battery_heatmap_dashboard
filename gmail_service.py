from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64

# Load credentials from token.json
def get_gmail_service():
    creds = Credentials.from_authorized_user_file(
        "token.json",
        ["https://www.googleapis.com/auth/gmail.send"]
    )
    service = build("gmail", "v1", credentials=creds)
    return service


def send_email(to, subject, body_text):
    service = get_gmail_service()

    # Explicitly set FROM (must be same Gmail as authorized account)
    sender = "sanidhya.gupta26@gmail.com"

    message = MIMEText(body_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    message = {"raw": raw_message}

    try:
        sent = service.users().messages().send(userId="me", body=message).execute()
        print(f"✅ Email sent successfully to {to}: {sent['id']}")
        print(f"📨 From: {sender}")
        print(f"📨 To: {to}")
        print(f"📨 Subject: {subject}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
