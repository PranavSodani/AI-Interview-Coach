from openai import OpenAI

from dotenv import load_dotenv

import os


load_dotenv()


client = OpenAI(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    ),
    base_url=
    "https://openrouter.ai/api/v1"
)


def generate_embedding(text):

    response = (
        client.embeddings.create(

            model=
            "text-embedding-3-small",

            input=text
        )
    )

    embedding = (
        response.data[0].embedding
    )

    return str(embedding)