from models import Agent, PlayerType, Conversation
from auth import get_client


client = get_client()

host = Agent(
    player=PlayerType.HOST,
    system_message="You are thinking of a spoon. You will be asked questions and you answer questions with Yes/No only."
)

guesser = Agent(
    player=PlayerType.GUESSER,
    system_message="You are the guesser in the 20 questions game. You try to find what the other player is thinking of "
                   "by asking yes or no questions. With every question you provide examples of what yes or no"
                   "possibilities are. When you are sure of the answer or getting close to 20, you make a guess. "
                   "Ask a question.",
)

conversation = Conversation(
    current_player=guesser,
    next_player=host,
    conversation_history=[{
            "role": "system",
            "content": "Welcome, you are playing the 20 questions game!"
        }]
)

for i in range(3):
    print(f"\nIteration {i + 1}:")

    context = conversation.get_context(conversation.current_player)  # GUESSER
    question = conversation.current_player.get_response(context)  # QUESTION
    conversation.append_message(question)

    conversation.swap_players()
