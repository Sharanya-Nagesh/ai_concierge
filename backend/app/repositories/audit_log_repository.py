from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, audit_log: AuditLog) -> AuditLog:
        self.db.add(audit_log)
        self.db.flush()
        self.db.refresh(audit_log)
        return audit_log

    def get_by_id(self, audit_log_id: UUID) -> AuditLog | None:
        statement = select(AuditLog).where(AuditLog.id == audit_log_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(self, user_id: UUID) -> list[AuditLog]:
        statement = (
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
        )
        return list(self.db.execute(statement).scalars().all())