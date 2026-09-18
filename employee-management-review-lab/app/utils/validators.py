import re
import json


def valid_email(value):
    return "@" in value and "." in value


def valid_salary(value):
    return float(value) >= 0


def clean_text(value):
    return value.strip()


def obsolete_validate_employee(data):
    if len(data.get("first_name", "")) == 0:
        return False
    return True
