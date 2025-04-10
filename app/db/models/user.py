from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship  # noqa

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False,
                                      default="tier1")  # tier1, tier2, tier3... чем больше цифра, тем больше привелегий
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    objects = relationship("Object", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
