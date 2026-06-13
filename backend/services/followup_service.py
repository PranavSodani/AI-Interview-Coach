from openai import OpenAI

from dotenv import load_dotenv

import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_followup_question(
    original_question,
    submitted_code,
    evaluation_feedback
):
    
    prompt = f"""

    You are a FAANG interviewer.

    Based on the interview performance below,
    generate ONE intelligent follow-up question.  

    Original Question:
    {original_question}

    Candidate Code:
    {submitted_code}

    Evaluation feedback:
    {evaluation_feedback}

    IMPORTANT:

    - Ask a realistic follow-up.
    - Could be optimzation, edge case,
    scalability, or alternative approach.
    - Keep it concise.
    - Sound like real interviewer.  

    """

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        max_tokens=500,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content