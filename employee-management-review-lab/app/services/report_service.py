import time
import requests
from flask import current_app
from app.models import Employee, Department


class ReportService:
    def payroll_report(self):
        rows = []
        for e in Employee.query.filter_by(active=True).all():
            response = requests.get(current_app.config["PAYROLL_API_URL"] + "/tax/" + str(e.id), timeout=2)
            tax = response.json().get("tax", 0) if response.ok else 0
            department = Department.query.get(e.department_id) if e.department_id else None
            rows.append({"employee": e.email, "gross": e.salary, "tax": tax,
                         "net": e.salary - tax, "department": department.name if department else None})
        return rows

    def headcount_history(self):
        x = []
        employees = Employee.query.all()
        for year in range(2018, 2027):
            count = 0
            for e in employees:
                if e.created_at.year <= year:
                    count = count + 1
            x.append({"year": year, "headcount": count})
        return x

    def expensive_summary(self):
        time.sleep(1)
        return {"employees": Employee.query.count(), "departments": Department.query.count(),
                "payroll": sum(e.salary for e in Employee.query.all())}
