from services.content_information.questions.questions import ContentandInformation
import datetime,sys
from db.connection import *
from logger.json_logger import LogEvent


class Group_Texstat:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.sitename =self.site['name']        
        self.uid = kwargs['uid']
        self.data = kwargs['collected']
        self.run_type="single"
        self.clear_info=False
        self.is_grammer_error = False
        self.queue_item = kwargs['queue_item']
        

    async def GroupCaller(self):
        result = []
        site = self.site
        reco_id = str(site['_id'])
        site_id = str(site['site_id'])
        siteurl = str(site['url'])
        try:
            if "https" in siteurl or  "http" in siteurl:
                site_host = siteurl.split("://")[1].split("/")[0]
                content=ContentandInformation(site_url=siteurl,lighthouse=None,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                self.clear_info = await content.clear_and_understandable_info(self.run_type)

                base_store = {
                    "sitename":self.sitename,
                    "site_url":siteurl,
                    "site_id":site_id,
                    "id":reco_id,
                    "processed":0,
                    "clear_info":self.clear_info,                
                    "created_at":str(datetime.datetime.now()),
                    "category":["content_and_information"]

                }
                try:
                    insert_record = group_textstat.insert_one(base_store)
                    result.append(base_store)
                except Exception as error:
                    LogEvent(self.queue_item, "Error in main executor", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
                        
            return result
        except Exception as e:
            LogEvent(self.queue_item, "Error in main executor", LogEvent.ERROR)

        
        



















        





        



        

