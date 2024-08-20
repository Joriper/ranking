from db.connection import *
import datetime,time,sys
from executor.executor import ExecutorHandler,GroupCallHandler,SugamyaHandler,UpdateGroup

async def ProcessNext(**kwargs):
    if kwargs['request_type'] =="Yes":
        working_col =  list(queue_collection.find({"status":"working"}))

        if len(working_col) == 0:
            for limits in list(nic_settings.find({})):
                try:
                    if isinstance(limits['data'][0]['value'],int)== True:
                        site_check =  list(queue_collection.find({"status":"pending","first_report":True}).limit(limits['data'][0]['value']))

                        if len(site_check) > 0:
                            pending_col = site_check
                        else:
                            current = datetime.datetime.now().strftime("%d/%m/%Y")
                            pending_col = []
                            check_site = list(queue_collection.find({"status":"pending","first_report":False}))
                            for all_sites in check_site:                            
                                get_date = all_sites['execution_date']
                                newdate1 = time.strptime(str(get_date), "%d/%m/%Y")
                                newdate2 = time.strptime(str(current), "%d/%m/%Y")
                                if newdate2 > newdate1:
                                    pending_col.append(all_sites)

                            pending_col = pending_col[0:limits['data'][0]['value']]

                        if len(pending_col) > 0:
                            for queue_thread in pending_col:
                                if queue_thread['type'] == "full":
                                    await ExecutorHandler(queue_thread).Executor()
                                else:
                                    await GroupCallHandler().GroupHandler(None,"Group_Psi","pending","partial",web=[queue_thread])
                except Exception as error:
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,"ProcessNext",this_function_name)                    
                
            if len(list(nic_settings.find({}))) == 0:
                tmp_list = list(queue_collection.find({"status":"pending"}).limit(1))
                try:
                    await ExecutorHandler(tmp_list[-1]).Executor()
                except Exception as error:
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,"ProcessNext",this_function_name)
        else:            
            for current_site in working_col:
                current_time = datetime.datetime.now()
                start_date = current_site['start_at']
                date_time_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S.%f')
                diff_min = current_time - date_time_obj
                get_minutes = round(diff_min.total_seconds()/60)
                if get_minutes >= 60:
                    queue_collection.update_one({"_id":current_site['_id']},{"$set":{"status":"process_timeout"}})
                sys.exit(1)            


    elif kwargs['request_type'] == "NO":
        #ig_queue_call =  list(queue_collection.find({"name":kwargs['website_name'],"status":"pending","processed":0}).limit(1))
        #if len(ig_queue_call) > 0
        return await ExecutorHandler(kwargs['web']).Executor()
        
    elif kwargs['request_type'] == "GROUP" and kwargs['group_name'] !=None and kwargs['website'] !=None:
        return await GroupCallHandler().GroupHandler(kwargs['website'],kwargs['group_name'])
    
    elif kwargs['request_type'] == "ps_web_collect_group_process" and kwargs['website_name'] !=None:
        return await GroupCallHandler().GroupHandler(kwargs['website_name'],"Group_Psi","pending","partial")
    
    elif kwargs['request_type'] == "update" and kwargs['update_id'] != None and kwargs['group_name'] != None and kwargs['keyname'] !=None and kwargs['group_key'] != None:
        print("CCC")
        return await UpdateGroup().UpdateGroupHandler(update_id=kwargs['update_id'],group_name=kwargs['group_name'],keyname=kwargs['keyname'],group_key=kwargs['group_key'])
    return


async def SubamyaQueueNext(**kwargs):
    if kwargs['request_type'] == "SUGAMYA_QUEUE":
        work_sugamya_col =  list(queue_sugamya.find({"status":"working","processed":0}))
        if len(work_sugamya_col) == 0:
            sugamya_col =  list(queue_sugamya.find({"status":"pending","processed":0}).limit(1))
            if len(sugamya_col) > 0:
                return await SugamyaHandler(sugamya_col[-1]).SugamyaExecutor()
            
  




