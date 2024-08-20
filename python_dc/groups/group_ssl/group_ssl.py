from helpers.requester.requester import HttpRequestHandler
from services.security_privacy.questions.questions import SecurityPrivacy
import datetime,sys
from db.connection import *
from logger.json_logger import LogEvent


class Group_SSL:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.is_ssl = False
        self.data = kwargs['collected']
        self.sitename =self.site['name']
        self.run_type = "single"
        self.uid = kwargs['uid']
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
                security = SecurityPrivacy(site_host=site_host,site_url=siteurl,data=self.data)
                self.is_ssl = await security.IsSSL()
                security_header = await security.Security_Headers()
                captch = await security.CaptchDetect()
                cookie = await security.Cookie_Policy(self.run_type)
                access_auth = await security.AccessAuthorization()
                secure_practice = await security.SecureDevelopmentPractice()

                base_store = {
                    "sitename":self.sitename,
                    "site_url":siteurl,
                    "site_id":site_id,
                    "id":reco_id,
                    "ssl_info":self.is_ssl,
                    "security_headers":security_header,
                    "strong_encryption":self.is_ssl['ssl_info']['strong_encryption'],
                    "captch":captch,
                    "cookie":cookie,
                    "access_auth":access_auth,                
                    "secure_development_practice":secure_practice,
                    "processed":0,
                    "created_at":str(datetime.datetime.now()),
                    "category":["security_and_privacy"]

                }

                print(base_store)
                try:
                    insert_record = group_ssl.insert_one(base_store)
                    result.append(base_store)
                except Exception as error:
                    LogEvent(self.queue_item, "Error in main executor", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
                        
            return result
        except Exception as e:
            LogEvent(self.queue_item, "Error in main executor", LogEvent.ERROR)

        
        



















        





        



        

