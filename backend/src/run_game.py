import time
from typing import AsyncGenerator

from backend.models.agent_models import Agent, PlayerType, Answer, Question
from backend.models.game_models import Game
from backend.src.prompts import HOST_PROMPT, GUESSER_PROMPT

from backend.models.game_models import QuestionAnswerSet

questions = [
    {'question': 'Is it a living thing?', 'answer': 'no', 'is_final_guess': False},
    {'question': 'Is it a physical object?', 'answer': 'yes', 'is_final_guess': False},
    {'question': 'Is it a man-made object?', 'answer': 'yes', 'is_final_guess': False},
    {'question': 'Is it something commonly found indoors?', 'answer': 'no', 'is_final_guess': False},
    {'question': 'Is it something commonly found outdoors?', 'answer': 'no', 'is_final_guess': False},
    {'question': 'Is it a tool?', 'answer': 'no', 'is_final_guess': False},
    {'question': 'Is it a vehicle?', 'answer': 'yes', 'is_final_guess': False},
    {'question': 'Is it a type of transportation?', 'answer': 'yes', 'is_final_guess': False},
    {'question': 'Is it a type of public transportation?', 'answer': 'no', 'is_final_guess': False},
    {'question': 'Is it a type of personal vehicle?', 'answer': 'yes', 'is_final_guess': False},
    {'question': 'Is it a type of motor vehicle?', 'answer': 'yes', 'is_final_guess': False},
    {'question': 'Is it a type of land vehicle?', 'answer': 'yes', 'is_final_guess': False},
    {'question': 'Is it a type of car?', 'answer': 'yes', 'is_final_guess': False},
    {'question': 'My guess is a car.', 'answer': 'yes', 'is_final_guess': True}
]


async def run_dummy_game() -> AsyncGenerator[QuestionAnswerSet, None]:
    for row in questions:
        yield QuestionAnswerSet(
            question=row['question'],
            answer=row['answer'],
            is_final_guess=row['is_final_guess']
        )
        time.sleep(1)


async def run_game(
    topic: str,
):
    host_prompt = HOST_PROMPT.format(topic=topic)

    host = Agent(
        player=PlayerType.HOST,
        system_message=host_prompt,
        response_object=Answer,
        temperature=0,
    )

    guesser = Agent(
        player=PlayerType.GUESSER,
        system_message=GUESSER_PROMPT,
        response_object=Question,
        temperature=0,
    )

    game = Game(topic=topic)

    async for value in game.play(guesser=guesser, host=host):
        yield value
