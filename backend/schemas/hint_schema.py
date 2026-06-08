from pydantic import BaseModel

class HintRequest(BaseModel):

    question: str

    code: str

    execution_result: str

class HintResponse(BaseModel):

    hint: str

    