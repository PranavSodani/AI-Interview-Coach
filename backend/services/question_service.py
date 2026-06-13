import random

from openai import OpenAI

from dotenv import load_dotenv

from models.question_model import Question

from models.company_question_model import (
    CompanyQuestion
)

from sqlalchemy.orm import Session

from schemas.question_schema import (
    QuestionUpdate
)

from services.retrieval_service import (
    retrieve_similar_questions
)

from services.resume_service import (
    get_latest_resume,
    extract_resume_profile,
    get_starting_difficulty
)

from fastapi import HTTPException

import os

import json


load_dotenv()


client = OpenAI(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    ),
    base_url=
    "https://openrouter.ai/api/v1"
)

def generate_question(
    user_id,
    difficulty,
    company,
    experience_level,
    comfortable_topics,
    db
):
    
    if difficulty == "":
    
        latest_resume = get_latest_resume(
            user_id,
            db
        )

        if latest_resume:
            profile = extract_resume_profile(latest_resume.extracted_text)

            print(profile)

            resume_level = profile.get(
                "resume_level",
                "Intermediate"
            )

            difficulty = (
                get_starting_difficulty(
                    resume_level
                )
            )

            print(
                "Resume Level:",
                resume_level
            )

            print(
                "Selected Difficulty:",
                difficulty
            )
        else:

            difficulty = "MEDIUM"

    print("USER ID:", user_id)
    
    comfortable_topics_list = [
        topic.strip()
        for topic in comfortable_topics.split(",")
        if topic.strip()
    ]

    if comfortable_topics_list:
        topic = random.choice(comfortable_topics_list)
    else:
        topic = "Arrays"


    query = f"""

    Topic:
    {topic}

    Difficulty:
    {difficulty}

    Experience Level:
    {experience_level}

    Comfortable Topics:
    {comfortable_topics}

    Company:
    {company}

    INTERVIEW CALIBRATION:

    If experience level is Beginner:

    - Prefer easier patterns
    - Avoid advanced optimizations
    - Focus on fundamentals

    If experience level is Intermediate:

    - Use standard interview questions
    - Require reasonable optimization

    If experience level is Advanced:

    - Prefer harder variations
    - Include edge cases
    - Require optimal solutions
    - Expect deeper algorithmic thinking

    FIRST QUESTION PERSONALIZATION:

    The candidate has indicated
    the following comfortable topics:

    {comfortable_topics}

    Interview strategy:

    - If the selected topic is among
    the candidate's comfortable topics,
    generate a question that slightly
    challenges them.

    - If the selected topic is NOT among
    the comfortable topics,
    generate a more approachable
    question for that topic.

    - Use experience level together
    with comfortable topics when
    deciding complexity.

    - The goal is to start the interview
    at an appropriate level, not to
    immediately make it difficult.

    """

    retrieved_questions = (
        retrieve_similar_questions(
            query,
            db
        )
    )

    print(
        "\nRETRIEVED QUESTIONS:\n"
    )

    for question in retrieved_questions:

        print(
            question.title,
            question.frequency
        )

    retrieval_context = ""

    for question in retrieved_questions:

        retrieval_context += f"""

        Title:
        {question.title}

        Topics:
        {question.topics}

        Difficulty:
        {question.difficulty}

        Frequency:
        {question.frequency}

        """

    effective_difficulty = difficulty

    if topic not in comfortable_topics.split(","):
        if difficulty == "MEDIUM":
            effective_difficulty = "EASY"
        elif difficulty == "HARD":
            effective_difficulty = "MEDIUM"

    prompt = f"""

    You are a senior software engineer conducting
    a real technical interview.

    Generate ONE DSA interview question.

    INTERVIEW CONTEXT

    Topic:
    {topic}

    Difficulty:
    {effective_difficulty}

    Experience Level:
    {experience_level}

    Comfortable Topics:
    {comfortable_topics}

    INTERVIEW CALIBRATION RULES

    Candidate Experience Level:

    - Beginner:
    Focus on fundamentals.
    Avoid tricky edge cases.
    Avoid advanced optimizations.

    - Intermediate:
    Standard interview questions.
    Expect reasonable optimization.

    - Advanced:
    Challenging interview questions.
    Include edge cases and deeper reasoning.

    Topic Comfort Rules:

    - If the selected topic IS included in
    Comfortable Topics:
        - Use the requested difficulty.
        - Include realistic interview twists.
        - Expect stronger problem solving.

    - If the selected topic IS NOT included in
    Comfortable Topics:
        - Reduce complexity by one level.
        - Focus on fundamentals.
        - Avoid advanced variations.
        - Avoid combining multiple concepts.
        - The goal is calibration, not elimination.

    IMPORTANT:

    The FIRST interview question should help
    determine the candidate's level.

    Do not intentionally make the first question
    too difficult.

    QUESTION GENERATION RULES

    - The question should follow LeetCode style.

    - User should only complete
    the function.

    - Do NOT use input() or print().

    - starter_code MUST contain
    a valid Python function skeleton.

    - starter_code must include
    proper indentation and pass statement.

    - function_name MUST ONLY contain
    the function name.

    - function_name should NOT contain
    "def" or parameters.

    - test case input_data must be
    function arguments as JSON arrays.

    Return ONLY valid JSON
    in this format:

    {{
        "title": "...",

        "function_name":
        "two_sum",

        "starter_code":
        "def two_sum(nums, target):\\n    pass",

        "problem_statement":
        "...",

        "constraints":
        "...",

        "examples":
        "...",

        "visible_test_cases": [

            {{
                "input_data":
                [[1,2,3,4]],

                "expected_output":
                10
            }}
        ],

        "hidden_test_cases": [

            {{
                "input_data":
                [[1,2,3]],

                "expected_output":
                6
            }}
        ]
    }}

    Use these real interview
    questions as inspiration:

    {retrieval_context}

    Generate a similar but
    unique question inspired
    by these.

    ...
    """

    try:

        response = (
            client.chat.completions.create(

                model=
                "openai/gpt-3.5-turbo",
                max_tokens=500,

                response_format={
                    "type":
                    "json_object"
                },

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        response_text = (
            response.choices[0]
            .message.content
        )

        print(response_text)

        parsed_response = json.loads(
            response_text
        )

        question = Question(

            topic=topic,

            difficulty=difficulty,

            title=
            parsed_response["title"],

            problem_statement=
            parsed_response[
                "problem_statement"
            ],

            constraints=
            parsed_response[
                "constraints"
            ],

            examples=
            parsed_response[
                "examples"
            ]
        )

        db.add(question)

        db.commit()

        db.refresh(question)

        return parsed_response

    except Exception as e:

        print(e)

        raise e


def get_all_questions(
    db: Session
):

    questions = db.query(
        Question
    ).all()

    return questions


def get_question_by_id(
    question_id: int,
    db: Session
):

    question = db.query(
        Question
    ).filter(
        Question.id == question_id
    ).first()

    if question is None:

        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return question


def delete_question(
    question_id: int,
    db: Session
):

    question = db.query(
        Question
    ).filter(
        Question.id == question_id
    ).first()

    if question is None:

        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    db.delete(question)

    db.commit()

    return {
        "message":
        "Question deleted successfully"
    }


def update_question(
    question_id: int,
    updated_data: QuestionUpdate,
    db: Session
):

    question = db.query(
        Question
    ).filter(
        Question.id == question_id
    ).first()

    if question is None:

        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    update_data = updated_data.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            question,
            key,
            value
        )

    db.commit()

    db.refresh(question)

    return question