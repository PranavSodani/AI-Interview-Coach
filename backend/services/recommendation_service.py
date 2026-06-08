from models.submission_model import Submission

def recommended_topic(db):

    submissoins = db.query(Submission).all()

    topic_scores = {}

    for submission in submissoins:
        
        topic = submission.topic

        score = submission.evaluation_score

        if topic not in topic_scores:
            
            topic_scores[topic] = []

        topic_scores[topic].append(score)
    
    weakest_topic = None

    weakest_average = 100

    for topic, scores in topic_scores.items():

        average_score = sum(scores) / len(scores)

        if average_score < weakest_average:

            weakest_average = average_score
            
            weakest_topic = topic

    return {
        "recommended_topic" : weakest_topic,
        "average_score": weakest_average
    }