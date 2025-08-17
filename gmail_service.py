import os
import json
import base64
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

def get_gmail_service():
    # Decode token.json from base64 stored in .env
    token_data = base64.b64decode(os.getenv("TOKEN_JSON_B64"))
    creds_info = json.loads(token_data.decode("utf-8"))

    creds = Credentials.from_authorized_user_info(
        creds_info, ["https://www.googleapis.com/auth/gmail.send"]
    )
    service = build("gmail", "v1", credentials=creds)
    return service

def send_email(to, subject, body_text):
    service = get_gmail_service()
    sender = os.getenv("SENDER_EMAIL")

    message = MIMEText(body_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    # Encode email to base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    message = {"raw": raw_message}

    try:
        sent = service.users().messages().send(userId="me", body=message).execute()
        print(f"✅ Email sent successfully: {sent['id']}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
