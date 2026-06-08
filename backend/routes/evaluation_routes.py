from fastapi import APIRouter

from schemas.evaluation_schema import (
    EvaluationRequest,
    EvaluationResponse
)

from services.evaluation_service import evaluate_solution

router = APIRouter()

@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate_solution_route(
    request: EvaluationRequest
):
    return evaluate_solution(
        request.question,
        request.code,
        request.execution_result
    )