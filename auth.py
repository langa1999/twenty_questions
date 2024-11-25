from openai import OpenAI

from settings import Settings

settings = Settings()


def get_client():
    client = OpenAI(api_key=settings.api_key)
    return client
