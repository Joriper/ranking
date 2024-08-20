from services.content_information.questions.questions import ContentandInformation
import datetime,sys
from db.connection import *
from logger.json_logger import LogEvent


class Group_Grammer:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.sitename = self.site['name']
        self.is_grammer_error = False
        self.run_type = "single"
        self.data = kwargs['collected']
        self.uid = kwargs['uid']
        self.queue_item = kwargs['queue_item']
        
    
    async def GroupCaller(self):
        result = []
        site = self.site
        reco_id = str(site['_id'])
        site_id = str(site['site_id'])
        site_url = str(site['url'])
        try:
            if "https" in site_url or  "http" in site_url:
                site_host = site_url.split("://")[1].split("/")[0]
                content=ContentandInformation(site_url=site_url,lighthouse=None,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                self.is_grammer_error = await content.grammer_mistake(self.run_type)
            
                base_detail = {                
                    "sitename":self.sitename,
                    "site_id":site_id,
                    "site_url":site_url,
                    "id":reco_id,                               
                    "is_grammer_error":self.is_grammer_error,
                    "processed":0,
                    "created_at":str(datetime.datetime.now()),
                    "category":["content_and_information"]

                }
                result.append(base_detail)
                try:
                    insert_record = group_grammer.insert_one(base_detail)
                except Exception as error:
                    LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
                    
            else:
                LogEvent(self.queue_item, "bypassed Group PSI", LogEvent.ERROR)
            return result
        except Exception as e:
                LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
            









        



        

