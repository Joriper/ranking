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


class Group_Beautiful:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.sitename = self.site['name']
        self.data  = kwargs['collected']
        self.run_type = "single"
        self.font_logo = False
        self.multi_lang = False
        self.copyright = False
        self.end_permit = False
        self.grievance = False
        self.social_media = False
        self.form_stat = False
        self.viewport_meta = False
        self.correct_title_ = False
        self.link_dist = False
        self.cdns = False
        self.about_page = False
        self.contact_page = False
        self.flagship = False
        self.download_excel_pdf = False
        self.online_trans = False
        self.is_opportunity = False
        self.pool_consult = False
        self.is_faq = False
        self.site_logo = False
        self.meta_description = False
        self.is_bread_crumb = False
        self.is_click_depth = False
        self.webhash = False
        self.change_detected = False
        self.is_404_500_error = False
        self.nav_across_site = False
        self.home_linked = False
        self.static_assets = False
        self.backlinks = False
        self.is_sitemap=False
        self.queue_item = kwargs['queue_item']
        self.uid = kwargs['uid']

    async def GroupCaller(self):
        LogEvent(self.queue_item, "process Initiated GroupCaller", LogEvent.INFO)

        site = self.site
        reco_id = str(site['_id'])
        sitename =self.site['name']
        site_id = str(site['site_id'])
        result=[]
        site_url = str(site['url'])
        try:
            if "https" in site_url or  "http" in site_url:
                site_host = site_url.split("://")[1].split("/")[0]

                LogEvent(self.queue_item, "STEP", LogEvent.INFO)
                performance = PerformanceandTechnical(data=None,record=None,cache=None,site_url=site_url,site_host=site_host,lighthouse=None,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                LogEvent(self.queue_item, "STEP", LogEvent.INFO)
                brand = BrandingandVisualIdentity(site_url=site_url,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                LogEvent(self.queue_item, "STEP", LogEvent.INFO)
                content=ContentandInformation(site_url=site_url,lighthouse=None,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                LogEvent(self.queue_item, "STEP", LogEvent.INFO)
                inter=InteractivityandEngagement(site_url=site_url,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                LogEvent(self.queue_item, "STEP", LogEvent.INFO)
                navigation=Navigation(site_url=site_url,site_host=site_host,lighthouse=None,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                LogEvent(self.queue_item, "STEP", LogEvent.INFO)
                mobile=MobileResponsiveness(site_host=site_host,site_url=site_url,lighthouse=None,loading_exp=None,random_id=self.uid,sv_m=self.data)
                LogEvent(self.queue_item, "STEP", LogEvent.INFO)
                integration=IntegrationandService(site_url=site_url,site_host=site_host,lighthouse=None,random_id=self.uid,sv_m=self.data)
                LogEvent(self.queue_item, "STEP", LogEvent.INFO)

                self.download_excel_pdf = await integration.can_download(self.run_type)
                self.is_click_depth  = await navigation.click_depth(self.run_type)
                self.online_trans = await inter.is_online_transaction(self.run_type)
                self.is_opportunity = await inter.opportunity(self.run_type)
                self.pool_consult = await inter.is_pool_cosultation_survey(self.run_type)
                self.font_logo = await brand.font_logo_same_website(self.run_type)
                self.multi_lang = await content.multilingual_support(self.run_type)
                self.copyright = await content.is_copyright_and_term_policy(self.run_type)
                self.end_permit = await integration._end_permit_benifits(self.run_type)
                self.grievance  =await integration.grienvance_system(self.run_type)
                self.social_media= await inter.social_media_integration(self.run_type)
                self.form_stat  = await inter.form_autofill_error_prevent(self.run_type)
                self.viewport_meta = await mobile.view_port_meta(self.run_type)
                self.correct_title_ = await navigation.correct_title(self.run_type)
                self.link_dist = await navigation.link_distiguishable(self.run_type)
                self.home_linked = await navigation.homepage_linked(self.run_type)
                self.cdns = await performance.is_cdns(self.run_type)
                self.change_detected = await content.is_web_regular_updated(self.run_type)
                self.form_exists  = await integration.form_submission_exits(self.run_type)

                self.webhash = await content.Web_base()

                self.is_404_500_error = await navigation.is_404_500_page()
                self.is_faq =  await navigation.has_faq(self.run_type)
                self.is_bread_crumb =  await navigation.bread_crumb(self.run_type)



                ################ For Other Use #############
                self.site_logo = await brand.website_logo(self.run_type)
                self.meta_description = await brand.MetaDescription(self.run_type)     

                base_detail = {                 
                    "sitename":self.sitename,
                    "site_id":site_id,
                    "site_url":site_url,
                    "id":reco_id,                               
                    "font_logo":self.font_logo,
                    "site_logo":self.site_logo,
                    "meta_description":self.meta_description,
                    "is_400_500_error":self.is_404_500_error,
                    "is_faq":self.is_faq,
                    "is_bread_crumb":self.is_bread_crumb,
                    "multi_lang":self.multi_lang,
                    "copyright":self.copyright,
                    "download_excel_pdf":self.download_excel_pdf,
                    "click_depth":self.is_click_depth,
                    "home_linked":self.home_linked,
                    "online_trans":self.online_trans,
                    "form_exists":self.form_exists,
                    "is_opportunity":self.is_opportunity,
                    "pool_consult":self.pool_consult,
                    "end_permit":self.end_permit,
                    "grievance":self.grievance,
                    "social_media":self.social_media,
                    "form_stat":self.form_stat,
                    "viewport_meta":self.viewport_meta,
                    "correct_title_":self.correct_title_,
                    "change_detected":self.change_detected,
                    "link_dist":self.link_dist,
                    "webhash":self.webhash,
                    "processed":0,
                    "cdns":self.cdns,
                    "created_at":str(datetime.datetime.now()),
                    "category":["brand_and_visual_identity","content_and_information","integration_and_service","inter_engagement","mobile_responsive","navigation","performance_and_technical"]
                }
                try:
                    
                    LogEvent(self.queue_item, "STEP", LogEvent.INFO)
                    group_beautiful.insert_one(base_detail)
                    result.append(base_detail)
                except Exception as error:
                    LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
        except Exception as e:
            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)






        





        



        

