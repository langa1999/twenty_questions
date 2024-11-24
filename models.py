from enum import Enum
from typing import List, Dict, Optional, Literal, Type
from auth import get_client
from pydantic import BaseModel, Field
import os

client = get_client()
model = os.getenv("MODEL")


class Question(BaseModel):
    """
    This class is used for the response from the guesser playing the 20 questions game.
    It can ask a question or make a guess. The guess does not need to be too specific. For example:
    If the user is thinking of a knife the LLM can guess "knife". It does NOT need to identify what type of knife it is.
    We also don't care about size (small-dog, big-dog) or color (black-house, white-house).
    """
    is_final_guess: bool = Field(
        description="Return True if this is the final and best guess. Otherwise, return False."
    )
    content: str = Field(
        description="This be next question to ask the user for example: Is it an animal? "
                    "Or it can be the final guess for example: My guess is a dog. "
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


class GameStatistics(BaseModel):
    game_won: bool = False
    reason: str = ''
    iterations: int = 0
    question_answer_set: List[Dict] = []


class Game(BaseModel):
    question_answer_set: List[Dict] = []
    last_question: str = ''
    iterations: int = 0

    def play(self, guesser: Agent, host: Agent) -> GameStatistics:
        game_won = False
        reason = "Guesser ran out of questions"
        for x in range(20):
            while self.iterations < 20:
                if self.next_question(guesser=guesser, host=host):
                    if self.question_answer_set[-1]['answer'].lower() == 'yes':
                        game_won = True
                        reason="Guesser guessed the topic"
                    elif self.question_answer_set[-1]['answer'].lower() == 'no':
                        game_won = False
                        reason = "Guesser guessed the wrong topic"

        game_statistics = GameStatistics(
            game_won=game_won,
            reason=reason,
            iterations=self.iterations,
            question_answer_set=self.question_answer_set,
        )
        return game_statistics

    def next_question(self, guesser: Agent, host: Agent) -> bool:

        # The guesser guesses a question
        guess = client.beta.chat.completions.parse(
            model=model,
            messages=self.get_context(guesser),
            max_tokens=150,
            temperature=0,
            response_format=guesser.response_object
        )

        guess = guess.choices[0].message.parsed

        self.last_question = guess.content

        answer = client.beta.chat.completions.parse(
            model=model,
            messages=self.get_context(host),
            max_tokens=150,
            temperature=0,
            response_format=host.response_object
        )
        answer = answer.choices[0].message.parsed

        self.question_answer_set.append({'question': self.last_question, 'answer': answer.response})

        print(self.question_answer_set[-1])

        self.iterations += 1

        return guess.is_final_guess

    def get_context(self, agent: Agent) -> List[Dict]:
        context = [{"role": "system", "content": agent.system_message}]
        if agent.player == PlayerType.GUESSER and self.question_answer_set:
            context.append({'role': 'assistant', 'content': self.format_question_answer_set()})

        elif agent.player == PlayerType.HOST and self.last_question:
            context.append({"role": "assistant", "content": self.last_question})

        return context

    def format_question_answer_set(self) -> str:
        result = "\nThis is what you know: \n"
        for item in self.question_answer_set:
            result += f"{item['question']} {item['answer']}\n"
        result = result + f"\nYou have {str(20 - self.iterations)} questions left. "
        return result
