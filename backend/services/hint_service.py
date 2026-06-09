from openai import OpenAI

from dotenv import load_dotenv

import os
import json

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_hint(
        question: str,
        code: str,
        execution_result: str
):
    
    prompt = f"""
    You are a DSA interview coach.

    Question:
    {question}

    Candidate Code:
    {code}

    Execution Result:
    {execution_result}

    Give ONLY ONE small hint.

    DO NOT provide full solution.

    Return valid JSON only:

    {{
        "hint": "..."
    }}
    """

    response = client.chat.completions.create(
        model = "openai/gpt-3.5-turbo",
        max_tokens=300,
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

def evaluate_behavioral_answer(
        question: str,
        answer: str
):
    prompt = f"""
    You are a FAANG behavioral interviewer.

    Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate the answer.

    Give.  
    1. Overall feedback
    2. Strengths
    3. Areas of improvement

    Return valid JSON only:
    Example:
    {{
        "feedback": "Good Communication",
        "strengths": "Clear Structure",
        "improvements": "Provide more detail"
    }}

    Do not include markdown.
    Do not include explanation.
    Do not include code fences.
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content":
                prompt
            }
        ]
    )

    response_text = response.choices[0].message.content
    print("RAW RESPONSE:")
    print(response_text)

    try:
        parsed_reponse = json.loads(response_text)
        return parsed_reponse
    except Exception:
        return {
            "feedback": response_text,
            "strengths": "",
            "improvements": ""
        }
    
def generate_final_behavioral_report(answers):

    prompt = f"""
    You are a senior behavioral interviewer.

    Evaluate the candidate based on all interview answers below:

    {answers}

    Return valid JSON only.

    {{
        "communication_score": 0,
        "leadership_score": 0,
        "confidence_score": 0,
        "overall_score": 0,
        "hiring_recommendation": "",
        "summary": ""
    }}
    """

    print(prompt)

    response = client.chat.completions.create(
        model = "openai/gpt-3.5-turbo",
        max_tokens=300,
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

def generate_follow_up_question(
        question: str,
        answer: str
):
    prompt = f"""
    You are a senior interviewer.

    Original Question:
    {question}

    Candidate Answer:
    {answer}

    Generate ONE follow-up question that helps
    the interviewer understand the answer better.

    Return valid JSON only:

    {{
        "follow_up_question": "..."
    }}
    """

    response = client.chat.completions.create(
        model = "openai/gpt-3.5-turbo",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_text = response.choices[0].message.content

    parsed_reponse = json.loads(response_text)

    return parsed_reponse