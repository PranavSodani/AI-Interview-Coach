from models.submission_model import Submission


def get_weak_topics(db):

    submissions = db.query(
        Submission
    ).all()

    topic_scores = {}

    for submission in submissions:

        topic = submission.topic

        score = submission.evaluation_score

        if topic not in topic_scores:

            topic_scores[topic] = []

        topic_scores[topic].append(score)

    weak_topics = []

    for topic, scores in topic_scores.items():

        average_score = (
            sum(scores) / len(scores)
        )

        if average_score < 7:

            weak_topics.append({
                "topic": topic,
                "average_score": round(
                    average_score,
                    1
                )
            })

    topic_performance = []

    for topic, scores in topic_scores.items():

        average = sum(scores) / len(scores)

        topic_performance.append({
            "topic": topic,
            "average_score": round(
                average,
                1
            )
        })

    return {
        "weak_topics": weak_topics,
        "topic_performance": topic_performance
    }