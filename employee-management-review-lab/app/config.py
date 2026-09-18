import os


class Config:
    SECRET_KEY = "enterprise-super-secret"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///employees.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "Welcome123"
    PAYROLL_API_URL = os.getenv("PAYROLL_API_URL", "https://example.invalid/payroll")
    TOKEN_TTL_HOURS = 168
