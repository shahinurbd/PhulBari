# 🌸PhulBari - Flower Marketplace API

A RESTful API for an online flower-selling platform built with **Django Rest Framework**. This backend allows users to browse and purchase flowers, while admins manage inventory and orders through a dedicated admin dashboard.

---

## 🛆 Features

* User registration and authentication using **Djoser** and **JWT**
* Flower catalog browsing and purchase via a `Buy Now` endpoint
* Role-based access control:

  * **Users** can view and buy flowers
  * **Admins** can create, update, and delete flowers and manage all orders
* Categorized flower listings
* Swagger/OpenAPI documentation

---

## 🧱 Tech Stack

* Python 3.x
* Django
* Django Rest Framework (DRF)
* Djoser (authentication)
* Simple JWT (authentication tokens)
* drf-yasg (Swagger documentation)

---

## 🔐 Authentication

Authentication is handled via **JWT tokens** using **Djoser**. After registration, users can log in to receive access and refresh tokens for authenticated requests.

---

## 📁 API Endpoints Overview

| Method | Endpoint                | Description                                 | Auth Required | Admin Only |   |   |
| ------ | ----------------------- | ------------------------------------------- | ------------- | ---------- | - | - |
| GET    | `/api/flowers/`         | List all flowers                            | ✅             | ✅          |   |   |
| GET    | `/api/flowers/<id>/`    | Retrieve a specific flower                  | ✅             | ✅          |   |   |
| POST   | `/api/flower/<id>/buy/` | Buy a flower (Buy Now)                      | ✅             | ✅          |   |   |
| GET    | `/api/orders/`          | View user’s own orders                      | ✅             | ✅          |   |   |
| POST   | `/api/flowers/`         | Create a new flower                         | ❌             | ✅          |   |   |
| PUT    | `/api/flowers/<id>/`    | Update flower details                       | ❌             | ✅          |   |   |
| DELETE | `/api/flowers/<id>/`    | Delete a flower                             | ❌             | ✅          |   |   |
| GET    | `/api/admin-dashboard/` | Admin dashboard for managing orders/flowers | ❌             | ✅          |   |   |

---

## 📂 Models

* **User** – Registered users with JWT auth
* **Flower** – Flower items with fields like name, price, description, image, category, etc.
* **Category** – Categories for organizing flowers
* **Order** – Stores flower purchase records by users

---

## 📄 API Documentation

Interactive API docs available at:

```
http://localhost:8000/swagger/
```

Provided by **drf-yasg** (Swagger/OpenAPI 2.0).

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/shahinurbd/phulbari.git
cd phulbari
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations and run server

```bash
python manage.py migrate
python manage.py runserver
```

### 5. Create superuser (for admin access)

```bash
python manage.py createsuperuser
```

---

## 🔧 Configuration Notes

* Make sure `rest_framework`, `djoser`, and `drf_yasg` are added to `INSTALLED_APPS`
* JWT settings and URLs must be properly configured in `settings.py`

---

## ✅ TODO / Future Improvements

* Payment integration (Stripe, PayPal, etc.)
* Flower reviews and ratings
* Wishlist and cart functionality
* Email notifications for orders

---

## 📃 License

This project is licensed under the MIT License.

---

## 🙋‍♂️ Author

Developed by \[Md Shahinur Islam]
Feel free to contribute or report issues.
