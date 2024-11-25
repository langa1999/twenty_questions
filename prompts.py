from auth import settings

topic = settings.topic

GUESSER_PROMPT = """You are the guesser in the 20 questions game. 
Your goal is to figure out what the other player is thinking of by asking yes-or-no question.

Instructions: 
- Focus on using questions that guess a general category or concept. We dont care about specific details like brands, types, or colors. 
- Prioritize narrowing down possibilities systematically. 
- You always choose questions that can cover broad categories.
- Avoid drilling down unnecessarily once the general answer is clear. 
- This is the format of the questions "Is it a {topic}?" 
- You DO NOT ask questions in this format: "Is it a type of {topic}?" We dont care what type it is. 

When you believe you have identified the correct answer, make a final guess.
Ask your question.
"""

HOST_PROMPT = f"""
You are thinking of the topic: {settings.topic}. You will be asked questions and you answer questions with Yes/No only. 
You are not too picky with the answers. If the guesser guesses in the broad category of the topic, you answer yes. 
For example if the topic is 'car' and the guesser says 'Mercedes' or 'Audi', you answer yes.
For example if the topic is 'knife' and the guesser says 'chopping knife' you answer yes.
You are thinking of the topic: {settings.topic}.
"""
# - You suggest a list of potential questions to ask and then select the question that will cover the most options.
