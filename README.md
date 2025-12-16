Urbano Cart 🛒

Urbano Cart is a **full‑stack Django-based e‑commerce web application** built to demonstrate real‑world backend development concepts such as authentication, cart management, order processing, and secure payment integration.

This project is designed as a **portfolio project for recruiters**, showcasing clean Django architecture, secure coding practices, and practical business logic.

---

## 🚀 Features

### 👤 User Features

* User signup, login, and logout (Django Authentication)
* Browse products by categories
* Product search, filter, and sorting
* Add to cart (supports size-based products)
* Cart management (update quantity, remove items)
* Checkout flow with address and delivery options
* Order history and order cancellation

### 🛍️ E‑Commerce Functionality

* Category-based product listing
* Best sellers, new arrivals, featured products
* Discount & sale price handling
* Session-based cart for guest users
* Database-backed cart for logged-in users

### 💳 Payments

* Razorpay payment gateway integration
* Cash on Delivery (COD) option
* Demo user checkout flow (no real payment required)

### 🛠️ Admin Features

* Django Admin dashboard
* Product & category management
* Multiple product images
* Order & order item management
* Contact messages management

---

## 🧑‍💻 Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, Django Templates
* **Database:** SQLite (development)
* **Payments:** Razorpay API
* **Authentication:** Django Auth System
* **Version Control:** Git & GitHub

---

## 🔐 Security Practices

* Sensitive data managed using **environment variables (.env)**
* `.env` excluded from GitHub using `.gitignore`
* No API keys or secrets committed to the repository

---

## 📂 Project Structure

```
urbano-cart/
│
├── urbano/              # Main Django app
│├── urbano_cart/        # Project settings
│├── templates/          # HTML templates
│├── static/             # Static assets
│├── manage.py
│├── .gitignore
```

---

## ⚙️ Local Setup Instructions

1. Clone the repository

   ```bash
   git clone https://github.com/vineela0206/urbano-cart.git
   cd urbano-cart
   ```

2. Create and activate virtual environment

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file (not included in repo)

   ```env
   DJANGO_SECRET_KEY=your-secret-key
   RAZORPAY_KEY_ID=your-key-id
   RAZORPAY_KEY_SECRET=your-key-secret
   EMAIL_HOST_USER=your-email
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. Run migrations

   ```bash
   python manage.py migrate
   ```

6. Create superuser

   ```bash
   python manage.py createsuperuser
   ```

7. Run the server

   ```bash
   python manage.py runserver
   ```

---

## 👤 Demo User

To test checkout without real payment:

```
Username: demo@example.com
Password: Demo@123
```

Demo users can place orders without triggering Razorpay payment.

---

## 📌 What This Project Demonstrates

* Practical Django MVT architecture
* Secure handling of secrets and credentials
* Real‑world e‑commerce workflows
* Clean Git & GitHub usage
* Debugging, migrations, and refactoring skills

---

## 🔮 Future Improvements

* Deployment (AWS / Render / Railway)
* REST API with Django REST Framework
* Frontend enhancement (React / Vue)
* Payment webhooks
* PostgreSQL database

---

## 👨‍🎓 Author

**Vineela**

Aspiring Backend / Python Developer / Software Engineer 

---

⭐ *If you are a recruiter, thank you for reviewing this project!*
