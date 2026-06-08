from pydantic import BaseModel

class BehavioralEvaluationRequest(BaseModel):
    question: str

    answer: str