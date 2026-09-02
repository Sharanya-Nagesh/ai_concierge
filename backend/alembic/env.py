from logging.config import fileConfig
import os

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.models.base import Base

# Import all models so SQLAlchemy registers their tables
from app.models.user import User
from app.models.user_preference import UserPreference
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.memory import Memory
from app.models.document import Document
from app.models.planner_task import PlannerTask
from app.models.audit_log import AuditLog


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Alembic Config object
# ---------------------------------------------------------

config = context.config


# ---------------------------------------------------------
# Database URL
# ---------------------------------------------------------

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        "Make sure it is defined in the backend/.env file."
    )

config.set_main_option("sqlalchemy.url", database_url)


# ---------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ---------------------------------------------------------
# SQLAlchemy metadata
# ---------------------------------------------------------

target_metadata = Base.metadata


# ---------------------------------------------------------
# Offline migration
# ---------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------
# Online migration
# ---------------------------------------------------------

def run_migrations_online() -> None:
    """
    Run migrations using an active database connection.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------
# Execute migration
# ---------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()