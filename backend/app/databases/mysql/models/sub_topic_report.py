from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import DATETIME, TEXT, VARCHAR, INTEGER, LONGTEXT

from backend.app.databases.mysql.models.base import Base


class SubTopicReport(Base):
    __tablename__ = "sub_topic_report"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    blog_id = Column(
        VARCHAR(100),
        nullable=False,
    )
    sub_topic = Column(TEXT, nullable=False)
    report = Column(LONGTEXT, nullable=True)
    created_dt = Column(DATETIME(6), nullable=False, default=text("CURRENT_TIMESTAMP"))
    updated_dt = Column(DATETIME(6), nullable=False, default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
