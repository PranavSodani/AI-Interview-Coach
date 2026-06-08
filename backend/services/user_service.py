from models.user_model import User

from models.session_model import InterviewSession

from models.submission_model import Submission

from services.strategy_service import generate_interview_strategy

def create_user(
        username,
        firebase_uid: str,
        email,
        db
):

    existing_user = db.query(
        User
    ).filter(
        User.firebase_uid == firebase_uid
    ).first()

    if existing_user:

        return {
            "id": existing_user.id,
            "username":
                existing_user.username
        }

    user = User(
        username=username,
        firebase_uid=firebase_uid,
        email=email
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "id": user.id,
        "username": user.username
    }


def get_user_analytics(
    user_id: int,
    db
):
    print("NEW ANALYTICS RUNNING")
    sessions = db.query(
        InterviewSession
    ).filter(
        InterviewSession.user_id == user_id
    ).all()

    session_ids = [
        session.id
        for session in sessions
    ]

    submissions = db.query(
        Submission
    ).filter(
        Submission.session_id.in_(session_ids)
    ).all()

    strategy = (
        generate_interview_strategy(
            submissions
        )
    )

    total_sessions = len(sessions)

    total_questions = len(submissions)

    if total_questions == 0:

        average_score = 0

    else:

        average_score = sum(
            submission.evaluation_score
            for submission in submissions
        ) / total_questions

    topic_scores = {}

    difficulty_scores = {}

    submission_trend = []

    for submission in submissions:

        topic = submission.topic

        if topic not in topic_scores:

            topic_scores[topic] = []

        topic_scores[topic].append(
            submission.evaluation_score
        )

        submission_trend.append({
            "submission": len(submission_trend)+1,
            "score": submission.evaluation_score
        })

        difficulty = (
            submission.difficulty
            if submission.difficulty
            else "Unknown"
        )

        if difficulty not in difficulty_scores:

            difficulty_scores[difficulty] = []

        difficulty_scores[difficulty].append(
            submission.evaluation_score
        )

    weak_topics = []

    weakest_topic = None

    weakest_average = 100

    topic_performance = []

    difficulty_performance = []

    for topic, scores in topic_scores.items():

        average = sum(scores) / len(scores)

        rounded_average = round(
            average,
            1
        )

        topic_performance.append({
            "topic": topic,
            "average_score": rounded_average
        })

        if average < 7:

            weak_topics.append(topic)

        if average < weakest_average:

            weakest_average = average

            weakest_topic = topic

    for difficulty, scores in difficulty_scores.items():

        average = sum(scores) / len(scores)

        difficulty_performance.append({
            
            "difficulty": difficulty,

            "average_score": round(average, 1)
        });
    
    if len(submissions) == 0:
        average_attempts = 0
    else:
        average_attempts = sum(
            submission.attempt_number
            for submission in submissions
        ) / len(submissions)

    print(round(average_attempts,2))
    return {

        "user_id": user_id,

        "total_sessions": total_sessions,

        "total_questions": total_questions,

        "average_score": round(
            average_score,
            1
        ),

        "weak_topics": weak_topics,

        "recommended_topic": weakest_topic,

        "topic_performance": topic_performance,

        "submission_trend": submission_trend,

        "difficulty_performance": difficulty_performance,

        "strategy": strategy,

        "average_attempts": round(average_attempts, 2),
    }