from django.urls import path
from .views import (RegisterCustomerView,
                    CheckLoanEligibilityView,
                    CreateLoanView,
                    ViewLoanDetailView,
                    ViewCustomerLoansView)

urlpatterns = [
    path('register', RegisterCustomerView.as_view(), name='register-customer'),
    path('check-eligibility', CheckLoanEligibilityView.as_view(), name='check-eligibility'),
    path('create-loan', CreateLoanView.as_view()),
    path('view-loan/<int:loan_id>/', ViewLoanDetailView.as_view()),
    path('view-loans/<int:customer_id>/', ViewCustomerLoansView.as_view()),
]
