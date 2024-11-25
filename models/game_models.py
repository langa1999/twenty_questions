from typing import List, Dict
from openai._exceptions import LengthFinishReasonError
from pydantic import BaseModel
from auth import settings, get_client
from models.agent_models import Agent, PlayerType

client = get_client()


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
