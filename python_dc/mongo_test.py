import os
from pymongo import MongoClient
print(f"MONGO_CONNECTION environment variable value: {os.environ.get('MONGO_CONNECTION')}")
connection = MongoClient(os.environ['MONGO_CONNECTION'])
