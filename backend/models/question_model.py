from sqlalchemy import Column, Integer, String, Text
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index = True)
    
    topic = Column(String)
    
    difficulty = Column(String)
    
    title = Column(String)

    problem_statement = Column(Text)

    constraints = Column(Text)

    examples = Column(Text)
    