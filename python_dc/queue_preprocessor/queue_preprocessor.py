from db.connection import *
from executor.executor import ExecutorHandler

def PreProcessor(**kwargs):
    col =  list(queue_collection.find({"status":"pending","processed":0,"name":kwargs['name']}).limit(kwargs['limit']))
    for data in col:
        return ExecutorHandler.ExecutorAll(data)
