### Welcome to the 20 Questions Game!

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

#### Future improvements:
- Add logic to ensure the guesser does not ask a repeated question.
- Break down the guesser agent into two agents (one to generate questions and another for guessing the topic).
