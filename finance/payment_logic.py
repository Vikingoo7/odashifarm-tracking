from datetime import datetime

# Calculate which months are still unpaid
def get_due_months(total_paid, monthly_fee, months_passed):
    months_paid = total_paid // monthly_fee
    months_due = months_passed - months_paid

    months_list = []
    if months_due > 0:
        today = datetime.today()
        for month_number in range(1, months_passed + 1):
            expected_payment = month_number * monthly_fee
            if expected_payment > total_paid:
                month_name = datetime(today.year, month_number, 1).strftime('%B')
                months_list.append(month_name)
    return months_list