from models.company_question_model import (
    CompanyQuestion
)


def get_company_questions(
    company,
    difficulty,
    topic,
    db
):

    questions = db.query(
        CompanyQuestion
    ).filter(
        CompanyQuestion.company == company,
        CompanyQuestion.difficulty == difficulty
    ).all()

    filtered_questions = []

    for question in questions:

        if (
            topic.lower()
            in question.topics.lower()
        ):

            filtered_questions.append(
                question
            )

    filtered_questions.sort(
        key=lambda x: x.frequency,
        reverse=True
    )

    return filtered_questions[:5]