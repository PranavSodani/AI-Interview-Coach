from fastapi import APIRouter

from schemas.question_schema import QuestionResponse

from schemas.question_schema import StoredQuestionResponse

from schemas.question_schema import QuestionUpdate

from schemas.behavioral_schema import BehavioralEvaluationRequest

from models.question_model import Question

from sqlalchemy.orm import Session

from database import get_db

from fastapi import Depends

from fastapi import HTTPException

from services import question_service

from models.question_model import Question

from services.hint_service import (
    evaluate_behavioral_answer,
    generate_final_behavioral_report,
    generate_follow_up_question,
    generate_adaptive_question
)

router = APIRouter()

@router.get("/generate-question", response_model = QuestionResponse)
def get_question(
    user_id: int,
    difficulty: str,
    company:str,
    experience_level: str,
    comfortable_topics: str,
    db: Session = Depends(get_db)
    ):

    return question_service.generate_question(user_id, difficulty, company, experience_level, comfortable_topics, db)


@router.get("/questions", response_model=list[StoredQuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return question_service.get_all_questions(db)


@router.get("/questions/{question_id}", response_model=StoredQuestionResponse)
def get_question_by_id(
    question_id: int,
    db: Session = Depends(get_db)
):
    return question_service.get_question_by_id(question_id,db)


@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    return question_service.delete_question(question_id, db)


@router.put("/questions/{question_id}", response_model=StoredQuestionResponse)
def update_question(
    question_id: int,
    updated_data: QuestionUpdate,
    db: Session = Depends(get_db)
):
    
    return question_service.update_question(question_id, updated_data, db)

@router.post("/evaluate-behavioral-answer")
async def evaluate_behavioral_answer_route(
    request: BehavioralEvaluationRequest
):
    result = evaluate_behavioral_answer(
        request.question,
        request.answer
    )
    return result

@router.post("/final-behavioral-report")
async def final_behavioral_report_route(request: dict):
    answers = request.get("answers", [])

    result = generate_final_behavioral_report(answers)

    return result

@router.post("/generate-follow-up-question")
def generate_follow_up_question_route(
    data: dict
):
    result = generate_follow_up_question(
        data["question"],
        data["answer"]
    )

    return result;

@router.post("/generate-adaptive-question")
def generate_adaptive_question_route(
    data: dict
):
    result = generate_adaptive_question(
        data["weaknesses"]
    )

    return result