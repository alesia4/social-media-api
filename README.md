# Social Media API

Built as a backend portfolio project for internship applications.

A RESTful social media backend built with **FastAPI** and **PostgreSQL**, featuring JWT authentication, user interactions, and a personalized feed system.

This project demonstrates backend architecture, authentication, relational data modeling, and clean API design.

---

## 🚀 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Pydantic
- Uvicorn

---

## ✨ Features

### 🔐 Authentication
- User registration
- Secure login
- Password hashing
- JWT access tokens
- Token validation & protected routes

### 👤 Users
- Retrieve user profiles
- Follow / Unfollow users
- Followers & following system

### 📝 Posts
- Create posts
- Read posts
- User-specific posts
- Delete posts

### 💬 Comments
- Add comments to posts
- Retrieve post comments
- Delete comments

### 📰 Feed
- Personalized feed
- Shows posts from followed users
- Ordered by creation date

---

## 📂 Project Structure

```
app/
 ├── auth/
 ├── users/
 ├── posts/
 ├── comments/
 ├── social/
 ├── feed/
 ├── database/
 └── main.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/social-media-api.git
cd social-media-api
```

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Create a `.env` file in the root folder and copy from `.env.example`.

Example:

```
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=social_media

JWT_SECRET=your_super_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=30
```

---

## ▶️ Run the application

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## 🗄 Database

- PostgreSQL required
- Tables are automatically created at startup
- Uses SQLAlchemy ORM

---

## 🔐 Authentication Flow

1. Register user
2. Login to receive JWT access token
3. Include token in Authorization header:

```
Authorization: Bearer <your_token>
```

---

## 📎 Why This Project?

This project demonstrates:

- Clean backend architecture
- RESTful API design
- Secure authentication practices
- Relational database modeling
- Modular FastAPI structure


