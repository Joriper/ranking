from services.content_information.questions.questions import ContentandInformation
from services.branding_visual.questions.questions import BrandingandVisualIdentity
from db.connection import *
import datetime,sys
from logger.json_logger import LogEvent


class Group_Img:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.sitename = self.site['name']
        self.data = kwargs['collected']
        self.run_type="single"
        self.effective_content = False
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
                insight_data = self.data['page_speed']['insights']
                access_data = self.data['page_speed']['access']

                light_house = insight_data['lighthouseResult'] if insight_data.get("lighthouseResult") else []
                result1 = light_house['audits'] if isinstance(light_house,list) == False and light_house.get("audits") else []
                cache_assets = result1['uses-long-cache-ttl']['details']['items'] if isinstance(light_house,list) == False else []           
                content=ContentandInformation(site_url=siteurl,lighthouse=light_house,site_host=site_host,random_id=self.uid,sv_m=self.data, queue_item=self.queue_item)
                brand = BrandingandVisualIdentity(site_host=site_host,random_id=self.uid,site_url=siteurl,sv_m=self.data, queue_item=self.queue_item)

                self.effective_content =  await content.use_of_multimedia_video_audio(self.run_type)
                self.image_content = await brand.ImageryRelevance()
                base_store ={
                    "sitename":self.sitename,
                    "site_id":site_id,
                    "siteurl":siteurl,
                    "id":reco_id,
                    "effective_content":self.effective_content,
                    "imagery":self.image_content,
                    "created_at":str(datetime.datetime.now()),
                    "category":["content_and_information","branding_and_visuality"]
                }
                try:
                    group_img.insert_one(base_store)
                    result.append(base_store)
                except Exception as error:
                    LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
            return result
        except Exception as e:
            LogEvent(self.queue_item, "STEP ERROR", LogEvent.ERROR)







        





        



        

