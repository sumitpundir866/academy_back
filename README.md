
# arch -arm64 /opt/homebrew/bin/brew install redis
# arch -arm64 /opt/homebrew/bin/brew services start redis
# arch -arm64 /opt/homebrew/bin/brew services stop redis
# arch -arm64 /opt/homebrew/bin/brew services list









# 🚀 FastAPI Production-Ready Project Structure

This repository contains a **scalable, maintainable, production-ready
FastAPI architecture**.\
It follows industry best practices for API design, modular development,
database migrations, and clean separation of concerns.

## 📁 Project Structure Overview

    app/
    │
    ├── api/
    │   ├── routes/
    │   │   ├── academy_routes.py
    │   │   └── __init__.py
    │   └── __init__.py
    │
    ├── core/
    │   ├── config.py
    │   ├── security.py
    │   └── __init__.py
    │
    ├── db/
    │   ├── base.py
    │   ├── session.py
    │   ├── init_db.py
    │   ├── migrations/
    │   │   ├── env.py
    │   │   ├── alembic.ini
    │   │   ├── script.py.mako
    │   │   └── versions/
    │   │       └── <revision>.py
    │   └── __init__.py
    │
    ├── models/
    │   ├── user.py
    │   └── __init__.py
    │
    ├── schemas/
    │   ├── user.py
    │   └── __init__.py
    │
    ├── services/
    │   ├── user_service.py
    │   └── __init__.py
    │
    ├── utils/
    │   ├── hashing.py
    │   ├── logger.py
    │   └── __init__.py
    │
    ├── main.py
    ├── requirements.txt
    └── alembic.ini

## 🧩 Folder Responsibility Breakdown

### 🔹 app/main.py

Main application entry point.

### 🔹 app/api/v1/

API routes, dependencies, and versioning.

### 🔹 app/core/

Global config and security utilities.

### 🔹 app/db/

Database session, base models, migrations.

### 🔹 app/models/

SQLAlchemy ORM models.

### 🔹 app/schemas/

Pydantic request/response schemas.

### 🔹 app/services/

Business logic/service layer.

### 🔹 app/utils/

Helper utilities (hashing, logging).

------------------------------------------------------------------------

## 🚀 Getting Started

### Install Dependencies

    pip install -r requirements.txt

### Run Migrations

    alembic upgrade head

### Start Server

    uvicorn app.main:app --reload

Visit Swagger Docs: http://localhost:8000/docs
