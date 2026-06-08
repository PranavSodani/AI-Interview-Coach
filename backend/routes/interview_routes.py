from fastapi import APIRouter

from schemas.interview_schema import (
    SubmitSolutionRequest,
    SubmitSolutionResponse
)

from services.interview_service import (
    submit_solution,
    get_user_submission,
    get_user_analytics
)

from sqlalchemy.orm import Session

from fastapi import Depends

from database import get_db


router = APIRouter()

@router.post(
    "/submit-solution",
    response_model=SubmitSolutionResponse
)
def submit_solution_route(
    request: SubmitSolutionRequest,
    db: Session = Depends(get_db)
):
    return submit_solution(
        session_id=request.session_id,
        topic=request.topic,
        difficulty=request.difficulty,
        question=request.question,
        code=request.code,
        function_name=request.function_name,
        test_cases=request.test_cases,
        db=db
    )

@router.get("/user/{user_id}/submissions")
def get_user_submissions_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_submission(
        user_id,
        db
    )

@router.get("/analytics/{user_id}")
def get_analytics(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_analytics(user_id, db)