from models import Agent, PlayerType, Game, Answer, Question

host = Agent(
    player=PlayerType.HOST,
    system_message="You are thinking of a spoon. You will be asked questions and you answer questions with Yes/No only.",
    response_object=Answer,
)

guesser = Agent(
    player=PlayerType.GUESSER,
    system_message="You are the guesser in the 20 questions game. "
                   "You try to find what the other player is thinking of by asking yes or no questions."
                   "When you are sure of the answer or getting close to 20, you make a guess. "
                   "Ask a question.",
    response_object=Question,
)

game = Game()

game_statistics = game.play(guesser=guesser, host=host)

print(game_statistics)
