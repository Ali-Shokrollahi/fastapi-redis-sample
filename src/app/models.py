from datetime import datetime
from sqlalchemy import String, Text, UniqueConstraint, func
from sqlalchemy.orm import mapped_column, Mapped

from src.core.database import Base


class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (
        UniqueConstraint("title", "company"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128), index=True)
    description: Mapped[str] = mapped_column(Text)
    company: Mapped[str] = mapped_column(String(128))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Job {self.title}>'
