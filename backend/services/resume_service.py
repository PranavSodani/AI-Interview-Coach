from pypdf import PdfReader
from io import BytesIO

from models.resume_model import Resume

from openai import OpenAI

import os

import json

client = OpenAI(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    ),
    base_url=
    "https://openrouter.ai/api/v1"
)

def extract_text_from_pdf(
        file_bytes
):
    
    pdf = PdfReader(
        BytesIO(file_bytes)
    )

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text

def save_resume(
        user_id,
        file_name,
        extracted_text,
        db
):
    
    resume = Resume(
        user_id = user_id,
        file_name = file_name,
        extracted_text = extracted_text
    )

    db.add(resume)

    db.commit()

    db.refresh(resume)

    return resume

def extract_resume_profile(
    resume_text
):
    prompt = f"""

    Analyze this resume.

    Extract:

    1. Skills
    2. Projects
    3. Experience

    Return ONLY valid JSON.

    Format:

    {{
        "skills": [],
        "projects": [],
        "experience": []
    }}

    Resume:

    {resume_text}

    """

    response = client.chat.completions.create(

        model="openai/gpt-3.5-turbo",
        max_tokens=1200,
        response_format={
            "type": "json_object"
        },

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_text = (
        response.choices[0]
        .message.content
    )

    print(response_text)

    parsed_response = json.loads(
        response_text
    )

    resume_level = "Beginner"

    if len(
        parsed_response.get(
            "experience",
            []
        )
    ) >= 2:
        resume_level = "Intermediate"

    if (
        len(
            parsed_response.get(
                "experience",
                []
            )
        ) >= 2
        and
        len(
            parsed_response.get(
                "projects",
                []
            )
        ) >= 2
    ):
        resume_level = "Advanced"

    parsed_response[
        "resume_level"
    ] = resume_level

    return parsed_response

def get_starting_difficulty(
        resume_level
):
    
    if resume_level == "Advanced":
        return "MEDIUM"
    
    if resume_level == "Intermediate":
        return "EASY"
    
    return "EASY"

def get_latest_resume(
        user_id,
        db
):
    return (
        db.query(Resume)
        .filter(
            Resume.user_id == user_id
        )
        .order_by(
            Resume.id.desc()
        )
        .first()
    )

def generate_resume_behavioral_questions(
        resume_text: str
):
    prompt = f"""
    You are a senior interviewer.

    Resume:

    {resume_text}

    Generate 5 personalized behavioral interview questions.

    Questions should be based on:
    - Projects
    - Experience
    - Skills

    Return valid JSON only:

    {{
        "questions": [
            "...",
            "...",
            "...",
            "...",
            "..."
        ]
    }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    response_text = response.choices[0].message.content

    parsed_reponse = json.loads(response_text)
    return parsed_reponse["questions"]
    
