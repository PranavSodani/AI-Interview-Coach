import pandas as pd

import os

from database import SessionLocal

from models.company_question_model import (
    CompanyQuestion
)

from services.embedding_service import generate_embedding


BASE_PATH = "datasets"


db = SessionLocal()


for company_name in os.listdir(BASE_PATH):

    company_folder = os.path.join(
        BASE_PATH,
        company_name
    )

    if not os.path.isdir(
        company_folder
    ):
        continue

    csv_path = os.path.join(
        company_folder,
        "5. All.csv"
    )

    if not os.path.exists(csv_path):

        continue

    print(
        f"Ingesting {company_name}"
    )

    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():

        embedding_text = f"""
        Company:
        {company_name}

        Title:
        {row.get("Title")}

        Topics:
        {row.get("Topics")}

        Difficulty:
        {row.get("Difficulty")}
        """
        
        embedding = generate_embedding(embedding_text)

        question = CompanyQuestion(

            company=company_name,

            title=row.get("Title"),

            difficulty=row.get(
                "Difficulty"
            ),

            frequency=float(
                row.get("Frequency", 0)
            ),

            acceptance_rate=float(
                row.get(
                    "Acceptance Rate",
                    0
                )
            ),

            link=row.get("Link"),

            topics=row.get("Topics"),

            embedding=embedding
        )

        db.add(question)

    db.commit()

print("Done ingesting.")