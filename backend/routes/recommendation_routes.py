from fastapi import APIRouter

from sqlalchemy.orm import Session

from fastapi import Depends

from database import get_db

from services.recommendation_service import (
    recommended_topic
)

router = APIRouter()

@router.get("/recommended-topic")
def recommended_topic_route(
    db: Session = Depends(get_db)
):
    return recommended_topic(db)