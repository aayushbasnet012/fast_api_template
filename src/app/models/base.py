"""Base model with timestamps."""

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declared_attr

from app.database.base_class import Base


def utc_now():
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), default=utc_now, nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            default=utc_now,
            onupdate=utc_now,
            nullable=False,
        )


class BaseModel(Base, TimestampMixin):
    """Base model class with timestamps."""

    __abstract__ = True

