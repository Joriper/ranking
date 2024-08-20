from helpers.requester.requester import *
from helpers.urls.urls import GetURL
from services.branding_visual.questions.questions import BrandingandVisualIdentity
from services.content_information.questions.questions import ContentandInformation
from services.navigation.questions.questions import Navigation
from services.mobile_responsive.questions.questions import MobileResponsiveness
from db.connection import *
import datetime,sys
from services.performance_technical.questions.questions import PerformanceandTechnical
from logger.json_logger import LogEvent


class Group_Psi:
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
        self.green_metrics = False
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
        site = self.site
        reco_id = str(site['_id'])
        sitename =self.site['name']
        site_id = str(site['site_id'])
        siteurl = str(site['url'])
        try:
            if "https" in siteurl or  "http" in siteurl:
                site_host = siteurl.split("://")[1].split("/")[0]
                insight_data = self.data['page_speed']['insights']
                access_data = self.data['page_speed']['access'] 

                light_house = insight_data['lighthouseResult'] if insight_data.get("lighthouseResult") else []
                result1 = light_house['audits'] if isinstance(light_house,list) == False and light_house.get("audits") else []
                cache_assets = result1['uses-long-cache-ttl']['details']['items'] if isinstance(light_house,list) == False else [] 
                
                performance = PerformanceandTechnical(data=result1,record=insight_data,cache=cache_assets,site_url=siteurl,site_host=site_host,lighthouse=light_house,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                brand = BrandingandVisualIdentity(site_host=site_host,random_id=self.uid,site_url=siteurl,sv_m=self.data, queue_item=self.queue_item)
                content=ContentandInformation(site_url=siteurl,lighthouse=light_house,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                navigation=Navigation(site_url=siteurl,site_host=site_host,lighthouse=light_house,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)

                mobile=MobileResponsiveness(site_url=siteurl,site_host=site_host,lighthouse=light_house,random_id=self.uid,sv_m=self.data)


                LogEvent(self.queue_item, "Page size", LogEvent.INFO)
                self.size_page = await performance.page_sizes()
                
                LogEvent(self.queue_item, "Code count", LogEvent.INFO)

                self.code_count = await navigation.code_count()

                pg_shot = []
                ################# Only for partial module ####################
                
                
                LogEvent(self.queue_item, "Total Request", LogEvent.INFO)
                self.request_total =await navigation.total_request()
                
                LogEvent(self.queue_item, "Load times", LogEvent.INFO)
                self.load_time  = await performance.load_times()            
                
                LogEvent(self.queue_item, "Tree map", LogEvent.INFO)
                self.treemap = await content.is_tree_map()
                
                LogEvent(self.queue_item, "Performace indicator", LogEvent.INFO)
                self.performance_indicate =  await content.performance_indicator()

                LogEvent(self.queue_item, "Meta description", LogEvent.INFO)                
                self.meta_description = await brand.MetaDescription(self.run_type)
                
                LogEvent(self.queue_item, "Correct Title", LogEvent.INFO)
                self.correct_title = await navigation.correct_title(self.run_type)
                
                LogEvent(self.queue_item, "Website Logo", LogEvent.INFO)
                self.logo = await brand.website_logo(self.run_type)
                
                LogEvent(self.queue_item, "Page speed API", LogEvent.INFO)
                self.loading_exp = insight_data['loadingExperience'] if insight_data.get("loadingExperience") else {}
                    
                LogEvent(self.queue_item, "Page speed API", LogEvent.INFO)
                self.origin_loading_exp = insight_data['originLoadingExperience'] if insight_data.get("originLoadingExperience") else {}
                try:
                    get_pg_screenshot = HttpRequestHandler(GetURL(type="page_speed_screenshot",url=siteurl)).json()
                    get_base = get_pg_screenshot['lighthouseResult']['fullPageScreenshot']['screenshot']['data'] if get_pg_screenshot.get("lighthouseResult") else False
                except Exception as error:
                    get_base=False
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)     

                save_image = HttpPostRequestHandler(data=get_base,url=GetURL(type="save_img")) if get_base != False else False
                
                LogEvent(self.queue_item, "Render Time", LogEvent.INFO)
                self.render_time = await performance.RenderTime()

                LogEvent(self.queue_item, "Green matrics", LogEvent.INFO)
                
                self.green_metrics = await mobile.GreenMetrics()
                
                LogEvent(self.queue_item, "Mobile Friendly", LogEvent.INFO)
                self.mobile_friendly = await performance.MobileFriendly()
                if save_image != False:
                    pg_shot.append(save_image['message'])


                ##################### END  ####################################
                base_store ={
                    "sitename":self.sitename,
                    "site_id":site_id,
                    "siteurl":siteurl,
                    "id":reco_id, 
                    "treemap":self.treemap,
                    "meta_description":self.meta_description,
                    "title":self.correct_title,
                    "site_logo":self.logo,
                    "performance_indicate":self.performance_indicate,
                    "request_total":self.request_total,
                    "load_time":self.load_time,
                    "code_count":self.code_count,
                    "pg_shot":pg_shot,
                    "loading_exp": self.loading_exp,
                    "origin_loading_exp": self.origin_loading_exp,
                    "size_page":self.size_page,
                    "status_reason_data":[str(insight_data),str(access_data)],
                    "render_time":self.render_time,
                    "mobile_friendly":self.mobile_friendly,
                    "green_metrics":self.green_metrics,
                    "created_at":str(datetime.datetime.now()),
                    "category":["brand_and_visual_identity","content_and_information","integration_and_service","navigation","performance_and_technical"]
                }
                
                try:
                    group_psi.insert_one(base_store)
                except Exception as error:
                    LogEvent(self.queue_item, "Group PSI started", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
            else:
                LogEvent(self.queue_item, "bypassed Group PSI", LogEvent.ERROR)
                
        except Exception as e:
                LogEvent(self.queue_item, "Group PSI started", LogEvent.ERROR)
            






        





        



        




