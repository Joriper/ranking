from db.connection import *
import os,sys

root_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
sys.path.append(root_path)
from python_dp.process.process import Process
from python_dp.process.process import SugamyaProcessor

async def ProcessNextProcessing(**kwargs):
    if kwargs['request_type'] == "queue_sugamay":
        sugmya_process_list =  list(group_accessibility.find({"processed":0}).limit(1))
        if len(sugmya_process_list) > 0:
            await SugamyaProcessor(access_insight=sugmya_process_list[-1]).ProcessSugamya()
        
    elif kwargs['request_type'] =="Yes":
        queue_col =  list(queue_collection.find({"status":"done","processed":0}).limit(1))
        if len(queue_col) > 0:
            await Process(queue_col[-1]).Processor()
    elif kwargs['request_type'] == "NO":
        ig_queue_call =  list(queue_collection.find({"name":kwargs['website_name'],"status":"done","processed":0}).limit(1))
        if len(ig_queue_call) > 0:
            return await Process(ig_queue_call[-1]).Processor()        
    
    elif kwargs['request_type'] == "GROUP":
        ig_queue_call =  list(queue_collection.find({"name":kwargs['website_name'],"status":"done","processed":0}).limit(1))
        if len(ig_queue_call) > 0:
            return await Process(ig_queue_call[-1]).Processor()
    elif kwargs['request_type'] == "NO" and kwargs['site_queue'] != None:
        ig_queue_call =  list(queue_collection.find({"_id":kwargs['site_queue']}).limit(1))
        if len(ig_queue_call) > 0:
            return await Process(ig_queue_call[-1]).Processor()





