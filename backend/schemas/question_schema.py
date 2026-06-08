from pydantic import BaseModel

from typing import Optional

class TestCase(BaseModel):

    input_data: list

    expected_output: object

class QuestionResponse(BaseModel):
    title: str

    function_name: str

    starter_code: str

    problem_statement: str

    constraints: str

    examples: str

    visible_test_cases: list[TestCase]

    hidden_test_cases: list[TestCase]
    
class StoredQuestionResponse(BaseModel):
    id: int

    topic: str

    difficulty: str

    title: str

    problem_statement: str

    constraints: str
    
    examples: str

    class Config:
        from_attributes = True

class QuestionUpdate(BaseModel):

    topic: Optional[str] = None

    difficulty: Optional[str] = None

    title: Optional[str] = None

    problem_statement: Optional[str] = None

    constraints: Optional[str] = None

    examples: Optional[str] = None

