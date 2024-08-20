import sys,bson,datetime,uuid,os,uuid

root_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from python_dp.generator.generate_report import GenerateReport
from python_dc.helpers.urls.urls import GetURL
from python_dc.error.error import Error
from python_dc.helpers.requester.requester import SugamyaHttpRequestHandler
from db.connection import *

class Process:
    def __init__(self,sites):
        self.site = sites
        self.queue_id = str(self.site['_id'])
        self.site_id = str(self.site['site_id'])
        self.site_name = str(self.site['name'])
        self.site_url = str(self.site['url'])
        self.random_id = str(uuid.uuid4())

    async def Processor(self):
        await GenerateReport(sitename=self.site_name,site=self.site).GenerateSiteReport()

class SugamyaProcessor:
    def __init__(self,**kwargs):
        self.access_insight = kwargs['access_insight']
        self.uid = str(uuid.uuid4())

    async def ProcessSugamya(self):
        try:
            running_id = self.access_insight['post_access_data']['id']

            result = SugamyaHttpRequestHandler(type="GET",url=GetURL(type="sugmya_get",web_id=running_id))
            if result['testRun']['status'] == "COMPLETE":
                group_accessibility.update_one({"id":str(self.access_insight['id'])},{"$set":{"processed":1}})
                process_collection.update_one({"queue_id":self.access_insight['id']},{"$set":{"sugmya_access_score":result,"access_id":self.uid}})
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                   
            Error(error,self.__class__.__name__,this_function_name)
