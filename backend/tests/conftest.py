import pytest  # type: ignore[reportMissingImports]
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.database import engine, get_db
from app.main import app


@pytest.fixture
def client():
    connection = engine.connect()
    transaction = connection.begin()

    db = Session(bind=connection)

    def override_get_db():
        nested_transaction = db.begin_nested()

        try:
            yield db
            nested_transaction.commit()

        except Exception:
            nested_transaction.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()
        db.close()
        transaction.rollback()
        connection.close()
