import os,sys
import time
from Queue.queue import ProcessNext
root_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
sys.path.append(root_path)
from python_dp.Queues.queue import ProcessNextProcessing



async def CustomExecutor(**kwargs):
    if kwargs['type']  == "collect" and kwargs['function_name'] == "PROCESS_NEXT_IN_QUEUE"  and kwargs['request'] == "Yes":
        await ProcessNext(function=kwargs['function_name'],request_type=kwargs['request'])
    elif kwargs['type']  == "collect" and kwargs['function_name'] == "EXECUTOR" and kwargs['website'] != None and kwargs['request'] == "NO":
        await ProcessNext(function=kwargs['function_name'],request_type=kwargs['request'],website_name=str(kwargs['website']))

    elif kwargs['type'] == "collect" and  kwargs['group_name'] !=None and kwargs['website'] !=None and kwargs['request'] == "GROUP":
        await ProcessNext(group_name=kwargs['group_name'],request_type=kwargs['request'],website_name=str(kwargs['website']))

    elif kwargs['type'] == "web_full_process":
        await ProcessNextProcessing(request_type="NO",website_name=kwargs['website'])

    elif kwargs['type'] == "collect_process":
        queue_id = await ProcessNext(function="EXECUTOR",request_type="NO",website_name=str(kwargs['website']),web=kwargs['web'])
        await ProcessNextProcessing(request_type="NO",website_name=kwargs['website'],site_queue=queue_id)

    elif kwargs['type'] == "ps_web_collect_group_process":
        queue_id = await ProcessNext(function="EXECUTOR",request_type="ps_web_collect_group_process",website_name=str(kwargs['website']))
        await ProcessNextProcessing(request_type="NO",website_name=kwargs['website'],site_queue=queue_id)