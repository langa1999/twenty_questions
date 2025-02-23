
export interface GameMessage {
  question: string;
  answer: string;
  is_final_guess: boolean;
}

export interface GameState {
  isPlaying: boolean;
  messages: GameMessage[];
  topic?: string;
}
