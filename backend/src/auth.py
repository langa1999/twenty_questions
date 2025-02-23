from openai import OpenAI, LengthFinishReasonError
from openai import AsyncOpenAI
from backend.settings import Settings

settings = Settings()


def get_client():
    client = OpenAI()
    return client


def get_async_client():
    async_client = AsyncOpenAI()
    return async_client


async def get_chat_completion(
    max_tokens: int,
    context: list[dict],
    temperature: int,
    response_format
):
    try:
        client = get_async_client()
        response = await client.beta.chat.completions.parse(
            model=settings.model,
            messages=context,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_format,
        )
        return response
    except LengthFinishReasonError as e:
        max_tokens += 100
        print(f">>> Token limit increased to {max_tokens}")
        return await get_chat_completion(context, response_format)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
