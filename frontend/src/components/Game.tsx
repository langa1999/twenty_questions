
import React, { useState, useRef, useEffect } from 'react';
import { GameService } from '../services/gameService';
import { GameMessage, GameState } from '../types/game';
import { useToast } from '../hooks/use-toast';
import { Loader } from 'lucide-react';

const Game = () => {
  const [apiKey, setApiKey] = useState('');
  const [topic, setTopic] = useState('');
  const [isValidated, setIsValidated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [gameState, setGameState] = useState<GameState>({
    isPlaying: false,
    messages: [],
  });
  
  const eventSourceRef = useRef<EventSource | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [gameState.messages]);

  const handleApiSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      await GameService.submitApiKey(apiKey);
      setIsValidated(true);
      toast({
        title: "Success",
        description: "API key validated successfully",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Invalid API key",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleGameStart = (isDummy: boolean = false) => {
    if (gameState.isPlaying) return;

    const startGame = () => {
      setGameState({ isPlaying: true, messages: [], topic: isDummy ? 'car' : topic });
      
      const onMessage = (data: string) => {
        try {
          const match = data.match(/question='([^']+)' answer='([^']+)' is_final_guess=(true|false)/);
          if (match) {
            const [, question, answer, is_final_guess] = match;
            const newMessage: GameMessage = {
              question,
              answer,
              is_final_guess: is_final_guess === 'true',
            };
            
            setGameState(prev => ({
              ...prev,
              messages: [...prev.messages, newMessage],
            }));
          }
        } catch (error) {
          console.error('Error parsing message:', error);
        }
      };

      if (isDummy) {
        eventSourceRef.current = GameService.startDummyGame(onMessage);
      } else {
        eventSourceRef.current = GameService.startGame(topic, onMessage);
      }
    };

    if (!isDummy && !topic.trim()) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please enter a topic",
      });
      return;
    }

    startGame();
  };

  const resetGame = () => {
    eventSourceRef.current?.close();
    setGameState({ isPlaying: false, messages: [] });
    setTopic('');
  };

  return (
    <div className="game-container">
      {!isValidated ? (
        <div className="card">
          <h2 className="text-2xl font-semibold mb-4">Welcome to the Game</h2>
          <form onSubmit={handleApiSubmit} className="space-y-4">
            <div className="input-container">
              <label htmlFor="apiKey" className="block text-sm font-medium">
                Enter your API Key
              </label>
              <input
                id="apiKey"
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="game-input"
                placeholder="sk-..."
                required
              />
            </div>
            <button type="submit" className="button w-full" disabled={isLoading}>
              {isLoading ? (
                <Loader className="animate-spin h-5 w-5 mx-auto" />
              ) : (
                'Validate API Key'
              )}
            </button>
          </form>
          <div className="mt-4">
            <button
              onClick={() => handleGameStart(true)}
              className="w-full p-3 text-center text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              or try a demo game without API key
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="card">
            <div className="input-container">
              <label htmlFor="topic" className="block text-sm font-medium">
                Enter a Topic
              </label>
              <input
                id="topic"
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="game-input"
                placeholder="Enter any topic..."
                disabled={gameState.isPlaying}
              />
            </div>
            {!gameState.isPlaying ? (
              <button
                onClick={() => handleGameStart(false)}
                className="button w-full mt-4"
              >
                Start Game
              </button>
            ) : (
              <button onClick={resetGame} className="button w-full mt-4">
                Reset Game
              </button>
            )}
          </div>

          {gameState.isPlaying && (
            <div className="card">
              <h3 className="text-lg font-medium mb-4">
                Game in progress: {gameState.topic}
              </h3>
              <div className="message-container">
                {gameState.messages.map((msg, index) => (
                  <div key={index} className="message">
                    <p className="font-medium">Q: {msg.question}</p>
                    <p className="text-muted-foreground">A: {msg.answer}</p>
                    {msg.is_final_guess && (
                      <p className="text-sm text-primary mt-2 font-medium">
                        Final Guess!
                      </p>
                    )}
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Game;
