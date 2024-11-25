import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL", "gpt-4o-mini")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "100"))

        # Validate required settings
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required but not set in the .env file.")
