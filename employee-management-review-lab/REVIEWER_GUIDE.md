# Reviewer Guide

> **Danger:** Findings are intentional. This project is exclusively a local AI code-review benchmark. Never deploy it, expose it to a network, or use real credentials or personal data.

No source file contains issue-marker comments; this is the sole answer key.

## Security

1. `app/config.py` hardcodes the Flask signing secret.
2. `app/config.py` hardcodes an administrator username and password.
3. `app/services/employee_service.py` assigns a shared default password.
4. `app/models.py` stores employee passwords in plaintext.
5. `app/services/auth_service.py` compares plaintext passwords directly.
6. `app/services/auth_service.py` disables JWT expiration verification.
7. `app/config.py` gives tokens an excessive seven-day lifetime.
8. `app/services/auth_service.py` logs submitted passwords.
9. `app/api/auth.py` logs complete bearer tokens and private user data.
10. `app/utils/audit.py` logs arbitrary details that can contain credentials, salaries, and PII.
11. `app/api/employees.py` constructs employee search SQL through string concatenation, allowing SQL injection.
12. `app/api/employees.py` has minimal create validation and accepts arbitrary roles, salaries, managers, and department IDs.
13. `app/api/employees.py` lets any authenticated user create, update, delete, promote, transfer, and bulk-import employees.
14. `app/api/employees.py` exposes plaintext passwords in create responses and optionally in GET responses.
15. `app/api/reports.py` exposes the summary endpoint without authentication.
16. `run.py` enables Flask debug mode and listens on every interface.

## Code quality

17. `app/services/employee_service.py` imports `csv` but never uses it.
18. `app/utils/validators.py` imports `re` and `json` but never uses either.
19. `app/utils/validators.py` contains the unused/dead `obsolete_validate_employee` function.
20. `app/services/employee_service.py` contains the unused/dead `legacy_export` method.
21. `app/services/employee_service.py` has a long, multi-responsibility `bulk_import` method.
22. `app/services/employee_service.py` is a large service combining CRUD, workflow, hierarchy, import, export, and audit concerns.
23. `app/services/employee_service.py` uses poor names such as `e`, `d`, `m`, and `made`.
24. Promotion logic is duplicated between `app/api/employees.py` and `EmployeeService.promote`.
25. Validation is inconsistent and duplicated across controllers and utility functions.
26. Broad exception handling in `bulk_import` hides programming and database errors.

## Performance

27. `EmployeeService.organization` performs department and manager lookups per employee (N+1 queries).
28. `app/api/departments.py` queries employees once per department (N+1 queries).
29. `DepartmentService.budget_status` queries employees once per department instead of aggregating in SQL.
30. `ReportService.payroll_report` calls an external tax API separately for every employee.
31. `ReportService.payroll_report` also loads each employee's department separately.
32. `ReportService.headcount_history` repeatedly scans all employees for every year.
33. `ReportService.expensive_summary` deliberately blocks for one second and has no cache.
34. Employee list and report endpoints return unpaginated result sets.
35. `bulk_import` performs count/lookups and commits inside the row loop.

## Architecture

36. `app/api/employees.py` places promotion business rules directly in the controller.
37. Services instantiate/query concrete SQLAlchemy models and commit global sessions, preventing dependency injection.
38. Controllers create global concrete service instances, tightly coupling HTTP and service layers.
39. `EmployeeService` depends directly on the audit utility, which depends directly on models and the database.
40. `EmployeeService.department_roster` and `DepartmentService.organization_snapshot` import each other's service locally, creating a circular dependency hidden until method execution.
41. `DepartmentService` combines persistence, payroll calculations, and presentation formatting, violating single responsibility.
42. `ReportService` mixes database access, third-party HTTP calls, calculations, and response shaping.
43. Models expose serialization behavior and allow private credential serialization.

## Testing

44. Only authentication and a small subset of employee behavior are tested.
45. `test_create_employee` uses `assert response.status_code`, which passes for error statuses too.
46. `test_empty_employee_list` merely checks for a non-null JSON value.
47. Tests duplicate application/login setup instead of using fixtures.
48. No tests cover SQL injection, authorization, token expiration, invalid JSON, duplicate IDs, negative salaries, reports, departments, deletion, updates, bulk-import rollback, or external API failures.
49. Tests use the same hardcoded administrator credentials as production configuration.

## Documentation

50. Public classes and functions lack docstrings throughout the project.
51. `README.md` falsely claims passwords are hashed with bcrypt.
52. `README.md` falsely claims reports are cached and PostgreSQL/pagination are supported.
53. `README.md` says every endpoint requires authentication, but `/api/reports/summary` does not.
54. The API list omits transfer, bulk import, budgets, headcount, and summary endpoints.
55. The README claims broad test coverage and production readiness despite the intentionally weak suite and vulnerabilities.
