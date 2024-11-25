from enum import Enum
from typing import Literal, Type
from auth import get_client
from pydantic import BaseModel, Field

client = get_client()


class SuggestedQuestions(BaseModel):
    question: str = Field(description="Question in this format 'Is it a ...?'")
    pro_cons: str = Field(description="Identify how broad this question is, and if it eliminates the most options")
    answer: str = Field(description="Broad answers to the questions asked. Dont go into detail, keep broad categories.")


class Question(BaseModel):
    """
    This class is used by the guesser playing the 20 questions game.
    It makes a list of suggested questions analysing the pro/con of each question.
    The best question is selected
    We also don't care about size (small-dog, big-dog) or color (black-house, white-house).
    """
    is_final_guess: bool = Field(
        description="Return True if this is the final and best guess. Otherwise, return False."
    )
    content: str = Field(
        description="""This is the question to ask the user. For example: Is it an animal?
                    When you have narrowed it down, you are not afraid to make a final guess.
                    For example: 'My guess is a dog.'"""
    )


class Answer(BaseModel):
    response: Literal["yes", "no"]


class PlayerType(str, Enum):
    GUESSER = "GUESSER"
    HOST = "HOST"


class Agent(BaseModel):
    player: PlayerType
    system_message: str
    response_object: Type[Question | Answer]

