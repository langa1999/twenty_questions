from typing import List, Dict
from pydantic import BaseModel
from backend.src.auth import settings, get_chat_completion
from backend.models.agent_models import Agent, PlayerType


class GameRequest(BaseModel):
    topic: str


class QuestionAnswerSet(BaseModel):
    question: str
    answer: str
    is_final_guess: bool


class Game(BaseModel):
    topic: str = "car"
    question_answer_set: List[Dict] = []
    token_max: int = settings.max_tokens
    last_question: str = ""
    iterations: int = 0

    async def play(self, guesser: Agent, host: Agent):
        while self.iterations < 20:
            async for value in self.next_question(guesser=guesser, host=host):
                yield value
            if value.is_final_guess:
                break

    async def next_question(self, guesser: Agent, host: Agent):
        guess = await get_chat_completion(
            max_tokens=self.token_max,
            context=self.get_context(guesser),
            response_format=guesser.response_object,
            temperature=guesser.temperature,
        )

        guess = guess.choices[0].message.parsed
        self.last_question = guess.content

        answer = await get_chat_completion(
            max_tokens=self.token_max,
            context=self.get_context(host),
            response_format=host.response_object,
            temperature=host.temperature,
        )
        answer = answer.choices[0].message.parsed

        self.question_answer_set.append(
            {"question": self.last_question, "answer": answer.response}
        )

        self.iterations += 1

        yield QuestionAnswerSet(
            question=self.last_question,
            answer=answer.response,
            is_final_guess=guess.is_final_guess
        )

    def get_context(self, agent: Agent) -> List[Dict]:
        context = [{"role": "system", "content": agent.system_message}]
        if agent.player == PlayerType.GUESSER and self.question_answer_set:
            context.append(
                {"role": "assistant", "content": self.format_question_answer_set()}
            )

        elif agent.player == PlayerType.HOST and self.last_question:
            context.append({"role": "assistant", "content": self.last_question})

        return context

    def format_question_answer_set(self) -> str:
        result = "\nThese are the questions you have already asked: \n"
        for item in self.question_answer_set:
            result += f"{item['question']} {item['answer']}\n"
        result = result + f"\nYou have {str(20 - self.iterations)} questions left. "
        return result
