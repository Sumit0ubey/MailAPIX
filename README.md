
# 📧 MailAPIX

MailAPIX is a robust RESTful backend API built using **FastAPI**, **PostgreSQL**, and **smtplib** to facilitate secure, scalable, and customizable email delivery. It supports user management, secure tokens, and email template-based communication.

---

## 🗂️ Project Structure

```
MailAPIXAPI/
├── Controller/            # Business logic (email sending, validations)
├── Routers/               # FastAPI route definitions
├── database.py            # DB connection and session config
├── main.py                # FastAPI app entry point
├── models.py              # SQLAlchemy models
├── schema.py              # Pydantic schemas
├── utils.py               # Token gen, email formatting, helper functions
└── .env                   # Environment variables
```

---

## 🚀 Features

- ✅ User registration with token delivery
- 📧 Email sending with multiple templates (via SMTP)
- 🔒 Token-based security & password protection
- ⚡ Async request handling
- 📚 Clean project structure (Controller, Routers, Models, Utils)
- 📨 System default vs User email-based delivery

---

## 🔧 Installation

### Requirements

- Python 3.8+
- PostgreSQL
- pip

### Setup

```bash
git clone https://github.com/Sumit0ubey/MailAPIX.git
cd MailAPIX

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### .env Example

```
DATABASE_URL=postgresql://user:password@localhost/dbname
DEFAULT_EMAIL=default@yourdomain.com
DEFAULT_PASSKEY=yourpassword
SMTP_SERVER=smtp.yourdomain.com
SMTP_PORT=587
```

---

## ▶️ Run Server

```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

---

## 📘 API ROUTES

### 🔹 `/` Root
`GET /`  
Returns API metadata: name, description, available routes, IDE used, and duration of development.

---

## 👤 `/users` Route

All `/users` endpoints manage registration, upgrades, tokens, and securing the account.

### `POST /users`
Creates a user.  
**Body:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com"
}
```
**Behavior:** Adds user to DB, sends email with token.

---

### `GET /users/info/{id}`
**Requires Header:** `token: <token>`  
Returns: Full name, email, token, isPaidUser, numberOfEmailsSent, createdAt

---

### `GET /users/upgrade`
**Requires Header:** `token: <token>`  
Sends an email with available subscription plans.

---

### `POST /users/newToken/{id}`
**Requires Header:** `token: <token>`, id, (optional password)  
Sends a new token to the user's email after verification.

---

### `PUT /users/secureAccount/{id}`
**Requires:** id, email, setPassword, confirmPassword, token  
**Returns:** Success message

---

## ✉️ `/email` Routes

These routes send emails using different credentials and templates.

---

### `POST /email`
Sends email using the **user’s email** and **passKey**.

**Fields:**
```json
Requires Header: token: <token>
{
  "title": "Hello",
  "content": "Welcome!",
  "sendTo": "someone@example.com",
  "passKey": "user_email_password",
}
query_parameter = template_id=1&company_name=YourCo&company_link=https:/yourco.com&email_title=Notification (optional)
```

---

### `POST /email/default/`
Same fields, **except no passKey**. Uses API’s default email configured.

---

## 🎨 Templates (`template_id`)

| ID  | Name     | Description                                                 |
|-----|----------|-------------------------------------------------------------|
| 0   | Simple   | No formatting, plain text                                   |
| 1   | Cool     | Header, body, footer layout                                 |
| 2   | Amazing  | Stylized layout with modern UI                              |
| 3   | Custom   | Full customization + brand fields like logo, footer, etc.   |

**Supported Optional Fields:**
- `company_name`
- `company_link`
- `email_title`

These enhance professional look and personalization in templates `1`, `2`, and `3`.

---

## 🧩 Code Overview

| File/Folder       | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| `main.py`         | App entry point, includes routers                                       |
| `database.py`     | DB session creation                                                     |
| `models.py`       | SQLAlchemy models (User, etc.)                                          |
| `schema.py`       | Pydantic models for validation                                          |
| `utils.py`        | Token creation, email formatting utilities                              |
| `Routers/`        | API route logic for `/users`, `/email`                                  |
| `Controller/`     | Functional logic (sending emails, verifying users, formatting)          |

---

## 🧪 Testing

You can use tools like:
- Swagger UI (`/docs`)
- Postman collection *(optional)*
- Curl scripts

---

## ✍️ Author

Made with ❤️ by [Sumit Dubey](https://github.com/Sumit0ubey)

---

## ⚠️ Usage & License Notice

This project is open-source for educational and reference purposes. It is hosted at:
🔗 [MailAPIX](https://api.mailapix.tech/docs)

You **may view, learn from, and fork this repository**, but **you are not permitted to republish, resell, or claim it as your own** under any circumstances.

All original work © 2025 Sumit Dubey. All rights reserved.

For collaboration or licensing inquiries, please contact the author directly through GitHub.

---
