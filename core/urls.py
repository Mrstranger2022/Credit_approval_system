from django.urls import path
from .views import RegisterCustomerView
from .views import CheckLoanEligibilityView
from .views import CreateLoanView

urlpatterns = [
    path('register', RegisterCustomerView.as_view(), name='register-customer'),
    path('check-eligibility', CheckLoanEligibilityView.as_view(), name='check-eligibility'),
    path('create-loan', CreateLoanView.as_view()),
]
