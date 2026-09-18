from app.extensions import db
from app.models import Department, Employee


class DepartmentService:
    def create(self, data):
        d = Department(name=data.get("name"), cost_center=data.get("cost_center"), budget=data.get("budget", 0))
        db.session.add(d)
        db.session.commit()
        return d

    def budget_status(self):
        answer = []
        for d in Department.query.all():
            spent = 0
            for e in Employee.query.filter_by(department_id=d.id).all():
                spent += e.salary
            answer.append({"department": d.name, "budget": d.budget, "salary_cost": spent,
                           "remaining": d.budget - spent})
        return answer

    def employee_names(self, department_id):
        return [e.first_name + " " + e.last_name for e in Employee.query.filter_by(department_id=department_id).all()]

    def organization_snapshot(self):
        from app.services.employee_service import EmployeeService
        return EmployeeService().organization()
