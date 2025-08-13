import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Customer

class Command(BaseCommand):
    help = "Ingest customers from Excel file (skips duplicates)"

    def handle(self, *args, **kwargs):
        file_path = 'core/data/customer_data.xlsx'
        df = pd.read_excel(file_path)

        # Keep column names exactly as in Excel (strip spaces)
        df.columns = df.columns.str.strip()

        added_count = 0
        skipped_count = 0

        for _, row in df.iterrows():
            if Customer.objects.filter(id=row['Customer ID']).exists():
                self.stdout.write(f"⚠️ Skipping customer {row['Customer ID']} (already exists)")
                skipped_count += 1
                continue

            Customer.objects.create(
                id=row['Customer ID'],  # Primary key
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=row['Phone Number'],
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit']
            )
            added_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Customers imported successfully. {added_count} added, {skipped_count} skipped."
        ))
