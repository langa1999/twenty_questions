from models.agent_models import Agent, PlayerType, Answer, Question
from models.game_models import Game
from prompts import HOST_PROMPT, GUESSER_PROMPT


def run_game(host_prompt: str, guesser_prompt: str, topic: str):
    host_prompt = host_prompt.format(topic=topic)

    host = Agent(
        player=PlayerType.HOST,
        system_message=host_prompt,
        response_object=Answer,
    )

    guesser = Agent(
        player=PlayerType.GUESSER,
        system_message=guesser_prompt,
        response_object=Question,
    )

    game = Game(topic=topic)
    statistics = game.play(guesser=guesser, host=host)

    return statistics


if __name__ == "__main__":
    game_statistics = run_game(host_prompt=HOST_PROMPT, guesser_prompt=GUESSER_PROMPT, topic="car")
    print(game_statistics)
