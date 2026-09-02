from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.document import Document
from app.schemas.document_schema import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)

    document = Document(
        user_id=document_data.user_id,
        filename=document_data.filename,
        original_filename=document_data.original_filename,
        file_size=document_data.file_size,
        mime_type=document_data.mime_type,
        page_count=document_data.page_count,
        upload_status=document_data.upload_status,
        storage_path=document_data.storage_path,
    )

    return service.create_document(document)


@router.get(
    "/user/{user_id}",
    response_model=list[DocumentResponse],
)
def get_user_documents(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)

    return service.get_user_documents(user_id)


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)

    document = service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)

    document = service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    service.delete_document(document)