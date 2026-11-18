
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


def utc_now():
    """Return the current timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class PreferenceMemory(Base):
    __tablename__ = "preference_memories"

    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'superseded', 'expired', 'archived')",
            name="ck_preference_memories_status",
        ),
        CheckConstraint(
            "valid_until IS NULL OR valid_until >= valid_from",
            name="ck_preference_memories_validity",
        ),
        Index(
            "ix_preference_memories_user_key_status",
            "user_id",
            "preference_key",
            "status",
        ),
        Index(
            "ix_preference_memories_user_scope_status",
            "user_id",
            "scope",
            "status",
        ),
    )

    # Unique identifier for each preference memory.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Identifies the user who owns this preference.
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # Identifies the preference dimension.
    # Example: detail_level, programming_language.
    preference_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Normalized preference value.
    # Example: detailed, Python, concise.
    canonical_value: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Original user statement, preserved for traceability.
    original_utterance: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Language in which the preference was expressed.
    # Example: en, kn.
    language: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # Script used in the original statement.
    # Example: Latin, Kannada.
    script: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    # Context in which the preference applies.
    # Examples: global, coding, NLP, interview_preparation.
    scope: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="global",
    )

    # Beginning of the preference's validity.
    valid_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    # End of validity. NULL means no scheduled expiry.
    valid_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Current lifecycle state of this preference.
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )

    # ID of the older preference replaced by this preference.
    # NULL means this preference does not supersede another record.
    supersedes_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("preference_memories.id"),
        nullable=True,
    )

    # Message from which this preference was extracted, if available.
    source_message_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("messages.id"),
        nullable=True,
    )

    # Record creation time.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    # Last modification time.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
