from services.branding_visual.questions.questions import BrandingandVisualIdentity
from services.content_information.questions.questions import ContentandInformation
from services.navigation.questions.questions import Navigation
from services.integration_service.questions.questions import IntegrationandService
from services.inter_engagement.questions.questions import InteractivityandEngagement
from services.mobile_responsive.questions.questions import MobileResponsiveness
from db.connection import *
import datetime,sys
from services.performance_technical.questions.questions import PerformanceandTechnical
from logger.json_logger import LogEvent


class Group_Beautiful_2:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.sitename = self.site['name']
        self.data  = kwargs['collected']
        self.run_type = "single"

        self.font_logo = False
        self.multi_lang = False
        self.is_descriptive = False
        self.copyright = False
        self.end_permit = False
        self.grievance = False
        self.social_media = False
        self.form_stat = False
        self.viewport_meta = False
        self.correct_title_ = False
        self.link_dist = False
        self.about_page = False
        self.contact_page = False
        self.flagship = False
        self.download_excel_pdf = False
        self.online_trans = False
        self.is_opportunity = False
        self.pool_consult = False
        self.is_faq = False
        self.is_bread_crumb = False
        self.is_404_500_error = False
        self.nav_across_site = False
        self.gov_respective = False
        self.home_linked = False
        self.static_assets = False
        self.backlinks = False
        self.broken_link = False        
        self.is_sitemap=False
        self.uid = kwargs['uid']
        self.queue_item = kwargs['queue_item']
    
    async def GroupCaller(self):
        site = self.site
        reco_id = str(site['_id'])
        sitename =self.site['name']
        site_id = str(site['site_id'])
        
        site_url = str(site['url'])
        try:
            if "https" in site_url or  "http" in site_url:
                site_host = site_url.split("://")[1].split("/")[0]
                result=[]
                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                
                performance = PerformanceandTechnical(data=None,record=None,cache=None,site_url=site_url,site_host=site_host,lighthouse=None,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                
                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                brand = BrandingandVisualIdentity(site_url=site_url,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                
                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                content=ContentandInformation(site_url=site_url,lighthouse=None,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                inter=InteractivityandEngagement(site_url=site_url,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                
                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                navigation=Navigation(site_url=site_url,site_host=site_host,lighthouse=None,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                
                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                mobile=MobileResponsiveness(site_host=site_host,site_url=site_url,lighthouse=None,loading_exp=None,random_id=self.uid,sv_m=self.data)
                
                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                integration=IntegrationandService(site_url=site_url,site_host=site_host,lighthouse=None,random_id=self.uid,sv_m=self.data)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.contact_page = await content.is_contact_page(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.about_page =await content.is_about_page(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.flagship = await content.flagship_priorities(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.nav_across_site = await navigation.navigation_cmp_across_site(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.is_sitemap = await navigation.has_site_map()

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.static_assets = await navigation.static_assets()

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.broken_link = await navigation.is_nobroken_link(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.backlinks = await navigation.BackLink(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.is_descriptive = await content.descriptive_hyperlink(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.gov_respective = await brand.goverment_respective_web(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.responsive_image = await mobile.ResponsiveImage()

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.comment_share_media = await inter.Social_Media_Comment(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.user_generated_content = await inter.UserGeneratedContent(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.memorable_logo = await brand.LogoMemorable(self.run_type)

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                self.cdn_performance = await performance.CDNPerformace()

                LogEvent(self.queue_item, "STEP ", LogEvent.DEBUG)
                old_hash = await content.Web_base()
            
                base_detail = {
                    "sitename":self.sitename,
                    "site_id":site_id,
                    "site_url":site_url,
                    "id":reco_id,      
                    "backlink":self.backlinks,
                    "about_page":self.about_page,
                    "contact_page":self.contact_page,
                    "flagship":self.flagship,
                    "nav_across_site":self.nav_across_site,
                    "site_map":self.is_sitemap,
                    "static_assets":self.static_assets,
                    "broken_link": self.broken_link,
                    "responsive_image":self.responsive_image,
                    "comment_share_media":self.comment_share_media,
                    "is_descriptive":self.is_descriptive,
                    "gov_respective":self.gov_respective,
                    "web_hash":old_hash,
                    "user_generated_content":self.user_generated_content,
                    "memorable_logo":self.memorable_logo,
                    "cdn_performace":self.cdn_performance,
                    "processed":0,
                    "created_at":str(datetime.datetime.now()),
                    "category":["brand_and_visual_identity","content_and_information","integration_and_service","inter_engagement","mobile_responsive","navigation","performance_and_technical"]
                }

                try:
                    group_beautiful_2.insert_one(base_detail)
                    result.append(base_detail)
                except Exception as error:
                    LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
            else:
                LogEvent(self.queue_item, "BYPASSED all Group_Beautiful_2", LogEvent.DEBUG)
        except Exception as e:
            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
            






        





        



        

