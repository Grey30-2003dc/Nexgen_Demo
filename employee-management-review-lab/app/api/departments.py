from flask import Blueprint, request, jsonify
from app.models import Department
from app.services.department_service import DepartmentService
from app.api.auth import token_required

bp = Blueprint("departments", __name__, url_prefix="/api/departments")
service = DepartmentService()


@bp.get("")
@token_required
def list_departments():
    result = []
    for d in Department.query.all():
        result.append({**d.as_dict(), "employees": service.employee_names(d.id)})
    return jsonify(result)


@bp.post("")
@token_required
def create_department():
    data = request.get_json() or {}
    d = service.create(data)
    return jsonify(d.as_dict()), 201


@bp.get("/budgets")
@token_required
def budgets():
    return jsonify(service.budget_status())
