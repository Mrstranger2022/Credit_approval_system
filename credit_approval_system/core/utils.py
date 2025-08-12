
from datetime import date
from .models import Customer, Loan

def calculate_credit_score(customer):
    loans = Loan.objects.filter(customer=customer)
    score = 100

    # Rule: If total debt exceeds limit → credit score = 0
    if customer.current_debt > customer.approved_limit:
        return 0

    total_loans = loans.count()
    on_time = sum(loan.emis_paid_on_time for loan in loans)
    current_year = date.today().year
    this_year_loans = loans.filter(start_date__year=current_year).count()
    total_volume = sum(loan.loan_amount for loan in loans)

    # Apply weights (example logic)
    if total_loans > 0:
        score -= (total_loans * 2)
    score += (on_time * 0.5)
    score -= (this_year_loans * 1)
    score -= (total_volume / 100000)  # reduce 1 point per lakh

    return max(int(score), 0)
