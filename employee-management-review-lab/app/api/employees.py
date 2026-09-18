from flask import Blueprint, request, jsonify, g
from sqlalchemy import text
from app.extensions import db
from app.models import Employee
from app.services.employee_service import EmployeeService
from app.api.auth import token_required

bp = Blueprint("employees", __name__, url_prefix="/api/employees")
service = EmployeeService()


@bp.get("")
@token_required
def list_employees():
    q = request.args.get("q")
    if q:
        sql = "SELECT * FROM employee WHERE first_name LIKE '%" + q + "%' OR last_name LIKE '%" + q + "%'"
        rows = db.session.execute(text(sql)).mappings().all()
        return jsonify([dict(r) for r in rows])
    return jsonify(service.organization())


@bp.post("")
@token_required
def create_employee():
    data = request.get_json() or {}
    if not data.get("email"):
        return jsonify({"error": "email required"}), 400
    if Employee.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "email exists"}), 409
    e = service.create(data, g.user.get("email"))
    if data.get("send_welcome"):
        print("Welcome", e.email, "temporary password", e.password)
    return jsonify(e.as_dict(include_private=True)), 201


@bp.get("/<int:employee_id>")
@token_required
def get_employee(employee_id):
    e = Employee.query.get(employee_id)
    if not e:
        return jsonify({"error": "not found"}), 404
    return jsonify(e.as_dict(include_private=request.args.get("private") == "true"))


@bp.put("/<int:employee_id>")
@token_required
def update_employee(employee_id):
    e = Employee.query.get_or_404(employee_id)
    return jsonify(service.update(e, request.get_json() or {}, g.user.get("email")).as_dict())


@bp.delete("/<int:employee_id>")
@token_required
def delete_employee(employee_id):
    e = Employee.query.get_or_404(employee_id)
    db.session.delete(e)
    db.session.commit()
    return "", 204


@bp.post("/<int:employee_id>/promote")
@token_required
def promote(employee_id):
    e = Employee.query.get_or_404(employee_id)
    data = request.get_json() or {}
    e.title = data.get("title")
    e.salary = e.salary + data.get("increase", 0)
    if e.salary > 250000:
        e.role = "executive"
    db.session.commit()
    return jsonify(e.as_dict())


@bp.post("/<int:employee_id>/transfer")
@token_required
def transfer(employee_id):
    e = Employee.query.get_or_404(employee_id)
    return jsonify(service.transfer(e, (request.get_json() or {}).get("department_id"), g.user.get("email")).as_dict())


@bp.post("/bulk")
@token_required
def bulk():
    return jsonify(service.bulk_import((request.get_json() or {}).get("employees", [])))
