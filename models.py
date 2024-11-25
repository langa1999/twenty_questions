from enum import Enum
from typing import List, Dict, Literal, Type, ClassVar
from auth import get_client, settings
from pydantic import BaseModel, Field
from openai._exceptions import LengthFinishReasonError

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


class GameStatistics(BaseModel):
    game_won: bool = False
    reason: str = ''
    iterations: int = 0
    question_answer_set: List[Dict] = []


class Game(BaseModel):
    question_answer_set: List[Dict] = []
    token_max: int = settings.max_tokens
    last_question: str = ''
    iterations: int = 0

    def play(self, guesser: Agent, host: Agent) -> GameStatistics:
        for x in range(20):
            while self.iterations < 20:
                if self.next_question(guesser=guesser, host=host):
                    print("Final guess has been made!")
                    if self.question_answer_set[-1]['answer'].lower() == 'yes':
                        game_statistics = GameStatistics(
                            game_won=True,
                            reason="Guesser guessed the topic",
                            iterations=self.iterations,
                            question_answer_set=self.question_answer_set,
                        )
                        return game_statistics
                    elif self.question_answer_set[-1]['answer'].lower() == 'no':
                        game_statistics = GameStatistics(
                            game_won=False,
                            reason="Guesser guessed the wrong topic",
                            iterations=self.iterations,
                            question_answer_set=self.question_answer_set,
                        )
                        return game_statistics

        game_statistics = GameStatistics(
            game_won=False,
            reason="Guesser ran out of questions",
            iterations=self.iterations,
            question_answer_set=self.question_answer_set,
        )
        return game_statistics

    def get_chat_completion(self, context: list[dict], response_format):
        try:
            response = client.beta.chat.completions.parse(
                model=settings.model,
                messages=context,
                max_tokens=self.token_max,
                temperature=0,
                response_format=response_format
            )
            return response
        except LengthFinishReasonError as e:
            self.token_max += 100
            print(f">>> Token limit increased to {self.token_max}")
            return self.get_chat_completion(context, response_format)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def next_question(self, guesser: Agent, host: Agent) -> bool:
        guess = self.get_chat_completion(
            context=self.get_context(guesser),
            response_format=guesser.response_object,
        )

        guess = guess.choices[0].message.parsed
        self.last_question = guess.content

        answer = self.get_chat_completion(
            context=self.get_context(host),
            response_format=host.response_object,
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
        result = "\nThese are the questions you have already asked: \n"
        for item in self.question_answer_set:
            result += f"{item['question']} {item['answer']}\n"
        result = result + f"\nYou have {str(20 - self.iterations)} questions left. "
        return result
