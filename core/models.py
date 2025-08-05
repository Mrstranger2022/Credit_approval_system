import datetime
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15, unique=True)
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField()
    current_debt = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.FloatField()
    tenure = models.IntegerField(help_text="in months",default=12)
    interest_rate = models.FloatField(default=10.0)
    monthly_repayment = models.FloatField(default=0.0)
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField(default=datetime.date.today())
    end_date = models.DateField(default=datetime.date.today())
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Loan #{self.id} - {self.customer.first_name} {self.customer.last_name}"


