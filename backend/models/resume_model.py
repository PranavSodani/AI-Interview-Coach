from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from database import Base

class Resume(Base):

    __tablename__ = "resumes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    file_name = Column(
        String,
        nullable=False
    )

    extracted_text = Column(
        String,
        nullable=False
    )