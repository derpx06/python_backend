# Task API — Scalable REST API with JWT Auth & RBAC

A production-ready full-stack Task Management application featuring a backend API built with **Python 3.12 / FastAPI**, asynchronous **PostgreSQL 17** integration via **SQLAlchemy 2.0 / Alembic**, secure stateless **JWT authentication** with role-based access control (RBAC), and a modern, responsive **Next.js 15** frontend.

The system is fully containerized using **Docker** and **Docker Compose**, providing a seamless localized setup experience, automated seed utilities, robust structured logging, and comprehensive input validation.

---

## 🚀 Key Features

### 🔒 Core Authentication & RBAC
- **Double JWT Flow**: Custom middleware extracting Access Tokens (15 min expiry) and Refresh Tokens (7 days expiry) via header validation.
- **Password Security**: State-of-the-art password hashing using `bcrypt` with `passlib` (12 salt rounds).
- **Role-Based Access Control (RBAC)**:
  - `USER`: Has self-contained workspace permissions. They can create, view, list, update, and delete tasks they own.
  - `ADMIN`: Possesses system-wide permissions. They can query, edit, and purge tasks belonging to any registered user in the database.
- **Automated Seeding**: On service startup, a lifespan event automatically initializes database tables and seeds a default administrative user.

### ⚡ Backend Architecture
- **Asynchronous Stack**: Built completely on FastAPI with asynchronous routing, SQLAlchemy's `asyncpg` driver, and async database sessions.
- **Input Validation**: Zero-trust JSON parsing using Pydantic v2 schemas.
- **Centralized Error Handling**: Custom middleware-level handlers returning uniform JSON representations for validation failures, exceptions, and resource limits.
- **Structured Logging**: Production logging configured with `Loguru` utilizing automated log rotation (`10 MB`), file archiving (`gz`), and retention (`30 days`).

### 🎨 Frontend Client
- **Modern UI Elements**: Custom dark/light premium layouts leveraging glassmorphism (translucency, backdrop-blur), gradients, micro-animations, and CSS Custom Properties.
- **Client State Management**: Integrated `AuthContext` to manage local session status, transparently store JWT tokens, and perform automated routing guards.
- **Custom Client API Wrapper**: Axios/Fetch wrappers utilizing inter-service communication paths.
- **Interactive Component Library**:
  - `Navbar`: Session indicator and responsive navigation actions.
  - `TaskCard`: Render tags representing status (`TODO`, `IN_PROGRESS`, `DONE`) with controls for edit/delete based on role permissions.
  - `TaskModal`: Dynamic form for creating and updating tasks with full validation.
  - `Toast`: Automated feedback alerts for user operations.

---

## 🛠 Tech Stack

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Backend** | `FastAPI`, `Uvicorn` | Asynchronous high-performance Python framework |
| **Database** | `PostgreSQL 17` | Relational database engine |
| **ORM** | `SQLAlchemy 2.0`, `asyncpg` | Python SQL Toolkit with Async IO support |
| **Migrations**| `Alembic` | Schema versioning and migration engine |
| **Validation**| `Pydantic v2` | Static and runtime data validation |
| **Security** | `python-jose`, `passlib` | Cryptographic signing, verification, and bcrypt hashing |
| **Frontend** | `Next.js 15`, `React 19` | Modern React framework with Server/Client Rendering |
| **Styling** | `Tailwind CSS v4` | Tailwind utility styles and custom CSS variables |
| **DevOps** | `Docker`, `Docker Compose` | Platform-agnostic container virtualization |

---

## 📁 Repository Layout

```
backend/
├── docker-compose.yml       # Local development & production multi-container orchestration
├── README.md                # System documentation
├── SCALABILITY.md           # Production horizontal & database scaling analysis
│
├── server/                  # FastAPI Application Source
│   ├── alembic/             # Alembic database migration histories
│   ├── app/                 # Backend core packages
│   │   ├── config.py        # Pydantic BaseSettings environment parsing
│   │   ├── database.py      # Async db engine, sessionmaker, and table initializer
│   │   ├── main.py          # App initialization, CORS, global handlers, and lifespan lifecycle
│   │   ├── middleware/      # Custom security and authorization middleware
│   │   ├── models/          # Declarative Base SQLAlchemy models (User, Task)
│   │   ├── routers/         # API Route Handlers (AuthRouter, TaskRouter)
│   │   ├── schemas/         # Pydantic schemas mapping request/response boundaries
│   │   └── services/        # Service layer housing raw business transactions
│   │
│   ├── alembic.ini          # Alembic configuration details
│   ├── Dockerfile           # Multistage backend container definition
│   ├── requirements.txt     # Python requirements list
│   └── .env.example         # Sample environment configurations
│
└── client/                  # Next.js Application Source
    ├── src/                 # Client source code
    │   ├── app/             # Next.js App Router (pages & global layouts)
    │   ├── components/      # Modular UI component files
    │   ├── context/         # AuthContext provider wrapper
    │   └── lib/             # API client utility config
    │
    ├── package.json         # Client dependencies & script directives
    └── Dockerfile           # Client container definition
```

---

## ⚙️ Environment Configuration

Both backend and docker environments leverage localized settings. Use the following parameters to adjust service behaviors (specified in `server/.env`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | `str` | `postgresql+asyncpg://postgres:postgres@localhost:5432/taskapi` | Async database endpoint string. |
| `DATABASE_URL_SYNC` | `str` | `postgresql://postgres:postgres@localhost:5432/taskapi` | Sync database connection endpoint for Alembic. |
| `JWT_SECRET_KEY` | `str` | `super-secret-jwt-key-change-in-production` | Cryptographic secret for signing access JWTs. |
| `JWT_REFRESH_SECRET_KEY` | `str` | `super-secret-refresh-key-change-in-production` | Cryptographic secret for signing refresh JWTs. |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| `int` | `15` | Expiry duration for Access Tokens. |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `int` | `7` | Expiry duration for Refresh Tokens. |
| `PORT` | `int` | `4000` | Local port binding for the backend server. |
| `ENVIRONMENT` | `str` | `development` | Environment environment (`development` / `production`). |
| `CORS_ORIGINS` | `str` | `http://localhost:3000` | Comma-separated list of allowed origins. |
| `ADMIN_EMAIL` | `str` | `admin@taskapi.com` | Seed admin email address. |
| `ADMIN_PASSWORD` | `str` | `admin12345` | Seed admin user password (min 8 chars). |
| `ADMIN_NAME` | `str` | `Admin User` | Seed admin display name. |

---

## 🏁 Quick Start Guide

### 🐳 Option A: Multi-Container Setup via Docker (Recommended)

Docker Compose spins up PostgreSQL 17, compiles the FastAPI app, builds the Next.js static asset bundles, and maps them to local ports:

```bash
# Clone the repository and navigate to the directory
cd backend

# Build and start all services
docker compose up --build
```

- **Next.js Client**: Available at `http://localhost:3000`
- **FastAPI Server**: Available at `http://localhost:4000`
- **Swagger Interactive Docs**: Available at `http://localhost:4000/api/docs`

> [!NOTE]
> Database table schemas are automatically created on startup by the server's lifespan hook, and the default admin user is seeded instantly.

---

### 💻 Option B: Manual Setup for Local Development

To run backend and client nodes locally outside Docker:

#### 1. Setup Postgres Database
Ensure a local PostgreSQL database instance is running. Create a target database named `taskapi`:
```sql
CREATE DATABASE taskapi;
```

#### 2. Run Backend Server
```bash
cd server

# Create and activate python virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install package dependencies
pip install -r requirements.txt

# Copy environment variables and verify settings
cp .env.example .env

# Perform database migration updates
alembic upgrade head

# Start the uvicorn development server
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

The backend server is active at `http://localhost:4000`. You can inspect the Swagger interface at `/api/docs` or ReDoc at `/api/redoc`.

#### 3. Run Frontend Client
```bash
cd client

# Install frontend dependencies
npm install

# Run the local development server
npm run dev
```

Open your browser to `http://localhost:3000`. The application will dynamically check local cookie tokens and route you to the login screen.

---

## 🔌 API Reference & Schema Documentation

All backend routes return structured responses under `/api/v1/*`.

### 🔑 Authentication Services

#### `POST /api/v1/auth/register`
Creates a new user profile with standard `USER` privileges.
- **Request Body**:
  ```json
  {
    "email": "developer@example.com",
    "password": "supersecretpassword",
    "name": "Jane Developer"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "success": true,
    "message": "User registered successfully.",
    "data": {
      "user": {
        "id": 2,
        "email": "developer@example.com",
        "name": "Jane Developer",
        "role": "USER",
        "created_at": "2026-06-02T01:45:00Z",
        "updated_at": "2026-06-02T01:45:00Z"
      }
    }
  }
  ```

#### `POST /api/v1/auth/login`
Validates credentials and delivers access and refresh tokens.
- **Request Body**:
  ```json
  {
    "email": "admin@taskapi.com",
    "password": "admin12345"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "message": "Login successful.",
    "data": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "user": {
        "id": 1,
        "email": "admin@taskapi.com",
        "name": "Admin User",
        "role": "ADMIN"
      }
    }
  }
  ```

#### `GET /api/v1/auth/me`
Retrieves information about the current authenticated session.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": {
      "user": {
        "id": 1,
        "email": "admin@taskapi.com",
        "name": "Admin User",
        "role": "ADMIN",
        "created_at": "2026-06-02T01:00:00Z",
        "updated_at": "2026-06-02T01:00:00Z",
        "task_count": 5
      }
    }
  }
  ```

#### `POST /api/v1/auth/refresh`
Issues a new Access Token using a valid Refresh Token.
- **Request Body**:
  ```json
  {
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
  }
  ```

---

### 📝 Task Management Services (Protected)
All endpoints require an `Authorization: Bearer <access_token>` header.

#### `GET /api/v1/tasks`
Lists tasks with options for sorting, filtering, searching, and pagination.
- **Query Parameters**:
  - `page` (int, default: `1`): Current page offset.
  - `limit` (int, default: `20`, max: `100`): Maximum records to fetch.
  - `status` (string, optional): Filter by `TODO`, `IN_PROGRESS`, or `DONE`.
  - `search` (string, optional): String to search inside task titles.
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": {
      "tasks": [
        {
          "id": 10,
          "title": "Complete README documentation",
          "description": "Elaborate detail on all endpoints and files",
          "status": "IN_PROGRESS",
          "owner_id": 2,
          "created_at": "2026-06-02T01:30:00Z",
          "updated_at": "2026-06-02T01:30:00Z"
        }
      ]
    },
    "meta": {
      "total": 1,
      "page": 1,
      "limit": 20,
      "total_pages": 1
    }
  }
  ```

#### `POST /api/v1/tasks`
Registers a new task.
- **Request Body**:
  ```json
  {
    "title": "Write unit tests",
    "description": "Establish Pytest unit test coverage",
    "status": "TODO"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "success": true,
    "message": "Task created successfully.",
    "data": {
      "task": {
        "id": 11,
        "title": "Write unit tests",
        "description": "Establish Pytest unit test coverage",
        "status": "TODO",
        "owner_id": 2,
        "created_at": "2026-06-02T01:46:12Z",
        "updated_at": "2026-06-02T01:46:12Z"
      }
    }
  }
  ```

#### `GET /api/v1/tasks/{task_id}`
Returns details of a single task.
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": {
      "task": {
        "id": 11,
        "title": "Write unit tests",
        "description": "Establish Pytest unit test coverage",
        "status": "TODO",
        "owner_id": 2,
        "created_at": "2026-06-02T01:46:12Z",
        "updated_at": "2026-06-02T01:46:12Z"
      }
    }
  }
  ```

#### `PUT /api/v1/tasks/{task_id}`
Updates details of a task (partially or fully).
- **Request Body**:
  ```json
  {
    "status": "IN_PROGRESS"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "message": "Task updated successfully.",
    "data": {
      "task": {
        "id": 11,
        "title": "Write unit tests",
        "description": "Establish Pytest unit test coverage",
        "status": "IN_PROGRESS",
        "owner_id": 2,
        "created_at": "2026-06-02T01:46:12Z",
        "updated_at": "2026-06-02T01:47:05Z"
      }
    }
  }
  ```

#### `DELETE /api/v1/tasks/{task_id}`
Permanently deletes a task.
- **Response (204 No Content)**: Returns empty body on success.

---

### 🔴 Standard Error Response
All validation errors and unhandled exceptions are mapped to a uniform format:
```json
{
  "success": false,
  "error": "Validation failed",
  "details": [
    {
      "field": "body -> password",
      "message": "String should have at least 8 characters"
    }
  ]
}
```

---

## 👥 Role-Based Access Rules

### Default Admin Account
The system automatically registers a default supervisor account for administrative testing:
- **Email**: `admin@taskapi.com`
- **Password**: `admin12345`
- **Role**: `ADMIN`

### Permission Matrix

| Feature / Action | Standard User (`USER`) | Admin (`ADMIN`) |
| :--- | :--- | :--- |
| **Register Account** | Yes | Yes |
| **Create Task** | Yes (Assigned to self) | Yes (Assigned to admin) |
| **List Own Tasks** | Yes | Yes |
| **List All Tasks (System-wide)**| No (Restricted to own) | Yes (All users' tasks) |
| **Edit Own Task** | Yes | Yes |
| **Edit Other Users' Tasks** | No | Yes |
| **Delete Own Task** | Yes | Yes |
| **Delete Other Users' Tasks** | No | Yes |

---

## 📈 Production Scalability

For a deep architectural review of production scaling strategies, consult [SCALABILITY.md](SCALABILITY.md). Key areas explored include:
- **Horizontal Pod Autoscaling**: stateless API operations backed by stateless JWTs deployed behind NGINX or Kubernetes Ingress routers.
- **Connection Pools & Replicas**: configuring SQLAlchemy pool limits with optional read replicas and PgBouncer proxy handlers.
- **Caching**: introducing Redis storage caches for fast authentication lookups, token blacklisting, and rate limit tracking.
- **Microservice Separation**: plans for detaching auth workflows into discrete microservices.

---

## 📝 License
This project is licensed under the MIT License.
