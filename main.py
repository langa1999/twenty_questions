from models import Agent, PlayerType, Game, Answer, Question


def play_game(iterations: int, game: Game, guesser: Agent, host: Agent) -> bool:
    for x in range(iterations):
        print(f"\nQuestion {game.iterations}:")
        while game.iterations < 20:
            if game.next_question(guesser=guesser, host=host):
                if game.question_answer_set[-1]['answer'].lower() == 'yes':
                    game.game_won = True
                    return game.game_won
    return game.won


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

game_result = play_game(iterations=20, game=Game(), guesser=guesser, host=host)

print(f"The game was won: {game_result}")
