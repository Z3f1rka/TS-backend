from datetime import datetime

from sqlalchemy import BigInteger, Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
# from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship  # noqa

from app.db.database import Base


class Object(Base):
    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    # text: Mapped[str] = mapped_column(Text, nullable=True)
    # approved_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    # status: Mapped[str] = mapped_column(String, nullable=False, default='private')
    # photo: Mapped[str] = mapped_column(String, nullable=True)
    file: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow())
    main_object_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="objects")
