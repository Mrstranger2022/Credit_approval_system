import os
import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Customer, Loan
from datetime import datetime

class Command(BaseCommand):
    help = 'Ingest loan data from Excel file'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'data', 'loan_data.xlsx')
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            try:
                customer = Customer.objects.get(customer_id=row['customer_id'])

                Loan.objects.create(
                    customer=row["Customer"],
                    loan_id=row['Loan ID'],
                    loan_amount=row['Loan Amount'],
                    tenure=row['Tenure'],
                    interest_rate=row['Interest Rate'],
                    monthly_repayment=row['Monthly payment'],
                    emis_paid_on_time=row['EMIs paid on Time'],
                    start_date=pd.to_datetime(row['date of Approval']).date(),
                    end_date=pd.to_datetime(row['End Date']).date()
                )
            except Customer.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠️ Customer ID {row['customer_id']} not found. Skipping..."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error processing loan record: {e}"))

        self.stdout.write(self.style.SUCCESS('✅ Loans imported successfully.'))
