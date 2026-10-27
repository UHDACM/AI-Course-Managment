from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Class(Base):
    __tablename__ = "classes"

    class_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    classname: Mapped[str] = mapped_column(String(100), nullable=False)
    assignment1: Mapped[str | None] = mapped_column(Text, nullable=True)