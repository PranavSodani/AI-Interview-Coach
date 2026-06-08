import ast

import math

from services.embedding_service import generate_embedding

from models.company_question_model import CompanyQuestion

def cosine_similarity(
        vec1,
        vec2
):
    
    dot_product = sum(
        a*b
        for a,b in zip(vec1, vec2)
    )

    magnitude1 = math.sqrt(
        sum(a * a for a in vec1)
    )

    magnitude2 = math.sqrt(
        sum(b * b for b in vec2)
    )

    if (
        magnitude1 == 0
        or magnitude2 == 0
    ):
        return 0
    
    return (
        dot_product / 
        (magnitude1 * magnitude2)
    )

def retrieve_similar_questions(
        query,
        db,
        top_k=5
):
    
    query_embedding = (
        generate_embedding(query)
    )

    query_embedding = ast.literal_eval(
        query_embedding
    )

    questions = db.query(CompanyQuestion).all()

    scored_questions = []

    for question in questions:

        question_embedding = (
            ast.literal_eval(
                question.embedding
            )
        )

        similarity = (
            cosine_similarity(
                query_embedding,
                question_embedding
            )
        )

        scored_questions.append(
            (
                similarity,
                question
            )
        )

    scored_questions.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        question
        for _, question
        in scored_questions[:top_k]
    ]