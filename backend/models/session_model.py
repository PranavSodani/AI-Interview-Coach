from sqlalchemy import (
    Column, 
    Integer,
    String,
    DateTime,
    ForeignKey
)

from datetime import datetime

from database import Base

class InterviewSession(Base):

    __tablename__ = "interview_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_name = Column(String)

    start_time = Column(
        DateTime,
        default = datetime.utcnow
    )

    end_time = Column(
        DateTime,
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    current_question_number = Column(
        Integer,
        default=1
    )

    total_questions = Column(
        Integer,
        default=5
    )
    