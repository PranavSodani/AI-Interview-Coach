from fastapi import APIRouter

from sqlalchemy.orm import Session

from fastapi import Depends

from database import get_db

from services.analytics_service import (
    get_weak_topics
)

router = APIRouter()

@router.get("/weak-topics")
def weak_topics_route(
    db: Session = Depends(get_db)
):
    return get_weak_topics(db)
