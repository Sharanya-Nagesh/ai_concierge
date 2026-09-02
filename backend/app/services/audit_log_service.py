from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository


class AuditLogService:
    def __init__(self, db: Session):
        self.repository = AuditLogRepository(db)

    def create_log(self, audit_log: AuditLog) -> AuditLog:
        return self.repository.create(audit_log)

    def get_log(self, audit_log_id: UUID) -> AuditLog | None:
        return self.repository.get_by_id(audit_log_id)

    def get_user_logs(self, user_id: UUID) -> list[AuditLog]:
        return self.repository.get_by_user_id(user_id)