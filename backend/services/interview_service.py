from services.execution_service import execute_code

from services.evaluation_service import evaluate_solution

from services.followup_service import (
    generate_followup_question
)

from services.interview_agent_service import (
    decide_next_difficulty,
    decide_next_topic
)

from models.submission_model import Submission

from models.session_model import InterviewSession

from sqlalchemy import func


def submit_solution(
    session_id: int,
    topic: str,
    difficulty: str,
    question: str,
    code: str,
    function_name: str,
    test_cases: list,
    db
):

    execution_result = execute_code(
        code,
        function_name,
        test_cases
    )

    evaluation_result = evaluate_solution(
        question=question,
        code=code,
        execution_result=str(
            execution_result
        )
    )

    next_difficulty = (
        decide_next_difficulty(
            difficulty,
            evaluation_result["score"]
        )
    )

    current_session = db.query(
        InterviewSession
    ).filter(
        InterviewSession.id == session_id
    ).first()

    user_submissions = db.query(
        Submission
    ).join(
        InterviewSession,
        Submission.session_id ==
        InterviewSession.id
    ).filter(
        InterviewSession.user_id ==
        current_session.user_id
    ).all()

    next_topic = decide_next_topic(
        user_submissions,
        topic
    )
    previous_attempts = db.query(
            Submission
    ).filter(
        Submission.session_id == session_id,
        Submission.question == question
    ).count()

    attempt_number = (
        previous_attempts + 1
    )
    
    submission = Submission(
        session_id=session_id,
        topic=topic,
        difficulty=difficulty,
        question=question,
        submitted_code=code,
        execution_result=str(
            execution_result
        ),
        evaluation_score=
            evaluation_result["score"],
        feedback=str(
            evaluation_result["feedback"]
        ),
        attempt_number=attempt_number
    )

    db.add(submission)

    db.commit()

    db.refresh(submission)

    return {

        "execution":
            execution_result,

        "evaluation":
            evaluation_result,

        "next_difficulty":
            next_difficulty,

        "next_topic":
            next_topic,

        "current_question_number":
            current_session.current_question_number,

        "total_questions":
            current_session.total_questions
    }


def get_user_submission(
    user_id: int,
    db
):

    submissions = db.query(
        Submission
    ).join(
        InterviewSession,
        Submission.session_id ==
        InterviewSession.id
    ).filter(
        InterviewSession.user_id ==
        user_id
    ).all()

    return submissions


def get_user_analytics(
    user_id,
    db
):

    submissions = db.query(
        Submission
    ).join(
        InterviewSession,
        Submission.session_id ==
        InterviewSession.id
    ).filter(
        InterviewSession.user_id ==
        user_id
    ).all()

    total_submissions = len(
        submissions
    )


    if total_submissions == 0:

        return {

            "total_submissions": 0,

            "average_score": 0,

            "strong_topic": None,

            "weak_topic": None,

            "average_attempts": 0
        }
    
    average_attempts = sum(
        submission.attempt_number
        for submission in submissions
    ) / total_submissions

    average_score = sum(

        submission.evaluation_score

        for submission in submissions

    ) / total_submissions

    topic_scores = {}

    for submission in submissions:

        if (
            submission.topic
            not in topic_scores
        ):

            topic_scores[
                submission.topic
            ] = []

        topic_scores[
            submission.topic
        ].append(
            submission.evaluation_score
        )

    topic_average = {

        topic:
        sum(scores) / len(scores)

        for topic, scores
        in topic_scores.items()
    }

    strong_topic = max(
        topic_average,
        key=topic_average.get
    )

    weak_topic = min(
        topic_average,
        key=topic_average.get
    )

    return {

        "total_submissions":
            total_submissions,

        "average_score":
            round(average_score, 2),

        "strong_topic":
            strong_topic,

        "weak_topic":
            weak_topic,

        "average_attempts":
            round(average_attempts, 2)
    }