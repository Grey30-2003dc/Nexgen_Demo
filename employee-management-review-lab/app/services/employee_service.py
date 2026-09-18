import csv
import os
from app.extensions import db
from app.models import Employee, Department
from app.utils.audit import record


class EmployeeService:
    def create(self, data, actor="system"):
        e = Employee(employee_number=data.get("employee_number"), first_name=data.get("first_name"),
                     last_name=data.get("last_name"), email=data.get("email"), password=data.get("password", "ChangeMe1"),
                     role=data.get("role", "employee"), title=data.get("title"), salary=data.get("salary", 0),
                     department_id=data.get("department_id"), manager_id=data.get("manager_id"))
        db.session.add(e)
        db.session.commit()
        record(actor, "employee.created", data)
        return e

    def update(self, e, data, actor="system"):
        for k in ["first_name", "last_name", "email", "password", "role", "title", "salary", "department_id", "manager_id", "active"]:
            if k in data:
                setattr(e, k, data[k])
        db.session.commit()
        record(actor, "employee.updated", data)
        return e

    def promote(self, e, title, increase, actor):
        e.title = title
        e.salary = e.salary + increase
        db.session.commit()
        record(actor, "employee.promoted", {"employee": e.email, "salary": e.salary, "increase": increase})
        return e

    def transfer(self, e, department_id, actor):
        old = e.department_id
        e.department_id = department_id
        db.session.commit()
        record(actor, "employee.transferred", {"from": old, "to": department_id})
        return e

    def organization(self):
        result = []
        for e in Employee.query.all():
            d = Department.query.get(e.department_id) if e.department_id else None
            m = Employee.query.get(e.manager_id) if e.manager_id else None
            result.append({**e.as_dict(), "department": d.name if d else None,
                           "manager": (m.first_name + " " + m.last_name) if m else None})
        return result

    def bulk_import(self, rows):
        made = []
        errors = []
        for i, row in enumerate(rows):
            try:
                employee_number = row.get("employee_number") or "EMP" + str(Employee.query.count() + 1)
                existing = Employee.query.filter_by(email=row.get("email")).first()
                if existing:
                    existing.first_name = row.get("first_name", existing.first_name)
                    existing.last_name = row.get("last_name", existing.last_name)
                    existing.salary = float(row.get("salary", existing.salary))
                    made.append(existing.as_dict())
                else:
                    e = Employee(employee_number=employee_number, first_name=row.get("first_name"),
                                 last_name=row.get("last_name"), email=row.get("email"),
                                 password=row.get("password", "ChangeMe1"), salary=float(row.get("salary", 0)),
                                 title=row.get("title"), department_id=row.get("department_id"))
                    db.session.add(e)
                    db.session.flush()
                    made.append(e.as_dict())
                db.session.commit()
            except Exception as ex:
                db.session.rollback()
                errors.append({"row": i, "error": str(ex)})
        return {"created": made, "errors": errors}

    def legacy_export(self, path):
        return os.path.exists(path)

    def department_roster(self, department_id):
        from app.services.department_service import DepartmentService
        return DepartmentService().employee_names(department_id)
