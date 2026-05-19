"""Import ORM models so Alembic can discover SQLAlchemy metadata.

Keep these imports out of app.db.base to avoid circular imports:
models import Base, while Alembic imports this module to register models.
"""

from app.db.base import Base
from app.modules.users.models import User  # noqa: F401

__all__ = ["Base"]
