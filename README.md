# Inkwell - A Full-Stack Blogging Platform

Inkwell is a responsive and feature-rich full-stack blogging platform built using **Python, Django, and PostgreSQL**. It provides a secure environment where users can create, manage, and interact with blog content through an authenticated system.

The platform follows Django's MVT architecture and implements relational database design to efficiently manage users, profiles, and blog posts.

---

## 🚀 Live Demo & Repository

- **Live Link:** https://www.inkwell.pro.bd
- **GitHub Repository:** https://github.com/atonu-a/inkwell

---

## ✨ Features

### 🔐 User Authentication
- Secure user registration, login, and logout functionality.
- User-specific access control for managing personal content.
- Protected routes using Django authentication system.

### 📝 Blog Management (CRUD)
- Create, read, update, and delete blog posts.
- Users can manage only their own articles.
- Dynamic blog listing and detailed post views.

### 🔗 Relational Data Management
- Efficient relationship handling between:
  - Users
  - User profiles
  - Blog posts
- Structured database design using Django ORM.

### 🎨 Responsive User Interface
- Clean and responsive design using Bootstrap 5.
- Optimized layout for:
  - Desktop
  - Tablet
  - Mobile devices

### ⚡ Additional Functionality
- Slug-based URLs for blog posts.
- Pagination for handling multiple posts.
- Image support for blog content.
- Dynamic user profile management.

---

## 🛠️ Tech Stack

### Backend
- Python
- Django

### Database
- PostgreSQL
- Supabase (Database Hosting)

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Deployment
- Vercel

---


## 💻 Local Setup Instructions

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/atonu-a/inkwell.git

cd inkwell
```

---

### 2. Create a Virtual Environment
```bash
python -m venv venv

Activate the virtual environment:

inkwell



venv\Scripts\activate

Linux/macOS

source venv/bin/activate

```
---

### 3. Install Dependencies
```bash
pip install -r requirements.txt

```
---

### 4. Configure Environment Variables
```bash
Create a .env file in the project root directory:

SECRET_KEY=your_secret_key

DEBUG=True

DATABASE_URL=your_database_url

Update the values according to your local setup.
```

---

#### 5. Apply Database Migrations
```bash
python manage.py makemigrations

python manage.py migrate
```

---

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

---

### 7. Run Development Server
```bash
python manage.py runserver
```
Open your browser and visit:

http://127.0.0.1:8000/


---

📸 Screenshots

(Add screenshots of the homepage, blog details, profile page, and dashboard here)


---

🔒 Security

Django authentication system for user management.

CSRF protection enabled.

User-based permission handling for blog operations.

Environment variables used for sensitive configuration.



---

🚧 Future Improvements

Add REST API using Django REST Framework.

Implement comments and likes system improvements.

Add categories and tags.

Improve content recommendation system.

Add rich text editor for blog writing.



---

👨‍💻 Author

Atonu Roy Chowdhury

GitHub: https://github.com/atonu-a

Portfolio: https://atonu-roy-chowdhury.pro.bd



---
