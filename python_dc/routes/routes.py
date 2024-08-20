from typing import Any, List
import json,sys,datetime,os,threading
from db.connection import *
from fastapi.staticfiles import StaticFiles
from fastapi import Request, Query, HTTPException
from multiprocessing import Process
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter,BackgroundTasks
import asyncio
from Queue.queue import ProcessNext
from models import *
from settings import JSON_LOGS_PATH



root_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
sys.path.append(root_path)
from python_dp.Queues.queue import ProcessNextProcessing
app_nic = APIRouter()

async def CustomExecutor(kwargs):
    await asyncio.sleep(5)
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

############################################ Routes FOR DATA COLLECTION #############################
###### QUEUE DATA COLLECTION ROUTE#########

@app_nic.get("/api/collect/queue",response_model=FullGroups)
async def queue_get():
    try:
        executor = CustomExecutor(function_name="PROCESS_NEXT_IN_QUEUE",request="Yes",type="collect")
        asyncio.create_task(executor)
        await asyncio.sleep(0)
        return {"status":200,"message":"Queue EXECUTED","error":0,"site":"False"}
    except  Exception as error:
        return {"status":200,"message":"Failed to Execute Queue","error":1,"site":"False"},

##### END #################################

###### SPECIFIC WEBSITE DATA COLLECTION ROUTE#########
@app_nic.get("/api/collect/{website_name}",response_model=BasicGroup)
async def group_get(website_name:str):
    try:
        executor = CustomExecutor(function_name="EXECUTOR",request="NO",website=website_name,type="collect")
        asyncio.create_task(executor)
        await asyncio.sleep(0)
        return {"status":200,"message":"EXECUTED","error":0,"site":str(website_name)}
    except Exception as error:
        return {"status":400,"message":"Failed to Execute","error":1,"site":str(website_name)}

####### END ###########################################

####### GROUP SPECIFIC ROUTE FOR WEBSITE ##############
@app_nic.get("/api/collect/{group_name}/{website_name}",response_model=BasicGroup)
async def full_get(website_name:str,group_name:str):
    try:
        executor = CustomExecutor(group_name=group_name,request="GROUP",website=website_name,type="collect")
        asyncio.create_task(executor)
        await asyncio.sleep(0)
        return {"status":200,"message":"EXECUTED","error":0,"site":str(website_name)}
    except Exception as error:
        return {"status":400,"message":"Failed to Execute","error":1,"site":str(website_name)}


########### END ##########################################



########################################### ROUTES FOR DATA PROCESSING ##################################

######### DIRECT PROCESSING ####################
@app_nic.get("/api/process/{website_name}/",response_model=BasicGroup)
async def web_process(website_name:str):
    result = []
    try:
        executor = CustomExecutor(type="web_full_process",website=website_name)
        asyncio.create_task(executor)
        await asyncio.sleep(0)
        return {"status":200,"message":"PROCESSING","error":0,"site":str(website_name)}
    except:
        return {"status":400,"message":"Failed to process","error":1,"site":str(website_name)}

###################### END #######################
@app_nic.get("/api/process/group/{group_name}/{website_name}/",response_model=BasicGroup)
async def web_process(website_name:str,group_name:str):
    try:
        executor = CustomExecutor(type="web_group_process",group_name=group_name,website=website_name)
        asyncio.create_task(executor)
        await asyncio.sleep(0)
        return {"status":200,"message":"PROCESSING","error":0,"site":str(website_name)}
    except:
        return {"status":400,"message":"Failed to process","error":1,"site":str(website_name)}        

#################### BOTH DATA COLLECTION AND PROCESSING #######################
@app_nic.get("/api/collect_process/{website_name}",response_model=BothGroup)
async def collect_process(website_name:str):
    try:
        def between_callback(args):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(CustomExecutor(args))
            loop.close()

        site_info =  list(queue_collection.find({"name":website_name,"status":"pending","processed":0,"type":"full"}).limit(1))
        if len(site_info) > 0:
            _thread = threading.Thread(target=between_callback, args=({"type":"collect_process","website":website_name,"web":site_info[-1]},))
            _thread.start()
            _thread.join()
            return {"status":200,"message":"PROCESSING_COLLECTION","error":0,"type":"full","site":str(website_name),"queue_id":str(site_info[-1]['_id'])}
        else:
            get_new_site = list(queue_collection.find({"name":website_name,"type":"full"}).limit(1))
            del get_new_site[-1]['_id']
            get_new_site[-1]['status']="pending"
            get_new_site[-1]['processed']=0
            get_new_site[-1]['created_at']=datetime.datetime.now()
            get_new_site[-1]['updated_at']=datetime.datetime.now()
            queue_collection.insert_one(get_new_site[-1])

            _thread = threading.Thread(target=between_callback, args=({"type":"collect_process","website":website_name,"web":get_new_site[-1]},))
            _thread.start()

            return {"status":200,"message":"PROCESSING_COLLECTION_VIA_GENERATED","error":0,"type":"full","site":str(website_name),"queue_id":str(get_new_site[-1]['_id'])}
            #return {"status":404,"message":"Failed to process","error":1,"type":"full","site":str(website_name),"queue_id":"Not found"}
    except Exception as error:
        return {"status":400,"message":"Failed to process","error":1,"site":str(website_name),"type":"full","queue_id":"NO"}

app_nic.mount("/static", StaticFiles(directory=os.path.dirname(os.path.normpath(os.getcwd()))+"/python_dc/screenshot"), name="static")

################## Google pagespeed Collection and processing ######################
@app_nic.get("/user/api/v1/ps_partial/{website_name}",response_model=BothGroup)
def google_insight(website_name:str):
    try:
        def Threader():
            site_info =  list(queue_collection.find({"name":website_name,"status":"pending","processed":0}).limit(1))
            print(site_info)
            if len(site_info) > 0:        
                asyncio.create_task(CustomExecutor(type="ps_web_collect_group_process",website=website_name))
                return site_info
            else:
                return False

        get_data = Threader()
        if isinstance(get_data,list) ==  True:
            return {"status":200,"message":"PS_PROCESSING_COLLECT","error":0,"site":str(website_name),"type":"partial","queue_id":str(get_data[-1]['_id'])}
        else:
            return {"status":404,"message":"Site Not Found","error":0,"site":str(website_name),"type":"partial","queue_id":"Not found"}
            
    except Exception as error:
        print("Called",error)
        return {"status":400,"message":"Failed to process","error":1,"site":str(website_name),"type":"partial","queue_id":"NO"}



@app_nic.get("/api/v1/logs_list/",response_model=List[str]) 
def logs_list(date: str = Query("", description="Date in YYYY-MM-DD format")):
    try:
        if not os.path.exists(JSON_LOGS_PATH):
            return []

        # Get the list of files starting with the provided date
        matching_files = [
            f for f in os.listdir(JSON_LOGS_PATH) 
            if os.path.isfile(os.path.join(JSON_LOGS_PATH, f)) and f.startswith(date)
        ]
        return matching_files
    except Exception as e:
        # Handle exceptions (e.g., directory access issues)
        # return {"error": str(e)}
        raise HTTPException(status_code=500, detail="an error occured while processing request")
    
    

@app_nic.get("/api/v1/log_data/",) #response_model=BothGroup)
def log_data(file_name: str = Query("Provide Log File Name", description="File Name example - 2024-05-22 11:35:55.916000-664dd89bb83a5eabd0199861-chatgpt.com")):
    file_path = os.path.join(JSON_LOGS_PATH, file_name)
    print(file_path)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                data = file.read().strip()
                data = '['+ data[:-1] + ']'
                return json.loads(data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="File not found")
