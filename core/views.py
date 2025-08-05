from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerRegistrationSerializer
from .models import Customer
from .serializers import LoanEligibilityRequestSerializer
from .utils import calculate_credit_score
from .serializers import CreateLoanSerializer
from .models import Loan
from .utils import calculate_credit_score
from datetime import timedelta
import datetime

class RegisterCustomerView(APIView):
    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CheckLoanEligibilityView(APIView):
    def post(self, request):
        serializer = LoanEligibilityRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            customer = Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        credit_score = calculate_credit_score(customer)

        # Compound Interest Monthly EMI Formula
        P = data['loan_amount']
        R = data['interest_rate'] / 12 / 100
        N = data['tenure']
        if R == 0:
            EMI = P / N
        else:
            EMI = P * R * (1 + R)**N / ((1 + R)**N - 1)

        total_current_emi = sum(
            loan.monthly_repayment for loan in customer.loans.filter(active=True)
        )

        income_threshold = 0.5 * customer.monthly_salary
        corrected_rate = data['interest_rate']

        # Interest rate slab correction
        if credit_score > 50:
            approved = True
        elif 30 < credit_score <= 50:
            if corrected_rate <= 12:
                corrected_rate = 13
            approved = True
        elif 10 < credit_score <= 30:
            if corrected_rate <= 16:
                corrected_rate = 17
            approved = True
        else:
            approved = False

        if total_current_emi + EMI > income_threshold:
            approved = False

        return Response({
            "customer_id": customer.id,
            "approval": approved,
            "interest_rate": data['interest_rate'],
            "corrected_interest_rate": corrected_rate,
            "tenure": data['tenure'],
            "monthly_installment": round(EMI, 2),
        })


class CreateLoanView(APIView):
    def post(self, request):
        serializer = CreateLoanSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            customer = Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        credit_score = calculate_credit_score(customer)

        P = data['loan_amount']
        R = data['interest_rate'] / 12 / 100
        N = data['tenure']
        if R == 0:
            EMI = P / N
        else:
            EMI = P * R * (1 + R)**N / ((1 + R)**N - 1)

        # Check EMI burden
        current_emi = sum(loan.monthly_repayment for loan in customer.loans.filter(active=True))
        if current_emi + EMI > 0.5 * customer.monthly_salary:
            return Response({
                "loan_id": None,
                "customer_id": customer.id,
                "loan_approved": False,
                "message": "EMI exceeds 50% of monthly salary",
                "monthly_installment": None,
            }, status=200)

        # Interest rate correction logic
        corrected_rate = data['interest_rate']
        approved = False

        if credit_score > 50:
            approved = True
        elif 30 < credit_score <= 50:
            if corrected_rate <= 12:
                corrected_rate = 13
            approved = True
        elif 10 < credit_score <= 30:
            if corrected_rate <= 16:
                corrected_rate = 17
            approved = True
        else:
            return Response({
                "loan_id": None,
                "customer_id": customer.id,
                "loan_approved": False,
                "message": "Credit score too low for loan approval",
                "monthly_installment": None,
            }, status=200)

        # Create Loan
        start_date = datetime.date.today()
        end_date = start_date + timedelta(days=30 * N)
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=P,
            tenure=N,
            interest_rate=corrected_rate,
            monthly_repayment=round(EMI, 2),
            start_date=start_date,
            end_date=end_date,
            active=True,
        )

        # Update current debt
        customer.current_debt += P
        customer.save()

        return Response({
            "loan_id": loan.id,
            "customer_id": customer.id,
            "loan_approved": True,
            "message": "Loan approved",
            "monthly_installment": round(EMI, 2)
        }, status=201)
