from fastapi import APIRouter

from sqlalchemy.orm import Session

from fastapi import Depends

from database import get_db

from schemas.session_schema import (
    StartSessionRequest,
    StartSessionResponse,
    SessionSummaryResponse
)

from services.session_service import (
    start_session,
    get_session_summary
)

from services.session_service import (
    end_session
)


router = APIRouter()

@router.post("/start-session", response_model=StartSessionResponse)
def start_session_route(
    request: StartSessionRequest,
    db: Session = Depends(get_db)
):
    return start_session(
        request.user_id,
        request.session_name,
        db
    )

@router.get(
    "/session/{session_id}",
    response_model=SessionSummaryResponse
)
def session_summary_route(
    session_id: int,
    db: Session = Depends(get_db)
):
    
    return get_session_summary(
        session_id,
        db
    )

@router.post("/end-session/{session_id}")
def end_session_route(
    session_id: int,
    db: Session = Depends(get_db)
):

    return end_session(
        session_id,
        db
    )