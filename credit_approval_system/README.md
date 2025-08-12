# 💳 Credit Approval System (Django + DRF + PostgreSQL + Docker)

A RESTful backend service to handle customer registration, loan eligibility checks, loan creation, and viewing of loans — all containerized and production-ready.

---

## 🚀 Features

- ✅ Customer Registration
- ✅ Loan Eligibility Check based on financial rules
- ✅ Loan Creation with EMI calculation
- ✅ View All Loans for a Customer
- ✅ PostgreSQL database (Dockerized)
- ✅ Django REST Framework API
- ✅ Docker support for deployment

---

## 📦 Tech Stack

- Python 3.11
- Django 4.x
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose

---

## 📂 Project Structure

credit_approval_system/
├── core/ # App with business logic
├── credit_approval/ # Django project root
├── Dockerfile # App container config
├── docker-compose.yml # App + DB setup
├── requirements.txt
├── manage.py
└── README.md



 
Run via Docker

# Build and run the project
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate