def decide_next_difficulty(
        current_difficulty,
        score
):
    
    current_difficulty = current_difficulty.upper()

    if score >= 8:

        if current_difficulty == "EASY":
            return "MEDIUM"
        
        if current_difficulty == "MEDIUM":
            return  "HARD"
        
        return "HARD"
    
    elif score <= 4:

        if current_difficulty == "HARD":
            return "MEDIUM"
        
        if current_difficulty == "MEDIUM":
            return "EASY"
        
        return "EASY"
    
    return current_difficulty


def decide_next_topic(
        submissions,
        current_topic
):
    
    if len(submissions) == 0:

        return current_topic
    
    topic_scores = {}

    for submission in submissions:

        topic = submission.topic

        if topic not in topic_scores:

            topic_scores[topic] = []

        topic_scores[topic].append(
            submission.evaluation_score
        )
    
    topic_average = {
        topic:
        sum(scores) / len(scores)
        for topic, scores
        in topic_scores.items()
    }

    weakest_topic = min(topic_average,key=topic_average.get)

    return weakest_topic