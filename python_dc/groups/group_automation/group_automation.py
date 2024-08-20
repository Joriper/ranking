from helpers.requester.requester import HttpRequestHandler
from services.integration_service.questions.questions import IntegrationandService
from services.branding_visual.questions.questions import BrandingandVisualIdentity
from services.performance_technical.questions.questions import PerformanceandTechnical
from services.mobile_responsive.questions.questions import MobileResponsiveness
from services.content_information.questions.questions import ContentandInformation
from services.inter_engagement.questions.questions import InteractivityandEngagement
from services.navigation.questions.questions import Navigation
import datetime,sys
from db.connection import *
from logger.json_logger import LogEvent


class Group_Automation:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.about_page = False
        self.contact_page = False
        self.flagship = False
        self.download_excel_pdf = False
        self.is_opportunity=False
        self.online_trans = False
        self.sitename =self.site['name']        

        self.backlinks = False
        self.is_faq = False
        self.uid = kwargs['uid']
        self.is_bread_crumb =  False
        self.nav_across_site = False
        self.gov_service=False
        self.home_linked = False
        self.pool_consult = False
        self.data = kwargs['collected']
        self.static_assets = False
        self.queue_item = kwargs['queue_item']
        
    
    async def GroupCaller(self):
        site = self.site
        reco_id = str(site['_id'])
        result=[]
        site_id = str(site['site_id'])
        siteurl = str(site['url'])
        try:
            if "https" in siteurl or  "http" in siteurl:
                site_host = siteurl.split("://")[1].split("/")[0]
                integration = IntegrationandService(site_host=site_host,random_id=self.uid,site_url=siteurl,sv_m=self.data)

                inter = InteractivityandEngagement(site_host=site_host,random_id=self.uid,site_url=siteurl,sv_m=self.data, queue_item=self.queue_item)
                performance = PerformanceandTechnical(data=None,record=None,cache=None,site_url=siteurl,site_host=site_host,lighthouse=None,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                mobile = MobileResponsiveness(site_host=site_host,random_id=self.uid,site_url=siteurl,lighthouse=None,sv_m=self.data)
                content=ContentandInformation(site_url=siteurl,lighthouse=None,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)

                self.real_time_chatbot = await inter.is_realtime_chatbot()
                print("called")
                self.easy_signup = await inter.is_easy_signup_email()
                print("Called1")
                comptability = await performance.compatability()
                print("called2")
                self.media_query = await mobile.MediaQuery()
                print("called3")
                # self.gov_service = await integration.avail_government_service()
                base_store = {
                    "sitename":self.sitename,
                    "site_id":site_id,
                    "site_url":siteurl,
                    "id":reco_id,
                    "real_time_chatbot":self.real_time_chatbot,
                    "easy_signup":self.easy_signup,
                    # "gov_service":self.gov_service,
                    "compatability":comptability,
                    "media_query":self.media_query,
                    "processed":0,
                    "created_at":str(datetime.datetime.now()),
                    "category":["inter_engagement","mobile_responsive","performance_and_technical"]
                }
                try:
                    group_automation.insert_one(base_store)
                    result.append(base_store)
                except Exception as error:  
                    import pdb;pdb.set_trace()
                    LogEvent(self.queue_item, "STEP ERROR", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
        except Exception as e:
            import pdb;pdb.set_trace()
            LogEvent(self.queue_item, "STEP ERROR", LogEvent.ERROR)



















        





        



        

