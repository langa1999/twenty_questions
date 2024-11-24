from enum import Enum
from typing import List, Dict, Optional
import openai

from pydantic import BaseModel, Field


class Guess(BaseModel):
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
    examples: Optional[str] = Field(
        description="Examples of yes and no answers. Use this format: Yes (e.g., dog, cat), No (e.g., cars, bicycles). "
                    "If is_final_guess is True, this field is left empty."
    )


class GuessResponse(BaseModel):
    response: bool


class PlayerType(str, Enum):
    GUESSER = "GUESSER"
    HOST = "HOST"


class Agent(BaseModel):
    player: PlayerType
    system_message: str

    def get_response(self, context: List[Dict]) -> List[Dict]:
        print(f"CONTEXT = {context}")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context,
            max_tokens=150,
            temperature=0,
        )

        content = response.choices[0].message.content
        print(f"RESPONSE = {content}")
        return [{'role': 'assistant', 'content': content}]


class Conversation(BaseModel):
    current_player: Agent
    next_player: Agent
    conversation_history: List[Dict] = []
    last_question: str = ''

    def get_context(self, agent: Agent) -> List[Dict]:
        if agent.player == PlayerType.GUESSER:
            context = agent.system_message
            for i in range(1, len(self.conversation_history) - 1, 2):
                context += "This is what you know: \n"
                context += self.conversation_history[i]['content'] + ": " + self.conversation_history[i + 1][
                    'content'] + "\n"
            return [{"role": "assistant", "content": context}]

        elif agent.player == PlayerType.HOST:
            context = [{"role": "system", "content": agent.system_message},
                       {"role": "assistant", "content": self.conversation_history[-1]['content']}
                       ]
            return context

    def swap_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    def append_message(self, message: List[Dict]) -> None:
        self.conversation_history += message
