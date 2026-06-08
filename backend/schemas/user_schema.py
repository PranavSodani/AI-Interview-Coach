from pydantic import BaseModel


class CreateUserRequest(BaseModel):

    username: str

    firebase_uid: str

    email: str


class UserResponse(BaseModel):

    id: int

    username: str


class TopicPerformance(BaseModel):

    topic: str

    average_score: float

class SubmissionTrend(BaseModel): 

    submission: int

    score: int

class DifficultyPerformace(BaseModel):

    difficulty: str

    average_score: float

class UserAnalyticsResponse(BaseModel):

    user_id: int

    total_sessions: int

    total_questions: int

    average_score: float

    weak_topics: list[str]

    recommended_topic: str | None

    topic_performance: list[TopicPerformance]

    submission_trend: list[SubmissionTrend]

    difficulty_performance: list[DifficultyPerformace]

    strategy: str

    average_attempts: float


