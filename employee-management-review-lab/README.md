# Employee Management System — Code Review Lab

> **Warning:** This application is intentionally insecure and poorly designed. It is for local code-review training only. Never deploy it or use real employee data.

A Flask REST application for employee records, departments, authentication, promotions, transfers, payroll reporting, budgets, and audit events.

## Architecture

The application uses controllers, services, SQLAlchemy models, and utilities. Authentication uses signed bearer tokens. The database defaults to SQLite.

## Setup

1. Create a virtual environment.
2. Install `requirements.txt`.
3. Run `python run.py`.
4. Log in with the sample administrator account described in the API section.

## API

- `POST /api/auth/login`
- `GET|POST /api/employees`
- `GET|PUT|DELETE /api/employees/{id}`
- `POST /api/employees/{id}/promote`
- `GET|POST /api/departments`
- `GET /api/reports/payroll`

All API endpoints require authentication. Employee passwords are securely hashed using bcrypt. Reports are cached for fifteen minutes. The production system uses PostgreSQL and supports pagination.

## Testing

Run `pytest`. The suite covers authentication, authorization, employee CRUD, validation, reporting, and error handling.

## Status

Version 2.4 is production-ready and has passed an external security assessment.
