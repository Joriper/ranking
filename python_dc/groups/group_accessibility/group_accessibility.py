from services.content_information.questions.questions import ContentandInformation
from helpers.urls.urls import GetURL
from helpers.requester.requester import SugamyaHttpRequestHandler
import datetime,time
from db.connection import *
from services.accessibility.questions.questions import *
from logger.json_logger import LogEvent


class Group_Accessibility:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.sitename = self.site['name']
        self.is_grammer_error = False
        self.data = kwargs['collected']
        self.uid = kwargs['uid']
        self.access = False
        self.queue_id = kwargs['queue_id']
        self.queue_item = kwargs['queue_item']
        

    async def GroupCaller(self):
        print("accessibility function call")
        site = self.site
        reco_id = str(site['_id'])
        site_id = str(site['site_id'])
        site_url = str(site['url'])
        try:
            if "https" in site_url or "http" in site_url:
                site_host = site_url.split("://")[1].replace("/", "")
                access = Accessibility(site_host=site_host, site_url=site_url)
                print("calling inside")
                self.access = await access.accessibility_find()
                base_store = {
                    "id": self.queue_id,
                    "sitename": self.sitename,
                    "site_id": site_id,
                    "siteurl": site_url,
                    "accessibility": self.access,
                    "processed": 0
                }
                try:
                    group_accessibility.insert_one(base_store)
                except Exception as error:
                    LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
        except Exception as e:
            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
            
                
