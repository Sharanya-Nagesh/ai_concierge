from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    def create_document(self, document: Document) -> Document:
        return self.repository.create(document)

    def get_document(self, document_id: UUID) -> Document | None:
        return self.repository.get_by_id(document_id)

    def get_user_documents(self, user_id: UUID) -> list[Document]:
        return self.repository.get_by_user_id(user_id)

    def update_document(self, document: Document) -> Document:
        return self.repository.update(document)

    def delete_document(self, document: Document) -> None:
        self.repository.delete(document)