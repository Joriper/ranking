from helpers.requester.requester import *
from helpers.urls.urls import GetURL
from services.mobile_responsive.questions.questions import MobileResponsiveness
from db.connection import *
import datetime,sys
from services.performance_technical.questions.questions import PerformanceandTechnical
from logger.json_logger import LogEvent


class Group_Psi_2:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.gov_respect = False
        self.treemap = False
        self.sitename = self.site['name']
        self.run_type = "single"
        self.codecount = False
        self.request_total =False
        self.code_count = False
        self.first_load_time = False
        self.performance_indicate = False
        self.size_page = False
        self.user_experience = False
        self.meta_description = False
        self.correct_title =  False
        self.logo =  False
        self.loading_exp =  False
        self.origin_loading_exp =  False

        self.metrics = False
        self.data = kwargs['collected']
        self.compatability=False
        self.cache_compress = False
        self.load_time =False
        self.uid = kwargs['uid']
        self.ttfb = False
        self.loading_quicker = False
        self.page_size_load = False
        self.minimize_numbers_requests = False
        self.queue_item = kwargs['queue_item']
                
    
    async def GroupCaller(self):
        result = []
        site = self.site
        reco_id = str(site['_id'])
        sitename =self.site['name']
        site_id = str(site['site_id'])
        siteurl = str(site['url'])
        try:
            if "https" in siteurl or  "http" in siteurl:
                site_host = siteurl.split("://")[1].split("/")[0]
                insight_data = self.data['page_speed']['insights']

                light_house = insight_data['lighthouseResult'] if insight_data.get("lighthouseResult") else []
                result1 = light_house['audits'] if isinstance(light_house,list) == False and light_house.get("audits") else []
                cache_assets = result1['uses-long-cache-ttl']['details']['items'] if isinstance(light_house,list) == False else [] 
                
                performance = PerformanceandTechnical(data=result1,record=insight_data,cache=cache_assets,site_url=siteurl,site_host=site_host,lighthouse=light_house,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                mobile=MobileResponsiveness(site_host=site_host,site_url=siteurl,lighthouse=None,loading_exp=None,random_id=self.uid,sv_m=self.data)

                ######################## Abhishek #####################

                self.ttfb = await performance.TIME_TO_FIRST_BYTE()
                self.loading_quicker = await performance.quicker_loading_page()
                self.page_size_load = await performance.loading_page_size()
                self.minimize_numbers_requests = await performance.minimize_numbers_requests()

                ################## end ################################


                self.metrics = await mobile.fcp_fid_cls()
                caches = await performance.Cacheability()
                error_rate = await performance.ErrorRate()
                third_party_scripts = await performance.ThirdPartyScripts()
                network_latency = await performance.NetworkLatency()
                self.cache_compress = await performance.cache_compression_optimization()           

                ##################### END  ####################################
                base_store ={
                    "sitename":self.sitename,
                    "site_id":site_id,
                    "siteurl":siteurl,
                    "id":reco_id, 
                
                    ############# Abhshek ################

                    "time_to_first_byte": self.ttfb,
                    "quicker_loading_page": self.loading_quicker,
                    "page_size_load": self.page_size_load,
                    "minimize_numbers_requests": self.minimize_numbers_requests,

                    ############## end #################
                    "metrics":self.metrics,
                    "cache":caches,
                    "error_rate":error_rate,
                    "third_party_scripts":third_party_scripts,
                    "network_latency":network_latency,
                    "cache_compress":self.cache_compress,
                    "processed":0,
                    "created_at":str(datetime.datetime.now()),
                    "category":["brand_and_visual_identity","content_and_information","integration_and_service","navigation","performance_and_technical"]

                }
                
                try:
                    group_psi_2.insert_one(base_store)
                except Exception as error:
                    LogEvent(self.queue_item, "Group PSI started", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
            else:
                LogEvent(self.queue_item, "bypassed Group PSI", LogEvent.ERROR)
                
            return result
                        
        except Exception as e:
                LogEvent(self.queue_item, "Group PSI started", LogEvent.ERROR)








        





        



        



