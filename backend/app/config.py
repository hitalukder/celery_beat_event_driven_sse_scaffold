import os
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/")
DB_NAME = os.getenv("DB_NAME", "realtime_data")
PULL_INTERVAL = float(os.getenv("PULL_INTERVAL", "2.0"))  # seconds
API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/todos/")  # example
STOP_FLAG_KEY = os.getenv("STOP_FLAG_KEY", "STOP_FLAG_KEY")  # stored in redis
