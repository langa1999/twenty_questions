
import React, { useState, useRef, useEffect } from 'react';
import { GameService } from '../services/gameService';
import { GameMessage, GameState } from '../types/game';
import { useToast } from '../hooks/use-toast';
import { Loader } from 'lucide-react';

const Index = () => {
  const [apiKey, setApiKey] = useState('');
  const [topic, setTopic] = useState('');
  const [isValidated, setIsValidated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [leftGame, setLeftGame] = useState<GameState>({
    isPlaying: false,
    messages: [],
    topic: 'car'
  });
  const [rightGame, setRightGame] = useState<GameState>({
    isPlaying: false,
    messages: [],
  });

  const leftEventSourceRef = useRef<EventSource | null>(null);
  const rightEventSourceRef = useRef<EventSource | null>(null);
  const leftMessagesEndRef = useRef<HTMLDivElement>(null);
  const rightMessagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  const scrollToBottom = (ref: React.RefObject<HTMLDivElement>) => {
    ref.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom(leftMessagesEndRef);
  }, [leftGame.messages]);

  useEffect(() => {
    scrollToBottom(rightMessagesEndRef);
  }, [rightGame.messages]);

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

  const startDummyGame = () => {
    if (leftGame.isPlaying) return;

    setLeftGame({ isPlaying: true, messages: [], topic: 'car' });
    
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
          
          setLeftGame(prev => ({
            ...prev,
            messages: [...prev.messages, newMessage],
          }));
        }
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    };

    leftEventSourceRef.current = GameService.startDummyGame(onMessage);
  };

  const startRealGame = () => {
    if (rightGame.isPlaying) return;

    if (!topic.trim()) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please enter a topic",
      });
      return;
    }

    setRightGame({ isPlaying: true, messages: [], topic });
    
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
          
          setRightGame(prev => ({
            ...prev,
            messages: [...prev.messages, newMessage],
          }));
        }
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    };

    rightEventSourceRef.current = GameService.startGame(topic, onMessage);
  };

  const resetLeftGame = () => {
    leftEventSourceRef.current?.close();
    setLeftGame({ isPlaying: false, messages: [], topic: 'car' });
  };

  const resetRightGame = () => {
    rightEventSourceRef.current?.close();
    setRightGame({ isPlaying: false, messages: [] });
    setTopic('');
  };

  return (
    <div className="split-layout">
      {/* Left Side - Dummy Game */}
      <section className="game-section">
        <div className="card mb-4">
          <h2 className="text-2xl font-semibold mb-4">Try Demo Game</h2>
          <p className="text-muted-foreground mb-4">
            Play a demo game about cars without an API key
          </p>
          {!leftGame.isPlaying ? (
            <button onClick={startDummyGame} className="button-secondary">
              Start Demo Game
            </button>
          ) : (
            <button onClick={resetLeftGame} className="button-accent">
              Reset Demo Game
            </button>
          )}
        </div>

        {leftGame.isPlaying && (
          <div className="card">
            <h3 className="text-lg font-medium mb-4">
              Demo Game: {leftGame.topic}
            </h3>
            <div className="message-container">
              {leftGame.messages.map((msg, index) => (
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
              <div ref={leftMessagesEndRef} />
            </div>
          </div>
        )}
      </section>

      {/* Right Side - Real Game */}
      <section className="game-section">
        {!isValidated ? (
          <div className="card">
            <h2 className="text-3xl font-bold mb-6 text-primary">Play Real Game</h2>
            <form onSubmit={handleApiSubmit} className="space-y-6">
              <div className="space-y-6">
                <div className="input-container">
                  <label htmlFor="apiKey" className="block text-lg font-semibold mb-2">
                    Enter your API Key
                  </label>
                  <input
                    id="apiKey"
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    className="game-input text-lg"
                    placeholder="sk-..."
                    required
                  />
                </div>
                <div className="input-container">
                  <label htmlFor="initialTopic" className="block text-lg font-semibold mb-2">
                    Enter a Topic
                  </label>
                  <input
                    id="initialTopic"
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    className="game-input text-lg"
                    placeholder="What should I guess?"
                  />
                </div>
              </div>
              <button type="submit" className="button text-xl" disabled={isLoading}>
                {isLoading ? (
                  <Loader className="animate-spin h-6 w-6 mx-auto" />
                ) : (
                  'Start Playing!'
                )}
              </button>
            </form>
          </div>
        ) : (
          <>
            <div className="card mb-4">
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
                  disabled={rightGame.isPlaying}
                />
              </div>
              {!rightGame.isPlaying ? (
                <button onClick={startRealGame} className="button mt-4">
                  Start Game
                </button>
              ) : (
                <button onClick={resetRightGame} className="button-accent mt-4">
                  Reset Game
                </button>
              )}
            </div>

            {rightGame.isPlaying && (
              <div className="card">
                <h3 className="text-lg font-medium mb-4">
                  Game in progress: {rightGame.topic}
                </h3>
                <div className="message-container">
                  {rightGame.messages.map((msg, index) => (
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
                  <div ref={rightMessagesEndRef} />
                </div>
              </div>
            )}
          </>
        )}
      </section>
    </div>
  );
};

export default Index;
