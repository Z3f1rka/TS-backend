from sqlalchemy import BigInteger, String
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship  # noqa

from app.db.database import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    user = relationship("User", back_populates="feedbacks")
