from openai import OpenAI

from dotenv import load_dotenv

import os

import json

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENROUTER_API_KEY"),
    base_url = "https://openrouter.ai/api/v1"
)

def evaluate_solution(
        question: str,
        code: str,
        execution_result: str
):
    prompt = f"""
    You are a DSA interview evaluator.

    Question:
    {question}

    Candidate Code:
    {code}

    Execution Result:
    {execution_result}

    Evaluate: 
    - correctness
    - readability
    - optimization
    - edge case handling

    Return ONLY valid JSON:

    {{
        "score": 0-10,
        "feedback": [
            "...",
            "..." 
        ]
    }}
    """

    response = client.chat.completions.create(
        model = "openai/gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_text = response.choices[0].message.content

    parsed_response = json.loads(response_text)

    return parsed_response