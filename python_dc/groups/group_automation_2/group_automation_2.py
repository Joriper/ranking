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


class Group_Automation_2:
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
        self.home_linked = False
        self.smooth_adjust = False
        self.request_2s = False
        self.page_speed =False
        self.pool_consult = False
        self.data = kwargs['collected']
        self.static_assets = False
        self.queue_item = kwargs['queue_item']
        
    
    async def GroupCaller(self):
        site = self.site
        reco_id = str(site['_id'])
        site_id = str(site['site_id'])
        result=[]
        siteurl = str(site['url'])
        try:
            if "https" in siteurl or  "http" in siteurl:
                site_host = siteurl.split("://")[1].split("/")[0]            
                inter = InteractivityandEngagement(site_host=site_host,random_id=self.uid,site_url=siteurl,sv_m=self.data, queue_item=self.queue_item)
                performance = PerformanceandTechnical(data=None,record=None,cache=None,site_url=siteurl,site_host=site_host,lighthouse=None,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                mobile = MobileResponsiveness(site_host=site_host,random_id=self.uid,site_url=siteurl,lighthouse=None,sv_m=self.data)
                content=ContentandInformation(site_url=siteurl,lighthouse=None,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                brand = BrandingandVisualIdentity(site_url=siteurl,lighthouse=None,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)

                screen_shot_smooth_adjust = await mobile.smooth_adjust_screen()
                self.sort_filter = await content.sorting_and_filtering()
                self.different_sizes = await mobile.different_browser_size()
                self.form_input_responsive = await mobile.form_input_responsive()
                self.is_44_by_44 = await mobile.input_44_css_pixel()
                self.page_speed = await performance.page_load_speed()
                self.result_2s =  await performance.Result_2s()
                self.consist_color = await brand.color_consistency()
                self.cross_browser_testing = await performance.cross_browser_testing()
                self.screen_shot = screen_shot_smooth_adjust['screenshot_path']
                self.smooth_adjust = screen_shot_smooth_adjust['zoom_screen_content']
                self.mobile_compatability = await mobile.CrossBrowserCompatability()
                
                base_store ={
                    "sitename":self.sitename,
                    "site_id":site_id,
                    "site_url":siteurl,
                    "id":reco_id,
                    "different_sizes":self.different_sizes,
                    "smooth_adjust":self.smooth_adjust,
                    "screenshot":self.screen_shot,
                    "sort_filter":self.sort_filter,
                    "page_speed":self.page_speed['page_speed_value'],
                    "result_2s":self.result_2s,
                    "user_experience":self.page_speed,                
                    "form_input_responsive":self.form_input_responsive,
                    "is_44_by_44":self.is_44_by_44,
                    "color_consistancy":self.consist_color,
                    "processed":0,
                    "mobile_compatability":self.mobile_compatability,
                    "cross_browser_testing":self.cross_browser_testing,
                    "created_at":str(datetime.datetime.now()),
                    "category":["inter_engagement","mobile_responsive","performance_and_technical"]                
                }
                try:
                    group_automation_2.insert_one(base_store)
                    result.append(base_store)
                except Exception as error:
                    LogEvent(self.queue_item, "STEP ERROR", LogEvent.ERROR)
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)                            
        except Exception as e:
            LogEvent(self.queue_item, "STEP ERROR", LogEvent.ERROR)



















        





        



        

