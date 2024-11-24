from models.agent_models import Agent, PlayerType, Answer, Question
from models.game_models import Game
from prompts import HOST_PROMPT, GUESSER_PROMPT

host = Agent(
    player=PlayerType.HOST,
    system_message=HOST_PROMPT,
    response_object=Answer,
)

guesser = Agent(
    player=PlayerType.GUESSER,
    system_message=GUESSER_PROMPT,
    response_object=Question,
)

game = Game()

game_statistics = game.play(guesser=guesser, host=host)

print(game_statistics)
