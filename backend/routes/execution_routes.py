from fastapi import APIRouter

from schemas.execution_schema import (
    CodeExecutionRequest,
    CodeExecutionResponse
)

from services.execution_service import execute_code

router = APIRouter()

@router.post(
    "/execute",
    response_model=CodeExecutionResponse
)
def execute_code_route(
    request: CodeExecutionRequest
):

    return execute_code(
        request.code,
        request.function_name,
        request.test_cases
    )