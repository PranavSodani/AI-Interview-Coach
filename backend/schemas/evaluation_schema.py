from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    question : str

    code: str

    execution_result: str

class EvaluationResponse(BaseModel):
    score: int

    feedback: list[str]