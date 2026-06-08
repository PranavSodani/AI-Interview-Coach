from fastapi import APIRouter

from schemas.hint_schema import (
    HintRequest,
    HintResponse
)

from services.hint_service import (
    generate_hint
)

router = APIRouter()

@router.post("/generate-hint", response_model=HintResponse)
def generate_hint_route(
    request: HintRequest
):
    return generate_hint(
        request.question,
        request.code,
        request.execution_result
    )