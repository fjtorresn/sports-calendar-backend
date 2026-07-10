from datetime import datetime, timezone
from typing import List, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app.core.database import Base

if TYPE_CHECKING:
    from .event import Event
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    preferences: Mapped[List["UserPreference"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    own_events: Mapped[List["Event"]] = relationship(back_populates="creator")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    entity_type: Mapped[str] = mapped_column(String(30), nullable=False) # "nation", "sport", "competition", etc.
    entity_id: Mapped[int] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="preferences")