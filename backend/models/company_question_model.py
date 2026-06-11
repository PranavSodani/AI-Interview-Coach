from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text
)

from database import Base

class CompanyQuestion(Base):

    __tablename__ = "company_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company = Column(String)

    title = Column(String)

    difficulty = Column(String)

    frequency = Column(Float)

    acceptance_rate = Column(Float)

    link = Column(Text)

    topics = Column(Text)

    embedding = Column(Text)