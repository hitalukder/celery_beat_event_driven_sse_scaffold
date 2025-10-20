import asyncio
import asyncio
from redis.asyncio import Redis
from fastapi.responses import StreamingResponse
from .config import REDIS_URL

async def event_generator():
    redis = Redis.from_url(REDIS_URL)
    pubsub = redis.pubsub()
    await pubsub.subscribe("sse_channel")
    try:
        async for message in pubsub.listen():
            print("*"*100)
            print(f"message type: {message}")
            print("*"*100)
            if message["type"] == "message":
                yield f"data: {message['data'].decode()}\n\n"
    finally:
        await pubsub.unsubscribe("sse_channel")

def sse_endpoint():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
