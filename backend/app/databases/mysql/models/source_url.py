from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import DATETIME, TEXT, TINYINT, VARCHAR, INTEGER

from backend.app.databases.mysql.models.base import Base


class SourceUrl(Base):
    __tablename__ = "source_url"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    blog_id = Column(VARCHAR(100), nullable=False)
    url = Column(TEXT, nullable=False)
    created_dt = Column(DATETIME(6), nullable=False, default=text("CURRENT_TIMESTAMP"))
    updated_dt = Column(DATETIME(6), nullable=False, default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
