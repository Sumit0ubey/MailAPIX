# ðŸ“§ MailApix API

> Enterprise-grade async email delivery API with token-based access, quota controls, and template-driven messaging.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Async-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Celery-dc382d?style=for-the-badge&logo=redis&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Status:** ![Build](https://img.shields.io/badge/Build-PASSING-brightgreen?style=flat-square)
![Production](https://img.shields.io/badge/Production-Ready-brightgreen?style=flat-square)
![Documentation](https://img.shields.io/badge/Documentation-Complete-brightgreen?style=flat-square)
![Version](https://img.shields.io/badge/Version-2.05.9-blue?style=flat-square)

</div>

---

## ðŸ“‘ Table of Contents

- [ðŸŽ¯ Overview](#-overview)
- [ðŸš€ Quick Start](#-quick-start)
- [ðŸ“š Documentation](#-documentation)
- [âœ¨ Features](#-features)
- [ðŸ—ï¸ System Design](#-system-design)
- [ðŸ—ï¸ Architecture](#-architecture)
- [ðŸ“Š Project Structure](#-project-structure)
- [ðŸ”Œ API Endpoints](#-api-endpoints)
- [ðŸ’¾ Technology Stack](#-technology-stack)
- [ðŸŽ¨ Templates](#-templates)
- [ðŸš¢ Deployment](#-deployment)
- [ðŸ›¡ï¸ Security](#-security)
- [ðŸ“ License](#-license)

---

## ðŸŽ¯ Overview

**MailApix API** is a production-ready async email delivery backend built with FastAPI and PostgreSQL. It provides secure token-based access for users to send emails using their own SMTP credentials or the system's default service with quota-based protection.

**Project Status:** âœ… **COMPLETE AND PRODUCTION READY**

- **Build Status:** âœ… SUCCESS
- **Features:** âœ… FULLY IMPLEMENTED (8 endpoints)
- **Documentation:** âœ… COMPLETE (API + Guides)
- **Deployment Ready:** âœ… YES (Docker + Gunicorn)

---

## ðŸš€ Quick Start

### ðŸ§° Prerequisites
- ðŸ Python 3.10+
- ðŸ—„ï¸ PostgreSQL 12+
- ðŸ”´ Redis
- ðŸ§¬ Git

### âš™ï¸ Installation

```bash
# Clone the repository
git clone https://github.com/Sumit0ubey/MailAPIX
cd MailApixAPI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Create .env file with database and email credentials
cp .env.example .env

# Run the application
uvicorn MailApixAPI.main:app --reload

# In another terminal, run Celery
celery -A MailApixAPI.celery_app:celery_app worker --loglevel=info
```

The API will be available at `http://localhost:8000`  
Documentation: `http://localhost:8000/documentation`

---

## ðŸ“š Documentation

### ðŸ“– **Complete API Documentation**
Comprehensive endpoint documentation with request/response examples, validation rules, and error scenarios.

**ðŸ‘‰ [View API Documentation](./API_DOCUMENTATION.md)**

### ðŸ“‹ **This README**
Project overview and quick reference guide.

---

## âœ¨ Features

<table>
<tr>
<td width="50%">

### ðŸ‘¥ User Management
- âœ… User registration with token delivery
- âœ… Token-based authentication
- âœ… Token refresh via revoke keys
- âœ… Account password protection

</td>
<td width="50%">

### ðŸ“§ Email Delivery
- âœ… Send with user SMTP credentials
- âœ… Send with system SMTP fallback
- âœ… Single or multi-recipient support
- âœ… Quota-based rate limiting

</td>
</tr>
<tr>
<td width="50%">

### ðŸŽ¨ Template System
- âœ… 5 email templates (0-4)
- âœ… Custom HTML support
- âœ… Dynamic variables
- âœ… Fallback text support

</td>
<td width="50%">

### ðŸ” Security
- âœ… Token-gated routes
- âœ… Password hardening
- âœ… Quota protection
- âœ… Email validation

</td>
</tr>
</table>

---

## ðŸ—ï¸ System Design

### ðŸ“ High-Level Architecture

```mermaid
graph TB
    Client["ðŸ‘¥ Client Layer<br/>(Web/Mobile/CLI Apps)"]
    
    subgraph API["ðŸš€ API Gateway Layer<br/>(FastAPI + CORS Middleware)"]
        UserRouter["User Router"]
        EmailRouter["Email Router"]
        StatusRouter["Status Routes"]
    end
    
    subgraph Core["âš™ï¸ Core Services Layer"]
        Services["Services<br/>â€¢ UserServices<br/>â€¢ EmailService"]
        Queue["Task Queue<br/>(Celery)"]
        DB["Database Service<br/>PostgreSQL<br/>Async ORM<br/>SQLAlchemy"]
    end
    
    Redis["ðŸ”´ Redis<br/>(Broker & Backend)"]
    
    subgraph Ext["ðŸŒ External Services"]
        SMTP["SMTP Service<br/>(Multi-Provider)"]
        Templates["Template Engine"]
        Logging["Logging System"]
    end
    
    EmailProviders["ðŸ“§ Email Providers<br/>(Gmail, Outlook, Yahoo, Zoho)"]
    
    Client -->|HTTP/REST| API
    API --> Services
    API --> Queue
    API --> DB
    Services --> Redis
    Queue --> Redis
    DB --> Redis
    Services --> SMTP
    Services --> Templates
    Services --> Logging
    SMTP --> EmailProviders
    
    style Client fill:#e1f5ff
    style API fill:#f3e5f5
    style Core fill:#e8f5e9
    style Ext fill:#fff3e0
    style EmailProviders fill:#ffebee
```

### ðŸ”„ Data Flow Diagram

#### ðŸ‘¤ User Registration Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Services
    participant DB as PostgreSQL
    participant Queue as Celery Queue

    Client->>API: POST /users/<br/>(fullName, email, password)
    API->>Services: Validate Input
    Services->>Services: Generate Tokens<br/>(API Token, Revoke)
    Services->>DB: Create User<br/>(Store in DB)
    DB-->>Services: User Created âœ“
    Services-->>API: User Object + Tokens
    API-->>Client: HTTP 201 Created<br/>(token, revokeToken)
    
    API->>Queue: Task: Send Registration Email<br/>(via Celery)
    Queue-->>Client: (Processing Async)
```

#### ðŸ“¨ Email Sending Flow (Async Processing)

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Queue as Redis Queue
    participant Worker as Celery Worker
    participant SMTP

    Client->>API: POST /email/
    API->>API: Validate Token
    API->>API: Check Quota
    API->>API: Store Request in DB
    API-->>Client: HTTP 202 Accepted<br/>(job_id)
    
    API->>Queue: Enqueue Task<br/>(via Redis)
    Queue->>Worker: Dequeue Task
    Worker->>SMTP: Connect to SMTP Server
    Worker->>Worker: Render Template
    Worker->>SMTP: Send Email
    SMTP-->>Worker: Success âœ“
    Worker-->>Queue: Result (Status)
```

#### ðŸ”‘ Token Refresh Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Services
    participant DB as PostgreSQL
    participant Queue as Celery Queue

    Client->>API: POST /users/newToken/{id}
    API->>Services: Verify User ID
    Services->>DB: Query User by ID
    DB-->>Services: User Info âœ“
    Services->>Services: Generate New Token
    Services->>DB: Update DB<br/>(Store New Token)
    DB-->>Services: Updated âœ“
    Services-->>API: New Token
    API-->>Client: HTTP 200 OK<br/>(newToken)
    
    Services->>Queue: Task: Revoke Old Token<br/>(Async)
    Queue-->>DB: Schedule Revoke
```

### ðŸ”€ Component Interaction Diagram

```mermaid
graph TB
    subgraph Router["ðŸŽ® FastAPI Router<br/>(Request Processing)"]
        UserR["User Router<br/>â€¢ register<br/>â€¢ getUser<br/>â€¢ newToken<br/>â€¢ revokeKey<br/>â€¢ secureAccount"]
        EmailR["Email Router<br/>â€¢ send<br/>â€¢ sendDefault"]
    end
    
    subgraph Services["âš™ï¸ Services Layer"]
        UserServ["UserServices<br/>â€¢ register()<br/>â€¢ getUser()<br/>â€¢ newToken()<br/>â€¢ revokeKey()<br/>â€¢ secureAccount()"]
        EmailServ["EmailService<br/>â€¢ validate_email()<br/>â€¢ send()<br/>â€¢ sendDefault()<br/>â€¢ renderTemplate()<br/>â€¢ getUserSMTP()"]
    end
    
    subgraph Data["ðŸ’¾ Data Access Layer"]
        ORM["SQLAlchemy ORM<br/>(Async Session)"]
        Model["User Model"]
    end
    
    subgraph DB["ðŸ—„ï¸ Database"]
        DBConn["PostgreSQL<br/>Primary Connection"]
        Table["Users Table<br/>â€¢ id<br/>â€¢ email<br/>â€¢ apiToken<br/>â€¢ quotas<br/>â€¢ createdAt"]
    end
    
    Queue["ðŸ“¦ Celery Queue<br/>(Redis)<br/>â€¢ revoke_token()<br/>â€¢ send_email()<br/>â€¢ notify_user()"]
    
    SMTP["ðŸ“§ SMTP Service<br/>(Multi-Provider)<br/>Gmail, Outlook,<br/>Yahoo, Zoho"]
    
    UserR -->|routes to| UserServ
    EmailR -->|routes to| EmailServ
    UserServ -->|uses| ORM
    EmailServ -->|uses| ORM
    ORM -->|maps| Model
    Model -->|queries| DBConn
    DBConn -->|accesses| Table
    UserServ -->|enqueues| Queue
    EmailServ -->|connects| SMTP
    Queue -->|processes async| EmailServ
    
    style Router fill:#f3e5f5
    style Services fill:#e8f5e9
    style Data fill:#e3f2fd
    style DB fill:#fff3e0
    style Queue fill:#fce4ec
    style SMTP fill:#f1f8e9
```

### ðŸ“Š Database Schema Diagram

```mermaid
erDiagram
    USERS ||--o{ EMAIL_SESSIONS : sends
    USERS ||--o{ TOKENS : has
    
    USERS {
        string id PK "UUID"
        string fullName "String, not null"
        string email UK "String, unique, not null"
        string password "String, hashed"
        string apiToken UK "String, unique, not null"
        string revokeToken UK "String, unique, nullable"
        boolean isPaidUser "Boolean, default false"
        int numberOfEmailSend "Integer, default 0"
        int numberOfEmailCanSend "Integer, default 20"
        int defaultEmailSend "Integer, default 0"
        int defaultEmailCanSend "Integer, default 5"
        timestamp createdAt "TIMESTAMP with timezone"
    }
    
    EMAIL_SESSIONS {
        string id PK "UUID"
        string user_id FK "References Users.id"
        string recipient "Email recipient"
        string subject "Email subject"
        text body "Email body/HTML"
        string status "pending, sent, failed"
        timestamp created_at "When email was sent"
    }
    
    TOKENS {
        string id PK "UUID"
        string user_id FK "References Users.id"
        string token_value "Token value"
        string token_type "api_token, revoke_token"
        timestamp expires_at "Token expiration"
        boolean is_active "Active status"
    }
```

### ðŸ” Authentication & Authorization Flow

```mermaid
flowchart TD
    Start["ðŸ” API REQUEST<br/>WITH TOKEN HEADER"] --> Extract["Extract Bearer Token<br/>from Headers"]
    Extract --> Query["Query User by Token<br/>in Database"]
    Query --> Check{Token<br/>Valid?}
    
    Check -->|YES| Load["Load User Context<br/>into Request"]
    Check -->|NO| Reject["âŒ Return 401<br/>Unauthorized"]
    
    Load --> CheckQuota{Check Quotas<br/>& Permissions}
    
    CheckQuota -->|OK| Proceed["âœ… Proceed with<br/>Request"]
    CheckQuota -->|DENIED| QuotaError["â›” Return 429<br/>Quota Limit Exceeded"]
    
    Proceed --> Success["Execute Handler"]
    Reject --> End1["End - Rejected"]
    QuotaError --> End2["End - Quota Error"]
    Success --> End3["End - Success"]
    
    style Start fill:#bbdefb
    style Proceed fill:#c8e6c9
    style Reject fill:#ffcdd2
    style QuotaError fill:#fff9c4
    style Success fill:#c8e6c9
```

### ðŸ“ˆ Scaling Architecture

```mermaid
graph TB
    subgraph LB["ðŸ”„ Load Balancing Layer"]
        Proxy["Reverse Proxy<br/>(Nginx/HAProxy)"]
    end
    
    subgraph API["ðŸš€ API Servers<br/>(Horizontally Scalable)"]
        Instance1["FastAPI Instance 1<br/>(Gunicorn)"]
        Instance2["FastAPI Instance 2<br/>(Gunicorn)"]
        InstanceN["FastAPI Instance N<br/>(Gunicorn)"]
    end
    
    subgraph Data["ðŸ’¾ Data Layer"]
        PG["PostgreSQL Primary"]
        PGRead1["Read Replica 1"]
        PGRead2["Read Replica N"]
    end
    
    subgraph Cache["âš¡ Cache & Queue Layer"]
        Redis["Redis Cluster<br/>â€¢ Task Queue<br/>â€¢ Result Backend<br/>â€¢ Caching<br/>â€¢ Sessions"]
    end
    
    subgraph Workers["ðŸ”§ Worker Layer"]
        Celery["Celery Workers<br/>(Async Processing)"]
    end
    
    Client["ðŸ‘¥ Clients"]
    
    Client -->|HTTP/HTTPS| Proxy
    Proxy --> Instance1
    Proxy --> Instance2
    Proxy --> InstanceN
    
    Instance1 --> PG
    Instance2 --> PG
    InstanceN --> PG
    
    Instance1 --> PGRead1
    Instance2 --> PGRead2
    InstanceN --> PGRead1
    
    Instance1 --> Redis
    Instance2 --> Redis
    InstanceN --> Redis
    
    Redis --> Celery
    Celery --> Redis
    
    style LB fill:#e1bee7
    style API fill:#c5e1a5
    style Data fill:#ffccbc
    style Cache fill:#ffccbc
    style Workers fill:#b2dfdb
```

---

## ðŸ—ï¸ Architecture

### Clean Layered Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚     FastAPI Routers                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚     Business Logic Layer            â”‚
â”‚     (Services)                      â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚     Data Access Layer               â”‚
â”‚     (Repositories + ORM)            â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚     Infrastructure                  â”‚
â”‚     (Database, Email, Cache)        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Key Design Principles

- **Async-First:** Non-blocking I/O with asyncio
- **Separation of Concerns:** Clear router â†’ service â†’ repository pattern
- **Dependency Injection:** FastAPI's Depends() for loose coupling
- **Error Handling:** Comprehensive exception handling with proper HTTP codes

---

## ðŸ“Š Project Structure

```
MailApixAPI/
â”‚
â”œâ”€â”€ ðŸŽ® Routers/
â”‚   â”œâ”€â”€ user.py              â”‚ User registration & token management
â”‚   â””â”€â”€ email.py             â”‚ Email sending endpoints
â”‚
â”œâ”€â”€ âš™ï¸ Services/
â”‚   â”œâ”€â”€ UserServices.py      â”‚ User business logic
â”‚   â””â”€â”€ EmailService.py      â”‚ Email delivery logic
â”‚
â”œâ”€â”€ ðŸ’¾ Controller/
â”‚   â”œâ”€â”€ database.py          â”‚ Database connection & session
â”‚   â”œâ”€â”€ models.py            â”‚ SQLAlchemy ORM models
â”‚   â”œâ”€â”€ schema.py            â”‚ Pydantic request/response schemas
â”‚   â””â”€â”€ parser.py            â”‚ Request parsers
â”‚
â”œâ”€â”€ ðŸŽ¨ Templates/
â”‚   â”œâ”€â”€ simple.py            â”‚ Plain text template
â”‚   â”œâ”€â”€ cool.py              â”‚ HTML template 1
â”‚   â”œâ”€â”€ amazing.py           â”‚ HTML template 2
â”‚   â”œâ”€â”€ impressive.py        â”‚ HTML template 3
â”‚   â””â”€â”€ System/
â”‚       â”œâ”€â”€ registration.py  â”‚ Registration email
â”‚       â”œâ”€â”€ packageplan.py   â”‚ Upgrade email
â”‚       â””â”€â”€ tokenrevert.py   â”‚ Token reset email
â”‚
â”œâ”€â”€ ðŸ“¦ Tasks/
â”‚   â””â”€â”€ revoke_token_tasks.py â”‚ Celery background tasks
â”‚
â”œâ”€â”€ __init__.py          â”‚ Package initialization
â”œâ”€â”€ main.py              â”‚ FastAPI app initialization
â”œâ”€â”€ celery_app.py        â”‚ Celery task queue setup  
â”œâ”€â”€ utils.py             â”‚ Helper functions
â”œâ”€â”€ logger.py            â”‚ Logging configuration        
â”‚
â””â”€â”€ .env                 â”‚ Environment variables
```

---

### ðŸ”Œ API Endpoints

### ðŸ“¥ **User Management** (GET)

| Endpoint | Purpose |
|----------|---------|
| `ðŸ“ GET /users/info` | Get user details |
| `ðŸ“ GET /users/upgrade` | Request upgrade plan |

### âœï¸ **User Creation/Auth** (POST)

| Endpoint | Purpose |
|----------|---------|
| `ðŸ“ POST /users/` | Register new user |
| `ðŸ“ POST /users/revokeKey/{id}` | Generate revoke key |
| `ðŸ“ POST /users/newToken/{id}` | Generate new token |

### ðŸ”„ **User Updates** (PUT)

| Endpoint | Purpose |
|----------|---------|
| `ðŸ“ PUT /users/secureAccount/{id}` | Set account password |

### ðŸ“§ **Email Sending** (POST)

| Endpoint | Purpose |
|----------|---------|
| `ðŸ“ POST /email/` | Send with user SMTP |
| `ðŸ“ POST /email/default` | Send with system SMTP |

### ðŸ“‹ Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| ðŸ·ï¸ `template_id` | int | Template ID (0-4) |
| ðŸ¢ `company_name` | string | Company name |
| ðŸ”— `company_link` | string | Company website |
| ðŸ“„ `email_title` | string | Email subject |

---

## ðŸ’¾ Technology Stack

- ðŸ **Framework:** FastAPI (Python)
- ðŸ—„ï¸ **Database:** PostgreSQL with asyncpg
- ðŸ”— **ORM:** SQLAlchemy (async)
- âœ… **Validation:** Pydantic v2
- ðŸ“§ **Email:** SMTP (smtplib)
- ðŸ“¬ **Background Tasks:** Celery + Redis
- ðŸš€ **Deployment:** Gunicorn + Uvicorn
- ðŸ“š **API Docs:** Swagger/OpenAPI

---

## ðŸŽ¨ Templates

| ID | Type | Use Case |
|----|------|----------|
| **0ï¸âƒ£** | Plain Text | Simple transactional emails |
| **1ï¸âƒ£** | Professional | Business communications |
| **2ï¸âƒ£** | Modern | Product notifications |
| **3ï¸âƒ£** | Elegant | Marketing campaigns |
| **4ï¸âƒ£** | Custom | Full HTML control |

### ðŸ·ï¸ Template Variables

All templates support:
- `title` - ðŸ“ Email heading
- `content` - ðŸ“„ Email body
- `company_name` - ðŸ¢ Company name
- `company_link` - ðŸ”— Company website

---

## ðŸš¢ Deployment

### ðŸ³ Production Setup

```bash
# Build container
docker build -t mailapix-api .

# Run with Gunicorn
gunicorn -k uvicorn.workers.UvicornWorker MailApixAPI.main:app \
  --workers 4 \
  --bind 0.0.0.0:8000
```

### ðŸ” Environment Variables

```env
# ðŸ—„ï¸ Database
DATABASE_USERNAME=postgres_user
DATABASE_PASSWORD=postgres_password
DATABASE_HOSTNAME=localhost
DATABASE_NAME=mailapix_db

# ðŸ“§ Email
SYSTEM_EMAIL=you@example.com
SYSTEM_EMAIL_PASSKEY=app_password

# ðŸ“¬ Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

### âœ… Deployment Checklist

- âœ… Use managed PostgreSQL (RDS, Cloud SQL)
- âœ… Store secrets in environment variables
- âœ… Enable HTTPS at reverse proxy
- âœ… Configure rate limiting
- âœ… Set up database backups
- âœ… Monitor logs and errors
- âœ… Use strong email passwords

---

## ðŸ›¡ï¸ Security

### ðŸ”’ Best Practices

- ðŸ” Never commit `.env` files or secrets
- ðŸ”„ Rotate `SYSTEM_EMAIL_PASSKEY` every 90 days
- ðŸ›¡ï¸ Use HTTPS in production
- â›” Configure CORS explicitly (not `*`)
- ðŸš¦ Implement rate limiting
- ðŸ“Š Monitor quota usage
- ðŸ”‘ Treat API tokens like passwords
- ðŸ“§ Validate email addresses

### ðŸ“‹ Security Policy

Have you found a security vulnerability? Please follow responsible disclosure:

ðŸ‘‰ [Security Policy](./SECURITY.md)

---

## ðŸ“ License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) for details.

---

## ðŸ‘¨â€ðŸ’» Author

**Sumit Dubey**

- ðŸ”— GitHub: [https://github.com/Sumit0ubey](https://github.com/Sumit0ubey)
- ðŸ“§ Email: sumitdubey810@outlook.com

---

## â­ Show Your Support

If you found this project helpful, useful, or interesting, please consider **giving it a star** on GitHub! Your support helps:

- ðŸš€ Reach more developers who need this solution
- ðŸ’ª Motivate continued development and improvements
- ðŸŒŸ Build a stronger community around the project

---

## ðŸ“š Additional Resources

- ðŸ¤ [Contributing Guidelines](./CONTRIBUTING.md)
- ðŸ“œ [Code of Conduct](./CODE_OF_CONDUCT.md)
- ðŸ“– [API Documentation](./API_DOCUMENTATION.md)


