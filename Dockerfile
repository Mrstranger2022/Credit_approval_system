FROM python:3.11-slim

WORKDIR /app

COPY . .


RUN apt-get update && apt-get install -y netcat-openbsd

# Install Python dependencies
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it and giving permissions
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 8000

# Starting app after DB is ready
CMD ["/wait-for-it.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"]
