import os
import random
import requests
from .celery_app import celery_app
from .database import save_raw, save_analysis
from .config import API_URL, STOP_FLAG_KEY, REDIS_URL
import redis

# Redis client for STOP flag and pub/sub
redis_client = redis.Redis.from_url(REDIS_URL)

@celery_app.task(name="app.tasks.pull_data_task")
def pull_data_task():
    # Check stop flag
    if redis_client.get(STOP_FLAG_KEY) == b"1":
        print("*"*100)
        print(f"Stopped pulling...")
        print("*"*100)
        return {"status": "stopped"}

    user_id = random.randint(1, 100)
    API_USER = f"{API_URL}{user_id}"

    try:
        r = requests.get(API_USER, timeout=5)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        redis_client.publish("sse_channel", f"pull_error:{str(e)}")
        return {"error": str(e)}

    saved = save_raw({"data": data})
    
    # threshold example
    if user_id % 2 == 0:
        analyze_data_task.delay(user_id)

    redis_client.publish("sse_channel", f"pulled:{user_id}")
    return {"inserted_id": saved["inserted_id"]}


@celery_app.task(name="app.tasks.analyze_data_task")
def analyze_data_task(record_id):
    result = {"record_id": str(record_id), "result": "analysis_done"}
    saved = save_analysis(result)
    redis_client.publish("sse_channel", f"analyzed:{record_id}")
    return {"record_id": result["record_id"], "db_inserted_id": saved["inserted_id"]}
