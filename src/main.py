from models.agent_models import Agent, PlayerType, Answer, Question
from models.game_models import Game
from src.prompts import HOST_PROMPT, GUESSER_PROMPT


def run_game(
    host_prompt: str,
    host_temperature: int,
    guesser_prompt: str,
    guesser_temperature: int,
    topic: str,
):
    host_prompt = host_prompt.format(topic=topic)

    host = Agent(
        player=PlayerType.HOST,
        system_message=host_prompt,
        response_object=Answer,
        temperature=host_temperature,
    )

    guesser = Agent(
        player=PlayerType.GUESSER,
        system_message=guesser_prompt,
        response_object=Question,
        temperature=guesser_temperature,
    )

    game = Game(topic=topic)
    statistics = game.play(guesser=guesser, host=host)

    return statistics


if __name__ == "__main__":
    game_statistics = run_game(
        host_prompt=HOST_PROMPT,
        host_temperature=0,
        guesser_prompt=GUESSER_PROMPT,
        guesser_temperature=0,
        topic="car",
    )
    print(game_statistics)
