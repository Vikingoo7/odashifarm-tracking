import base64
from email.mime.text import MIMEText

# Create a Gmail message
def create_message(sender, to, subject, html_content):
    message = MIMEText(html_content, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

# Send the message through Gmail API
def send_message(service, user_id, message, email):
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"✅ Email successfully sent to {email}")
        return sent_message
    except Exception as error:
        print(f"❌ Failed to send email to {email}: {error}")
        return None