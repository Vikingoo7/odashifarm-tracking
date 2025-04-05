import pandas as pd
import time
from datetime import datetime
from auth.auth import gmail_authenticate
from emails.email_sender import create_message, send_message
from finance.payment_logic import get_due_months

# Main function to read Excel and send emails
def send_emails_from_excel(file_path):
    df = pd.read_excel(file_path)
    service = gmail_authenticate()
    sender = "odashifarm@gmail.com"

    # Load the base email template
    with open('emails/templates/template_base.html', 'r', encoding='utf-8') as f:
        base_template = f.read()

    # Load the payment message template
    with open('emails/templates/payment_message.html', 'r', encoding='utf-8') as f:
        payment_template = f.read()

    today = datetime.today()
    months_passed = today.month - 1  # We do not count the current month until it ends

    for index, row in df.iterrows():
        full_name = row.get('Name')
        email = row.get('Email')
        monthly_fee = row.get('MonthlyFee')
        total_paid = row.get('TotalPaid', 0)

        # Basic data validations
        if pd.isna(email) or not isinstance(email, str) or email.strip() == "":
            print(f"⚠️ No valid email found for {full_name}. Skipping.")
            continue
        if pd.isna(full_name) or not isinstance(full_name, str) or full_name.strip() == "":
            print(f"⚠️ No valid name for a row. Skipping.")
            continue
        if pd.isna(monthly_fee) or not isinstance(monthly_fee, (int, float)) or monthly_fee <= 0:
            print(f"⚠️ No valid monthly fee for {full_name}. Skipping.")
            continue

        # Extract first name
        first_name = full_name.strip().split(' ')[0]

        # Calculate owed amount
        expected_total = months_passed * monthly_fee
        owed_amount = expected_total - total_paid

        if owed_amount <= 0:
            print(f"✅ {full_name} is fully paid. No email needed.")
            continue

        # Get missing months
        missing_months = get_due_months(total_paid, monthly_fee, months_passed)
        months_text = ", ".join(missing_months)

        # Fill the payment block
        payment_block = payment_template.replace('{owed_amount}', f"{owed_amount:.2f}")\
                                        .replace('{months_text}', months_text)

        email_type = "Payment Reminder"
        subject = "Payment Reminder - Odashi Farm"

        # Fill the base email
        template_filled = base_template.replace('{name}', first_name)\
                                       .replace('{payment_block}', payment_block)\
                                       .replace('{email}', email)\
                                       .replace('{email_type}', email_type)

        # Send the email
        message = create_message(sender, email, subject, template_filled)
        send_message(service, 'me', message, email)

        # Pause between emails
        time.sleep(1)

if __name__ == '__main__':
    send_emails_from_excel('finance/Sample Data.xlsx')