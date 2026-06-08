from pydantic import BaseModel

from schemas.execution_schema import (
    TestCase,
    CodeExecutionResponse
)

from schemas.evaluation_schema import (
    EvaluationResponse
)

class SubmitSolutionRequest(BaseModel):

    session_id: int

    topic: str

    difficulty: str
    
    question: str

    code: str

    function_name: str

    test_cases: list[TestCase]

class SubmitSolutionResponse(BaseModel):

    execution: CodeExecutionResponse

    evaluation: EvaluationResponse

    next_difficulty: str

    next_topic: str

    current_question_number: int

    total_questions: int