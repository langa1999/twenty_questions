import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv()

        self.model = os.getenv("MODEL", "gpt-4o-mini")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "100"))