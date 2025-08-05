FROM python:3.11-slim

WORKDIR /app

COPY . .

# ✅ Fix: Install netcat (Debian slim needs netcat-openbsd)
RUN apt-get update && apt-get install -y netcat-openbsd

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy wait-for-it and give permissions
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 8000

# Start the app after DB is ready
CMD ["/wait-for-it.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"]
