from models.session_model import InterviewSession

from models.submission_model import Submission

from datetime import datetime

def start_session(
        user_id: int,
        session_name: str,
        db
):
    
    session = InterviewSession(
        user_id=user_id,
        session_name=session_name,
        current_question_number=1,
        total_questions=5
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return {
        "session_id": session.id,
        "session_name": session.session_name,
        "current_question_number": session.current_question_number,
        "total_questions": session.total_questions
    }

def get_session_summary(
        session_id: int,
        db
):
    
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id
    ).first()

    submissions = db.query(Submission).filter(
        Submission.session_id == session_id
    ).all()

    total_questions = len(submissions)

    if total_questions == 0:
        
        average_score = 0

    else:
        
        average_score = sum(
            submission.evaluation_score
            for submission in submissions
        ) / total_questions

    topics_covered = list(set(
        submission.topic
        for submission in submissions
    ))

    weak_topics = []

    topic_scores = {}

    for submission in submissions:

        topic = submission.topic

        if topic not in topic_scores:

            topic_scores[topic] = []

        topic_scores[topic].append(
            submission.evaluation_score
        )

    for topic, scores in topic_scores.items():

        average = sum(scores) / len(scores)

        if average < 7:

            weak_topics.append(topic)

    duration_minutes = None

    if session.end_time:

        duration = (
            session.end_time - session.start_time
        )

        duration_minutes = (
            duration.total_seconds() / 60
        )
    
    return {
        "session_id": session.id,
        "session_name": session.session_name,
        "total_questions": total_questions,
        "average_score": average_score,
        "topics_covered": topics_covered,
        "weak_topics": weak_topics,
        "duration_minutes": duration_minutes
    }

def end_session(
        session_id: int,
        db
):
    
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id
    ).first()

    session.end_time = datetime.utcnow()

    db.commit()

    db.refresh(session)

    return {
        "message": "Session ended succesfully"
    }