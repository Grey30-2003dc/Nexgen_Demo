import logging
from app.extensions import db
from app.models import AuditEvent


def record(actor, action, details):
    logging.info("audit actor=%s action=%s details=%s", actor, action, details)
    x = AuditEvent(actor=actor, action=action, details=str(details))
    db.session.add(x)
    db.session.commit()


def recent_events(limit=100):
    return AuditEvent.query.order_by(AuditEvent.created_at.desc()).limit(limit).all()
