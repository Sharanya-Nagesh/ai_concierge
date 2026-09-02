from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, document: Document) -> Document:
        self.db.add(document)
        self.db.flush()
        self.db.refresh(document)
        return document

    def get_by_id(self, document_id: UUID) -> Document | None:
        statement = select(Document).where(Document.id == document_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(self, user_id: UUID) -> list[Document]:
        statement = (
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(Document.uploaded_at.desc())
        )
        return list(self.db.execute(statement).scalars().all())

    def update(self, document: Document) -> Document:
        self.db.flush()
        self.db.refresh(document)
        return document

    def delete(self, document: Document) -> None:
        self.db.delete(document)