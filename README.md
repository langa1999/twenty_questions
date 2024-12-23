### Welcome to the 20 Questions Game!
The 20 Questions game is a guessing game where one player, the "guest," attempts to deduce an unknown object, concept, or entity by asking up to 20 yes-or-no questions. The other player, the "host," provides yes/no answers to help guide the guest toward the correct answer.

When played between two large language models, the roles are divided as follows:

Guest Agent: The guest model generates strategic yes-or-no questions based on prior responses to systematically eliminate incorrect options and converge on the answer.
Host Agent: The host model starts with a preselected "answer" and evaluates each question posed by the guest, responding truthfully with "yes," "no," or occasionally "unsure," depending on the specificity of the query.

#### Setup Instructions:

1. **Configure the `.env` File**  
   - Add your OpenAI API key 


2. **Run the Game**  
   Execute the game once with the default topic `"car"` by running:  
   ```bash
   cd src
   python main.py
   ```  
   Execute a test set with multiple topics:  
   ```bash
   cd tests
   python test_topics.py
   ```  

### Future improvements

For the guesser agent:
- Add logic to ensure the guesser does not ask repeated questions.
- Break down the guesser agent into two agents (one to generate questions and another for guessing the topic).
- Improve prompting significantly: with few-shots or suggesting a list of possible questions and suggesting pros/cons of each.
- What happens when we prompt the agent to adopt the mentality of binary search? What is the best way to slice the universe of possibilities into two options (Yes/No)
- I would love to explore the idea of rewards for good questions asked. Maybe this is more experimental. 

For the host agent: 
- I would  improve the prompting to ensure it concedes the game when the guesser has made a reasonably close guess, albeit not perfect. 
- We could also create a new critic agent that holds all the information and can assess whether the guesser has gotten close enough to end the game.

For evaluation:
- I would spend a lot of time working on building a good testing framework. We want to test different prompts and topics and measure the associated success rate. 
- Thinking beyond this, I would like to also make the code more modular such that agents themselves can best tested (beyond just their system prompt). For example testing agents with search tools?  
- The main topic I would explore is calculating a similarity score after each question. I want to quantify how close each guess is to topic. This will be particularly useful when the guesser runs out of questions in the game, so we know how close it came to guessing the answer.
- I don't know what packages are available to create such a score, but we could start by calculating the distance between the embeddings of the topic and the guess. 
