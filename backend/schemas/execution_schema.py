from pydantic import BaseModel

from typing import Optional

class TestCase(BaseModel):

    input_data: list

    expected_output: object

class CodeExecutionRequest(BaseModel):

    code: str

    function_name: str

    test_cases: list[TestCase]

class TestCaseResult(BaseModel):
    
    input_data: list

    expected_output: object

    actual_output: str

    passed: bool

    error: Optional[str] = None

class CodeExecutionResponse(BaseModel):

    results: list[TestCaseResult]

    all_passed: bool

    error: Optional[str] = None



    