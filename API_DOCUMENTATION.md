# 📚 MailApix API - Complete API Documentation

> **Full Reference Guide for MailApix Email Service API**
>
> Base URL: `https://api.mailapix.tech`  <br />
> API Version: `2.05.9`  
> Documentation Endpoint: `/documentation`

---

## 📋 Table of Contents

1. [🔐 Authentication](#-authentication)
2. [📦 Request/Response Format](#-requestresponse-format)
3. [👥 User Endpoints](#-user-endpoints)
4. [📧 Email Endpoints](#-email-endpoints)
5. [🎨 Templates](#-templates)
6. [⚠️ Error Handling](#-error-handling)
7. [📊 Rate Limits & Quotas](#-rate-limits--quotas)
8. [💡 Examples](#-examples)

---

## 🔐 Authentication

All protected endpoints require authentication via **API Token** passed in the request header.

### 🎫 Token Header
```
token: your-api-token-here
```

**Token Format**: UUID-based unique identifier  
**Validity**: Until revoked or manually reset  
**Obtaining Token**: Provided during user registration via email

### 🔒 Security Notes
- 🔐 Tokens are **confidential** - never share them publicly
- 🚨 If compromised, immediately generate a new token using the revoke key flow
- 🔤 Tokens are case-sensitive

---

## 📦 Request/Response Format

### 📋 Content-Type
All requests and responses use **JSON** format.

```
Content-Type: application/json
```

### 📊 Standard Response Structure

**✅ Success Response (2xx)**
```json
{
  "message": "Operation completed successfully",
  "data": {}
}
```

**❌ Error Response (4xx, 5xx)**
```json
{
  "message": "Error description",
  "detail": "Additional error information"
}
```

---

## 👥 User Endpoints

### 1️⃣ Register New User
**Register a new user and receive API credentials**

**Endpoint**: `POST /users/`

**📝 Headers**

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| Content-Type | string | Yes | `application/json` |

**📥 Request Body**
```json
{
  "fullName": "John Doe",
  "email": "john@example.com"
}
```

**✔️ Request Schema**

| Field | Type | Required | Validation | Description |
|-------|------|----------|-----------|-------------|
| fullName | string | Yes | 1-100 chars | User's full name |
| email | string | Yes | Valid email | User's email address |

**📋 Response Codes**

| Code | Status | Response |
|------|--------|----------|
| 201 | Created | `{"message": "We have send your credential to your email. please check it.."}` |
| 404 | Not Found | `{"message": "User cannot be created or email already exists"}` |
| 500 | Server Error | `{"message": "Failed to send email"}` |

**🔗 cURL Example**
```bash
curl -X POST "https://api.mailapix.com/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "John Doe",
    "email": "john@example.com"
  }'
```

**✅ Response Example (201)**
```json
{
  "message": "We have send your credential to your email. please check it.."
}
```

---

### 2️⃣ Get User Information
**Retrieve authenticated user's account details**

**Endpoint**: `GET /users/info`

**📝 Headers**

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| user_id | string | Yes | User's ID |

**📋 Response Codes**

| Code | Status | Response |
|------|--------|----------|
| 302 | Found | User information object (see schema below) |
| 404 | Not Found | `{"message": "User does not exists"}` |

**📤 Response Schema**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "fullName": "John Doe",
  "email": "john@example.com",
  "isPaidUser": false,
  "numberOfEmailSend": 5,
  "numberOfEmailCanSend": 20,
  "numberOfDefaultEmailSend": 2,
  "numberOfDefaultEmailCanSend": 5,
  "createdAt": "2024-01-15T10:30:00Z"
}
```

**🔗 cURL Example**
```bash
curl -X GET "https://api.mailapix.com/users/info" \
  -H "user_id: your-user-id"
```

---

### 3️⃣ Upgrade to Paid Plan
**Send upgrade plan information email to user**

**Endpoint**: `GET /users/upgrade`

**📝 Headers**

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| user_id | string | Yes | User's ID |

**📋 Response Codes**

| Code | Status | Response |
|------|--------|----------|
| 202 | Accepted | `{"Message": "We have send you an email please check it.."}` |
| 404 | Not Found | `{"message": "User does not exists"}` |
| 500 | Server Error | `{"message": "Failed to send email"}` |

**🔗 cURL Example**
```bash
curl -X GET "https://api.mailapix.com/users/upgrade" \
  -H "user_id: your-user-id"
```

---

### 4️⃣ Generate Revoke Key
**Generate a temporary revoke key to reset your API token (valid for 4 minutes by default)**

**Endpoint**: `POST /users/revokeKey/{id}`

**📍 Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | User's ID |

**📝 Headers**

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| Content-Type | string | Yes | `application/json` |

**📥 Request Body**
```json
{
  "password": ""
}
```

**✔️ Request Schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| password | string | No | Account password (if set) |

**📋 Response Codes**

| Code | Status | Response |
|------|--------|----------|
| 202 | Accepted | Revoke key email sent with task ID |
| 401 | Unauthorized | `{"message": "Unauthorized Access"}` |
| 500 | Server Error | `{"message": "Failed to send revoke email"}` |
| 503 | Service Unavailable | `{"message": "Revoke email sent, but auto-expiry scheduling failed..."}` |

**📤 Response Schema (202)**
```json
{
  "message": "Revoke key email sent. The key will auto-expire in 4 minutes.",
  "invalidateTaskId": "task-id-for-tracking"
}
```

**🔗 cURL Example**
```bash
curl -X POST "https://api.mailapix.com/users/revokeKey/your-user-id" \
  -H "Content-Type: application/json" \
  -d '{
    "password": ""
  }'
```

---

### 5️⃣ Generate New Token
**Generate a new API token using the revoke key**

**Endpoint**: `POST /users/newToken/{id}`

**📍 Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | User's ID |

**📝 Headers**

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| key | string | Yes | Revoke key from previous step |
| Content-Type | string | Yes | `application/json` |

**📥 Request Body**
```json
{
  "password": ""
}
```

**✔️ Request Schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| password | string | No | Account password (if set) |

**📋 Response Codes**

| Code | Status | Response |
|------|--------|----------|
| 202 | Accepted | `{"Message": "We have send you an email with your new token please check it.."}` |
| 401 | Unauthorized | `{"message": "Unauthorized Access"}` |
| 500 | Server Error | `{"message": "Failed to send email"}` |

**🔗 cURL Example**
```bash
curl -X POST "https://api.mailapix.com/users/newToken/your-user-id" \
  -H "key: your-revoke-key" \
  -H "Content-Type: application/json" \
  -d '{
    "password": ""
  }'
```

---

### 6️⃣ Secure Account with Password
**Set or update your account password for additional security**

**Endpoint**: `PUT /users/secureAccount/{id}`

**📍 Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | User's ID |

**📝 Headers**

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| key | string | Yes | Revoke key |
| Content-Type | string | Yes | `application/json` |

**📥 Request Body**
```json
{
  "email": "john@example.com",
  "oldPassword": "",
  "setPassword": "newPassword123",
  "confirmPassword": "newPassword123"
}
```

**✔️ Request Schema**

| Field | Type | Required | Validation | Description |
|-------|------|----------|-----------|-------------|
| email | string | Yes | Valid email | User's email |
| oldPassword | string | No | - | Old password (if exists) |
| setPassword | string | Yes | Min 8 chars | New password |
| confirmPassword | string | Yes | Must match setPassword | Confirmation of new password |

**📋 Response Codes**

| Code | Status | Response |
|------|--------|----------|
| 202 | Accepted | `{"message": "Now your Account is Secure \| Password is set"}` |
| 401 | Unauthorized | `{"message": "Unauthorized Access"}` |
| 409 | Conflict | `{"message": "Password does not match"}` |
| 500 | Server Error | `{"message": "Failed to update password"}` |

**🔗 cURL Example**
```bash
curl -X PUT "https://api.mailapix.com/users/secureAccount/your-user-id" \
  -H "key: your-revoke-key" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "oldPassword": "",
    "setPassword": "newPassword123",
    "confirmPassword": "newPassword123"
  }'
```

---

## 📧 Email Endpoints

### 1️⃣ Send Email with User SMTP Credentials
**Send an email using the user's own SMTP credentials**

**Endpoint**: `POST /email/`

**📝 Headers**

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| token | string | Yes | User's API token |
| email_title | string | No | Subject line (fallback to title if not provided) |
| template_id | integer | No | Email template ID (0-4, default: 0) |
| company_name | string | No | Company name for template |
| company_link | string | No | Company website link |
| Content-Type | string | Yes | `application/json` |

**📋 Query Parameters**

| Parameter | Type | Default | Allowed | Description |
|-----------|------|---------|---------|-------------|
| template_id | integer | 0 | 0-4 | Email template ID |

**📥 Request Body**
```json
{
  "title": "Welcome",
  "content": "This is the email content",
  "sendTo": "recipient@example.com",
  "passKey": "your-smtp-app-password",
  "customHtml": null
}
```

**✔️ Request Schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Email title/heading |
| content | string | Yes | Email body content |
| sendTo | string or array | Yes | Recipient email or array of emails |
| passKey | string | Yes | SMTP app password |
| customHtml | string | No | Custom HTML (only if template_id = 4) |

**📋 Response Codes**

| Code | Status | Response |
|------|--------|----------|
| 202 | Accepted | `{"Message": "Email send to [email] with title [title] using [service]"}` |
| 401 | Unauthorized | `{"message": "Unauthorized Access"}` |
| 403 | Forbidden | `{"message": "Maximum quota exceeded"}` |
| 500 | Server Error | `{"message": "Failed to send email... Check your credential and try again."}` |

**🔗 cURL Example**
```bash
curl -X POST "https://api.mailapix.com/email/?template_id=1" \
  -H "token: your-api-token" \
  -H "email_title: Welcome to Our Service" \
  -H "company_name: Acme Corp" \
  -H "company_link: https://acme.com" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Welcome",
    "content": "Hello! Thanks for signing up.",
    "sendTo": "recipient@example.com",
    "passKey": "your-smtp-app-password"
  }'
```

---

### 2️⃣ Send Email with System SMTP Credentials
**Send an email using the system's default SMTP credentials (uses your free quota)**

**Endpoint**: `POST /email/default`

**📝 Headers**

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| token | string | Yes | User's API token |
| email_title | string | No | Subject line (fallback to title if not provided) |
| template_id | integer | No | Email template ID (0-4, default: 0) |
| company_name | string | No | Company name for template |
| company_link | string | No | Company website link |
| Content-Type | string | Yes | `application/json` |

**📋 Query Parameters**

| Parameter | Type | Default | Allowed | Description |
|-----------|------|---------|---------|-------------|
| template_id | integer | 0 | 0-4 | Email template ID |

**📥 Request Body**
```json
{
  "title": "Welcome",
  "content": "This is the email content",
  "sendTo": "recipient@example.com",
  "customHtml": null
}
```

**✔️ Request Schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Email title/heading |
| content | string | Yes | Email body content |
| sendTo | string or array | Yes | Recipient email or array of emails |
| customHtml | string | No | Custom HTML (only if template_id = 4) |

**📋 Response Codes**

| Code | Status | Response |
|------|--------|----------|
| 202 | Accepted | `{"Message": "Email send to [email] with title [title] using Gmail service"}` |
| 401 | Unauthorized | `{"message": "Unauthorized Access"}` |
| 403 | Forbidden | `{"message": "Maximum quota exceeded"}` |
| 500 | Server Error | `{"message": "Failed to send email... Check your credential and try again."}` |

**📤 Response Schema (202)**
```json
{
  "Message": "Email send to recipient@example.com with title Welcome using Gmail service"
}
```

**🔗 cURL Example**
```bash
curl -X POST "https://api.mailapix.com/email/default?template_id=1" \
  -H "token: your-api-token" \
  -H "email_title: Welcome to Our Service" \
  -H "company_name: Acme Corp" \
  -H "company_link: https://acme.com" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Welcome",
    "content": "Hello! Thanks for signing up.",
    "sendTo": "recipient@example.com"
  }'
```

---

## 🎨 Templates

MailApix provides pre-built email templates or allows custom HTML. Templates are identified by ID (0-4).

### 🆔 Template IDs

| ID | Name | Type | Use Case | Requires Custom HTML |
|----|------|------|----------|----------------------|
| 0 | Plain Text | Text-only | Simple transactional emails | No |
| 1 | Professional | HTML | Business communications | No |
| 2 | Modern | HTML | Product notifications | No |
| 3 | Elegant | HTML | Marketing emails | No |
| 4 | Custom | Custom HTML | Full control over design | Yes |

### 📝 Template Parameters

Templates support dynamic variables that can be customized:

```json
{
  "title": "Email Heading",
  "content": "Body content",
  "company_name": "Your Company",
  "company_link": "https://yourcompany.com"
}
```

### 🎯 Custom HTML Template (ID: 4)

When using template ID 4, provide your own HTML:

```json
{
  "title": "Welcome",
  "content": "Email body text",
  "sendTo": "recipient@example.com",
  "customHtml": "<html><body><h1>Hello {{name}}</h1><p>Welcome!</p></body></html>"
}
```

**🔤 Supported HTML Variables**:
- `{{title}}` - Email title/subject
- `{{content}}` - Email body
- `{{company_name}}` - Company name
- `{{company_link}}` - Company link

---

## ⚠️ Error Handling

### 🔴 Common Error Codes

| Code | Scenario | Resolution |
|------|----------|-----------|
| 400 | Bad Request | Check request body schema and format |
| 401 | Unauthorized | Verify API token is correct and active |
| 403 | Forbidden | Check quota limits or access permissions |
| 404 | Not Found | Resource doesn't exist or user not found |
| 409 | Conflict | Data mismatch (e.g., password confirmation) |
| 500 | Server Error | Check SMTP credentials or contact support |
| 503 | Service Unavailable | Queue service issue, try again later |

### 📄 Error Response Format

```json
{
  "message": "Brief error description",
  "detail": "Additional context (if available)"
}
```

### ⏳ Handling Expired Tokens

**❌ Error Response**:
```json
{
  "message": "Unauthorized Access"
}
```

**🛠️ Resolution**:
1. Generate a revoke key: `POST /users/revokeKey/{id}`
2. Generate new token: `POST /users/newToken/{id}`
3. Retry the request with new token

---

## 📊 Rate Limits & Quotas

### 👤 User Quotas

| Tier | Free | Premium |
|------|------|---------|
| **Monthly Email Limit** | 20 | 1000+ |
| **Default (System) Emails** | 5/month | Included |
| **Custom SMTP Emails** | 15/month | Included |
| **Token Expiry** | Never | Never |
| **Revoke Key TTL** | 4 minutes | 4 minutes |

### ✅ Quota Checking

Each endpoint checks quotas before sending:

- `numberOfEmailSend` vs `numberOfEmailCanSend` for custom SMTP
- `defaultEmailSend` vs `defaultEmailCanSend` for system SMTP

**⛔ Response on Quota Exceeded**:
```json
{
  "message": "Maximum quota exceeded",
  "status": 403
}
```

### 🚀 Upgrading Quota

Users can upgrade to premium plans to increase their quota:
```bash
GET /users/upgrade
```

---

## 💡 Examples

### 🧭 Complete Workflow Example

#### 1️⃣ Step 1: Register User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "John Doe",
    "email": "john@example.com"
  }'
```

📩 Response:
```json
{
  "message": "We have send your credential to your email. please check it.."
}
```

#### 2️⃣ Step 2: Check Email for API Token
(Check john@example.com for registration confirmation containing the API token)

#### 3️⃣ Step 3: Send Email with System SMTP
```bash
curl -X POST "http://localhost:8000/email/default?template_id=1" \
  -H "token: <received-api-token>" \
  -H "email_title: Test Email" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Subject",
    "content": "This is a test email",
    "sendTo": "recipient@example.com"
  }'
```

✅ Response:
```json
{
  "Message": "Email send to recipient@example.com with title Test Subject using Gmail service"
}
```

#### 4️⃣ Step 4: Get User Info
```bash
curl -X GET "http://localhost:8000/users/info" \
  -H "user_id: <your-user-id>"
```

📋 Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "fullName": "John Doe",
  "email": "john@example.com",
  "isPaidUser": false,
  "numberOfEmailSend": 0,
  "numberOfEmailCanSend": 20,
  "numberOfDefaultEmailSend": 1,
  "numberOfDefaultEmailCanSend": 5,
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### 👥 Multiple Recipients Example

Send email to multiple recipients:

```bash
curl -X POST "http://localhost:8000/email/?template_id=1" \
  -H "token: your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Newsletter",
    "content": "This month news...",
    "sendTo": ["user1@example.com", "user2@example.com", "user3@example.com"],
    "passKey": "your-smtp-app-password"
  }'
```

### 🎨 Custom HTML Email Example

```bash
curl -X POST "http://localhost:8000/email/default?template_id=4" \
  -H "token: your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Custom HTML Email",
    "content": "Fallback text content",
    "sendTo": "recipient@example.com",
    "customHtml": "<html><body style=\"font-family: Arial;\"><h1>Welcome!</h1><p>This is a custom HTML email</p></body></html>"
  }'
```

---

## 🔗 Additional Resources

- 📖 **Interactive Documentation**: `/documentation` (Swagger UI)
- 🐙 **GitHub Repository**: [MailApix API](https://github.com/Sumit0ubey/MailAPIX)
- 💬 **Support Email**: sumitdubey810@outlook.com
- 🔢 **Version**: 2.05.9

---

## 📝 Notes

- ⏰ All timestamps are in ISO 8601 format (UTC)
- ✉️ Email addresses must be valid according to RFC 5322
- 📋 Requests must include appropriate Content-Type headers
- 🚦 Rate limiting may apply to high-volume requests
- ⚡ The API uses asynchronous processing for reliability

---

**Last Updated**: March 29, 2026  
**Created by**: Sumit Dubey  
**License**: MIT

