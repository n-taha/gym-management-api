# 🏋️ Gym Management System API

A **RESTful Gym Management System API** built using **Django** and **Django REST Framework**.
This project provides a complete backend solution for managing gym operations including **authentication, fitness classes, memberships, subscriptions, instructors, and feedback**.
The API is fully documented using **Swagger (OpenAPI)**.

---

## 🚀 Features

### 🔐 Authentication & Security
- JWT-based authentication (Access & Refresh tokens)
- User registration & login
- Forgot password / reset password system


### 🏫 Fitness Classes & Booking
- Create, update, delete fitness classes
- Schedule classes with instructors
- Manage class capacity
- Online class booking system
- Member booking history

### 👤 Instructor Management
- Instructor profile management
- Assign instructors to classes
- View instructor-wise class schedules

### 💳 Membership & Subscription
- Membership plan management
- Automatic subscription creation after membership purchase
- Subscription expiration based on plan duration
- Active & expired subscription tracking

### ⭐ Feedback System
- Members can submit feedback for classes
- Class-wise feedback listing
- Admin moderation capability

### 📘 API Documentation
- Swagger UI (OpenAPI)
- Interactive API testing
- Clear request & response schemas

---

## 🛠️ Tech Stack

| Technology | Purpose |
|----------|--------|
| Python | Backend programming |
| Django | Web framework |
| Django REST Framework | REST API development |
| SimpleJWT | JWT authentication |
| Djoser | User management |
| PostgreSQL / SQLite | Database |
| drf-yasg | Swagger documentation |

---

## 📂 Project Structure

gym-management-api/
│
├── accounts/ # Authentication & users
├── classes/ # Fitness classes & bookings
├── memberships/ # Memberships & subscriptions
├── instructors/ # Instructor management
├── feedbacks/ # Feedback system
├── core/ # Shared utilities
│
├── manage.py
├── requirements.txt
└── README.md


---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/gym-management-api.git

cd gym-management-api

2. Create Virtual Environment

python -m venv venv

source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Environment Configuration
Create a .env file in the root directory:

SECRET_KEY=your_secret_key

DEBUG=True

DATABASE_URL=your_database_url

5. Apply Migrations

python manage.py migrate

6. Create Superuser

python manage.py createsuperuser

7. Run Development Server
python manage.py runserver

🔑 Authentication Usage


Include JWT access token in request headers:

Authorization: Bearer <access_token>
Refresh token endpoint:

POST /api/auth/jwt/refresh/
📖 API Documentation
After running the server, access:

Swagger UI
http://127.0.0.1:8000/swagger/
ReDoc
http://127.0.0.1:8000/redoc/
🧪 Sample API Endpoint


👨‍💻 Author
Mubtasim Ahsan Taha


