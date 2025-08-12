import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Customer

class Command(BaseCommand):
    help = "Ingest customers from Excel file"

    def handle(self, *args, **kwargs):
        file_path = 'core/data/customer_data.xlsx'
        df = pd.read_excel(file_path)

        # Normalize column names for easier mapping
        df.columns = df.columns.str.strip()

        for _, row in df.iterrows():
            Customer.objects.create(
                id=row['Customer ID'],  # Primary key if your model uses default `id`
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=row['Phone Number'],
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit']
            )

        self.stdout.write(self.style.SUCCESS("✅ Customers imported successfully."))
