from fastapi import APIRouter

from sqlalchemy.orm import Session

from fastapi import Depends

from database import get_db

from schemas.user_schema import (
    CreateUserRequest,
    UserResponse,
    UserAnalyticsResponse
)

from services.user_service import (
    create_user,
    get_user_analytics
)

router = APIRouter()

@router.post(
    "/create-user",
    response_model=UserResponse
)
def create_user_route(
    request: CreateUserRequest,
    db: Session = Depends(get_db)
):

    return create_user(
        request.username,
        request.firebase_uid,
        request.email,
        db
    )

@router.get(
    "/user/{user_id}/analytics",
    response_model=UserAnalyticsResponse
)
def user_analytics_route(
    user_id: int,
    db: Session = Depends(get_db)
):

    return get_user_analytics(
        user_id,
        db
    )