from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from sse_starlette import EventSourceResponse
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

from backend.models.game_models import GameRequest
from backend.src.run_game import run_dummy_game, run_game

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define a request model to match the frontend request structure
class APIKeyRequest(BaseModel):
    openai_api_key: str  # Define expected JSON key


@app.post("/submit_key")
async def submit_key(request: APIKeyRequest) -> str:
    openai_api_key = request.openai_api_key  # Extract key from JSON request body

    try:
        client = openai.OpenAI(api_key=openai_api_key)

        if client.models.list():
            os.environ['OPENAI_API_KEY'] = openai_api_key
            return "API key validated and saved successfully"

    except openai.APIConnectionError:
        raise HTTPException(
            status_code=404,
            detail="Connection error with OpenAI API"
        )
    except openai.AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="Invalid OpenAI API key"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.post("/start_game")
async def start_game(request: GameRequest):
    return EventSourceResponse(run_game(topic=request.topic))


@app.post("/start_dummy_game")
async def start_dummy_game():
    return EventSourceResponse(run_dummy_game())


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)

