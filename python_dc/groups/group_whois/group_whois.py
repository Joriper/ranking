from services.branding_visual.questions.questions import BrandingandVisualIdentity
import datetime,sys
from db.connection import *
from logger.json_logger import LogEvent


class Group_Whois:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.sitename = self.site['name']
        self.data  = kwargs['collected']
        self.ownership_info = False
        self.uid = kwargs['uid']
        self.queue_item = kwargs['queue_item']


    async def GroupCaller(self):
        result = []
        site = self.site
        reco_id = str(site['_id'])
        sitename =self.site['name']
        site_id = str(site['site_id'])
        site_url = str(site['url'])
        try:
            if "https" in site_url or  "http" in site_url:
                site_host = site_url.split("://")[1].split("/")[0]
                brand = BrandingandVisualIdentity(site_url=site_url,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)

                self.ownership_info = await brand.ownership_information()
                base_detail = {                
                    "sitename":self.sitename,
                    "site_id":site_id,
                    "site_url":site_url,
                    "id":reco_id,                               
                    "ownership_info":self.ownership_info,
                    "processed":0,
                    "created_at":str(datetime.datetime.now()),
                    "category":["brand_and_visual_identity"]
                }

                print(base_detail)
                try:
                    insert_record = group_whois.insert_one(base_detail)
                    result.append(base_detail)
                except Exception as error:
                    LogEvent(self.queue_item, "STEP ERROR", LogEvent.ERROR)
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)

            return result
        except Exception as e:
            LogEvent(self.queue_item, "STEP ERROR", LogEvent.ERROR)

