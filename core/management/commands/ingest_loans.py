import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Loan, Customer

class Command(BaseCommand):
    help = "Ingest loans from Excel into the Loan model (skips duplicates & missing customers)"

    def handle(self, *args, **kwargs):
        file_path = 'core/data/loan_data.xlsx'
        df = pd.read_excel(file_path)

        # Keep Excel's case, but strip spaces
        df.columns = df.columns.str.strip()

        added_count = 0
        skipped_count = 0
        error_count = 0

        for _, row in df.iterrows():
            try:
                customer_id = row["Customer ID"]
                loan_id = row["Loan ID"]

                # Skip if loan already exists
                if Loan.objects.filter(id=loan_id).exists():
                    self.stdout.write(f"⚠️ Skipping loan {loan_id} (already exists)")
                    skipped_count += 1
                    continue

                # Skip if customer does not exist
                try:
                    customer = Customer.objects.get(id=customer_id)
                except Customer.DoesNotExist:
                    self.stdout.write(f"⚠️ Skipping loan {loan_id} — customer {customer_id} not found")
                    skipped_count += 1
                    continue

                Loan.objects.create(
                    id=loan_id,
                    customer=customer,
                    loan_amount=row["Loan Amount"],
                    tenure=row["Tenure"],
                    interest_rate=row["Interest Rate"],
                    monthly_repayment=row["Monthly payment"],
                    emis_paid_on_time=row["EMIs paid on Time"],
                    start_date=pd.to_datetime(row["Date of Approval"]).date() if pd.notna(row["Date of Approval"]) else None,
                    end_date=pd.to_datetime(row["End Date"]).date() if pd.notna(row["End Date"]) else None,
                    active=True
                )
                added_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error processing loan record: {e}"))
                error_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Loans imported successfully. {added_count} added, {skipped_count} skipped, {error_count} errors."
        ))
