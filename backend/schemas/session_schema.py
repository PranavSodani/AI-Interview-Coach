from pydantic import BaseModel

class StartSessionRequest(BaseModel):

    user_id: int

    session_name: str


class StartSessionResponse(BaseModel):

    session_id: int

    session_name: str

    current_question_number: int

    total_questions: int


class SessionSummaryResponse(BaseModel):

    session_id: int

    session_name: str

    total_questions: int

    average_score: float

    topics_covered: list[str]

    weak_topics: list[str]

    duration_minutes: float | None