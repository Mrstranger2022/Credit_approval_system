from rest_framework import serializers
from .models import Customer, Loan


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'age', 'monthly_salary', 'phone_number', 'approved_limit']
        read_only_fields = ['id', 'approved_limit']

    def create(self, validated_data):
        salary = validated_data.get('monthly_salary')
        # Round to nearest lakh: example 655000 → 700000
        approved_limit = round(36 * salary / 100000) * 100000
        validated_data['approved_limit'] = approved_limit
        return super().create(validated_data)

class LoanEligibilityRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()


class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()


class LoanDetailSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            'id',
            'loan_amount',
            'tenure',
            'interest_rate',
            'monthly_repayment',
            'emis_paid_on_time',
            'start_date',
            'end_date',
            'active',
            'customer'
        ]

    def get_customer(self, obj):
        customer = obj.customer
        return {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age,
            "monthly_salary": customer.monthly_salary,
            "approved_limit": customer.approved_limit,
            "current_debt": customer.current_debt
        }



class LoanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            'id', 'loan_amount', 'tenure', 'interest_rate', 'monthly_repayment',
            'start_date', 'end_date', 'active'
        ]



