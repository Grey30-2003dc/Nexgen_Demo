from datetime import datetime
from app.extensions import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    cost_center = db.Column(db.String(30))
    budget = db.Column(db.Float, default=0)
    employees = db.relationship("Employee", backref="department", lazy=True)

    def as_dict(self):
        return {"id": self.id, "name": self.name, "cost_center": self.cost_center, "budget": self.budget}


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_number = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False)
    password = db.Column(db.String(180), nullable=False)
    role = db.Column(db.String(30), default="employee")
    title = db.Column(db.String(120))
    salary = db.Column(db.Float, default=0)
    active = db.Column(db.Boolean, default=True)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    manager_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self, include_private=False):
        data = {"id": self.id, "employee_number": self.employee_number, "first_name": self.first_name,
                "last_name": self.last_name, "email": self.email, "role": self.role, "title": self.title,
                "salary": self.salary, "active": self.active, "department_id": self.department_id,
                "manager_id": self.manager_id}
        if include_private:
            data["password"] = self.password
        return data


class AuditEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor = db.Column(db.String(180))
    action = db.Column(db.String(120))
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
