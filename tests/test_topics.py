from concurrent.futures import ThreadPoolExecutor, as_completed
from main import run_game
from prompts import HOST_PROMPT, GUESSER_PROMPT

topics = [
    "Dog",
    "Car",
    "Apple",
    "Shakespeare",
    "Mountain",
    "Water",
    "Paris",
    "Sun",
    "Robot",
    "Star"
]

test_cases = [(HOST_PROMPT, GUESSER_PROMPT, topic) for topic in topics]


with ThreadPoolExecutor() as executor:
    futures = [executor.submit(run_game, *args) for args in test_cases]
    results = [future.result() for future in as_completed(futures)]

games_won = 0

for game_played in results:
    if game_played.game_won:
        games_won += 1

print(f"Percentage of games won {100*games_won/(len([topics])+1)}%")
