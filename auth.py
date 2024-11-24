import os

from openai import OpenAI


def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")


def get_client():
    client = OpenAI(api_key=get_openai_api_key())
    return client
