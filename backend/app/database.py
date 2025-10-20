from pymongo import MongoClient
from .config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
raw_collection = db["raw_data"]
analysis_collection = db["analysis_results"]

def save_raw(doc):
    res = raw_collection.insert_one(doc)
    return {"inserted_id": str(res.inserted_id)}

def save_analysis(doc):
    res = analysis_collection.insert_one(doc)
    return {"inserted_id": str(res.inserted_id)}
