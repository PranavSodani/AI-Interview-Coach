from openai import OpenAI

from dotenv import load_dotenv

import os


load_dotenv()


client = OpenAI(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    ),
    base_url=
    "https://openrouter.ai/api/v1"
)


def generate_interview_strategy(
    submissions
):

    history = ""

    for submission in submissions:

        history += f"""

        Topic:
        {submission.topic}

        Difficulty:
        {submission.difficulty}

        Score:
        {submission.evaluation_score}

        """

    prompt = f"""

    You are an expert FAANG
    interview coach.

    Analyze the candidate's
    interview history and create:

    1. Weakness analysis
    2. Strength analysis
    3. Recommended learning plan
    4. Suggested next focus area

    Keep response concise,
    strategic,
    and realistic.

    Interview History:

    {history}

    """

    response = client.chat.completions.create(

        model="openai/gpt-3.5-turbo",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[
        0
    ].message.content