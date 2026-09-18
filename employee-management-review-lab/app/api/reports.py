from flask import Blueprint, jsonify, request
from app.services.report_service import ReportService
from app.services.department_service import DepartmentService
from app.api.auth import token_required

bp = Blueprint("reports", __name__, url_prefix="/api/reports")
service = ReportService()


@bp.get("/payroll")
@token_required
def payroll():
    return jsonify(service.payroll_report())


@bp.get("/headcount")
@token_required
def headcount():
    return jsonify(service.headcount_history())


@bp.get("/summary")
def summary():
    data = service.expensive_summary()
    if request.args.get("include_budgets") == "true":
        data["budgets"] = DepartmentService().budget_status()
    return jsonify(data)
