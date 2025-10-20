from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .sse_manager import sse_endpoint
import redis
from .config import REDIS_URL, STOP_FLAG_KEY

app = FastAPI(title="Real-time SSE API")

# Allow all origins (useful for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 👈 allow all domains
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

redis_client = redis.Redis.from_url(REDIS_URL)

@app.get("/events")
async def events():
    return sse_endpoint()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/stop_pull")
async def stop_pull():
    redis_client.set(STOP_FLAG_KEY, "1")
    return JSONResponse({"status": "stopped"})

@app.post("/resume_pull")
async def resume_pull():
    redis_client.set(STOP_FLAG_KEY, "0")
    return JSONResponse({"status": "resumed"})
