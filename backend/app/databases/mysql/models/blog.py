from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import DATETIME, TEXT, VARCHAR, LONGTEXT

from backend.app.databases.mysql.models.base import Base


class Blog(Base):
    __tablename__ = "blog"

    blog_id = Column(
        VARCHAR(100),
        primary_key=True,
    )
    question = Column(TEXT, nullable=False)
    introduction = Column(LONGTEXT, nullable=True)
    final_report = Column(LONGTEXT, nullable=True)
    created_dt = Column(DATETIME(6), nullable=False, default=text("CURRENT_TIMESTAMP"))
    updated_dt = Column(DATETIME(6), nullable=False, default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
