
export class GameService {
  private static BASE_URL = 'http://localhost:8000';

  static async submitApiKey(key: string): Promise<Response> {
    const response = await fetch(`${this.BASE_URL}/submit_key`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ openai_api_key: key }),
    });

    if (!response.ok) {
      throw new Error('Invalid API key');
    }

    return response;
  }


  static async startDummyGame(onMessage: (data: string) => void): Promise<void> {
    const response = await fetch(`${this.BASE_URL}/start_dummy_game`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const reader = response.body?.getReader();
    if (!reader) return;

    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });

      // Process each SSE message
      chunk.split("\n").forEach((line) => {
        if (line.startsWith("data: ")) {
          onMessage(line.replace("data: ", "").trim());
        }
      });
    }
  }



  static async startGame(topic: string, onMessage: (data: string) => void): Promise<void> {
    const response = await fetch(`${this.BASE_URL}/start_game`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ topic }),
    });

    const reader = response.body?.getReader();
    if (!reader) return;

    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });

      // Process each SSE message
      chunk.split("\n").forEach((line) => {
        if (line.startsWith("data: ")) {
          onMessage(line.replace("data: ", "").trim());
        }
      });
    }
  }


}