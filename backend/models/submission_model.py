from sqlalchemy import ForeignKey

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from database import Base

class Submission(Base):

    __tablename__ = "submissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    topic = Column(String)

    difficulty = Column(String)

    question = Column(Text)

    submitted_code = Column(Text)

    execution_result = Column(Text)

    evaluation_score = Column(Integer)

    feedback = Column(Text)

    session_id = Column(
        Integer,
        ForeignKey("interview_sessions.id")
    )

    attempt_number = Column(
        Integer,
        default=1
    )

    

