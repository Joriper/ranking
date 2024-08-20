from helpers.parser.parser import Parser
from helpers.requester.requester import HttpRequestHandler
from resmem import ResMem, transformer
from db.connection import *
import numpy as np
from colorthief import ColorThief
from error.error import Error
from PIL import Image
import re,sys,whois
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
from sentence_transformers import SentenceTransformer, util
from logger.json_logger import LogEvent
from PIL import Image
from io import BytesIO

from utils.selenium_utils import get_driver, get_firefox_driver

class BrandingandVisualIdentity:
    def __init__(self,**kwargs):
        self.site_url=kwargs['site_url']
        self.site_host=kwargs['site_host']
        self.branding_platform=False
        self.insight_id = kwargs['random_id']
        self.gov_authorized=False
        self.site_logo = False
        self.ownership_info = False
        self.meta_description = False
        self.memorable_logo = {}
        self.color_consit = {}
        self.imagery = {}
        self.sv_m = kwargs['sv_m']['dump_helper']
        self.link_collection = kwargs['sv_m']['dump_links']
        self.top_links = kwargs['sv_m']['top_links']
        self.queue_item = kwargs['queue_item']

        
    async def is_visual_design_logo(self):
        pass

    async def font_logo_same_website(self,run_type):
        try:        
            def GraphNormal(data):
                dop = Parser(data)
                get_icon = dop.find(attrs={"rel":re.compile("icon")}).get("href")
                get_image = dop.find_all("img")
                res = len([x for x in get_image if self.site_host in x.get("src") or x.get("src").startswith("/")])

                if (self.site_host in get_icon or get_icon.startswith("/") ) and (res > 0):
                    self.branding_platform={
                        "status":True,                        
                        "reason":"The website have font and logo present on the same site because {}".format(get_icon),
                        "data":str(get_icon)
                    }
                else:
                    self.branding_platform ={
                        "status":False,
                        "reason":"The font and logo looks like did'nt on the same platform",
                        "data":str(get_icon)
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])                    
        except Exception as error:
            LogEvent(self.queue_item, "font_logo_same_website", LogEvent.ERROR)
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.branding_platform == False:
            self.branding_platform={
                "status":False,
                "reason":"The website did'nt allow to track the private source or could'nt find logo on same platform",
                "data":""
            }

        return self.branding_platform

    async def ownership_information(self):
        try:
            result = whois.whois(self.site_host)
            check = list(result.values())
            if check.count(None) != len(result):
                self.ownership_info={
                    "status":True,
                    "data":result,
                    "reason":"The website is registered with domain services",
                }
        except Exception as error:
            LogEvent(self.queue_item, "ownership_information", LogEvent.ERROR)
            
            this_function_name = sys._getframe().f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.ownership_info == False:
            self.ownership_info={
                "status":False,
                "reason":"The website did'nt allow to get the ownership Informatin like domain etc try again latter",
                "data":{}
            }
        return self.ownership_info


    async def goverment_respective_web(self,run_type):
        def GraphNormal():
            try:
                if ".gov" in self.site_url:
                    self.gov_authorized={
                        "status":True,
                        "reason":self.site_url
                    }
                else:
                    self.gov_authorized = {
                        "status":False,
                        "reason":self.site_url
                    }
            except Exception as error:
                LogEvent(self.queue_item, "goverment_respective_web", LogEvent.ERROR)
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal()
        if self.gov_authorized ==  False:
            self.gov_authorized = {
                "status":False,
                "reason":"Failed to Detect"
            }
        return self.gov_authorized
        
    
    ########################### Other Use ###################
    async def website_logo(self,run_type):
        try:
            def GraphNormal(data_):
                dop = Parser(data_)
                get_icon = dop.find(attrs={"rel":re.compile("icon")}).get("href")
                if get_icon != None:
                    if get_icon.startswith("http") or get_icon.startswith("https"):
                        self.site_logo = get_icon
                    else:
                        self.site_logo = self.site_url+get_icon
                if self.site_logo ==  False:
                    self.site_logo = "The website does'nt have any site logo."
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])
        except Exception as error:
            LogEvent(self.queue_item, "website_logo", LogEvent.ERROR)
            
            #print("Error soun",error)
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.site_logo
        
    async def MetaDescription(self,run_type):
        def GraphNormal(data_):
            try:
                dop = Parser(data_)
                get_description = dop.find("meta",attrs={"name":"description"})
                if get_description != None:
                    self.meta_description = str(get_description.get("content"))
            except Exception as error:
                LogEvent(self.queue_item, "MetaDescription", LogEvent.ERROR)
                
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
            if self.meta_description == False:
                self.meta_description = "The website did'nt found any meta description."
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'])
        return self.meta_description
            



    async def LogoMemorable(self,run_type):
        try:
            dop = Parser(self.sv_m['dump'])
            get_icon = dop.find(attrs={"rel":re.compile("icon")}).get("href")
            save_logo = HttpRequestHandler(get_icon)
            with open(get_icon.split("/")[-1],"wb") as writer:
                writer.write(save_logo.content)
                writer.close()
            model = ResMem(pretrained=True)                
            img = Image.open('{}'.format(get_icon.split("/")[-1]))
            img = img.convert('RGB') 
            model.eval()
            image_x = transformer(img)                        
            prediction = model(image_x.view(-1, 3, 227, 227))
            self.memorable_logo = {
                "status":True,
                "reason":str(prediction)
            }       
        except Exception as error:
            LogEvent(self.queue_item, "LogoMemorable", LogEvent.ERROR)
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if len(self.memorable_logo) == 0:
            self.memorable_logo = {
                "status":False,
                "reason":"The prediction of logo did'nt found any scalablity"
            }
        try:
            os.remove(os.getcwd()+"/{}".format(get_icon.split("/")[-1]))
        except Exception as error:
            print(error)
            LogEvent(self.queue_item, "LogoMemorable", LogEvent.ERROR)

        return self.memorable_logo
    


    async def color_consistency(self):
        try:
            actual_rgb = []
            dominant_color = False

            def color_distance(c1, c2): 
                """Calculate the Euclidean distance between two colors in RGB space."""
                return np.sqrt(sum((a-b) ** 2 for a, b in zip(c1, c2)))

            def are_similar_colors(c1, c2, threshold=30):
                """Determine if two colors are similar within a threshold."""
                return color_distance(c1, c2) < threshold

            def palette_similarity(palette1, palette2, threshold=30):
                """Check if two palettes are similar, allowing for variations."""
                for color1 in palette1:
                    if not any(are_similar_colors(color1, color2, threshold) for color2 in palette2):
                        return False
                return True

            def is_design_consistent(pages_colors, threshold=30):
                """Assess if the design is consistent across multiple pages."""
                for i, page_colors in enumerate(pages_colors):
                    for other_page_colors in pages_colors[i+1:]:
                        if not palette_similarity(page_colors, other_page_colors, threshold):
                            return False
                return True
            
            options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
            driver = get_driver()
            
            os.mkdir(os.getcwd(),"color_images") if not os.path.exists("color_images") else False
            for total_links in self.top_links:
                driver.get(total_links)
                driver.get_screenshot_as_file(os.getcwd()+"/color_images/{}.png".format(total_links.split("://")[-1].replace("/","-")))
            

            for data in os.listdir(os.getcwd()+"/color_images/"):
                try:
                    #print(data)
                    grab_image = ColorThief(os.getcwd()+"/color_images/{}".format(data))
                    dominant_color = grab_image.get_color(quality=1)
                    actual_rgb.append(grab_image.get_palette(color_count=6))
                except:
                    pass
        
            consistency = is_design_consistent(actual_rgb)
            for i in os.listdir(os.getcwd()+"/color_images/"):
                os.remove(os.getcwd()+"/color_images/{}".format(i))

            self.color_consit = {
                "status":True,
                "reason":{"status":consistency,"reason":str(actual_rgb)+str(dominant_color)}
            }


        except Exception as error:
            LogEvent(self.queue_item, "color_consistency", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
    
        if len(self.color_consit) == 0:
            self.color_consit ={
                "status":False,
                "reason":{"status":0,"reason":"The color did'nt found any emotional impact of the graphics"}
            }
        return self.color_consit
    
    async def ImageryRelevance(self):
        try:
            model = ResNet50(weights='imagenet')
            get_all_images = Parser(self.sv_m['dump']).find_all("img",attrs={"src":re.compile(".png|.jpg|.jpeg",re.IGNORECASE)})[1:10]
            image_labels = []
            for img_url in get_all_images:
                try:
                    url = ""
                    if not img_url.get("src").startswith('http') or not img_url.get("src").startswith("https"):
                        url = self.site_url + img_url.get("src")
                    else:
                        url = img_url.get("src")
                
                    img_response = HttpRequestHandler(url)
                    img_obj = Image.open(BytesIO(img_response.content))
                    img_obj = img_obj.resize((224, 224))
                    img_array = img_to_array(img_obj)
                    img_array = np.expand_dims(img_array, axis=0)
                    img_array = preprocess_input(img_array)
                    predictions = model.predict(img_array)
                    labels = decode_predictions(predictions)
                    image_labels.extend(labels)
                    
                except Exception as error:
                    LogEvent(self.queue_item, "ImageryRelevance", LogEvent.ERROR)
                    
            models = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            image_embeddings = models.encode(image_labels)
            total_similarity = 0
            
            for img_emb in image_embeddings:
                similarities = util.cos_sim(img_emb, image_embeddings)
                total_similarity += np.max(similarities.numpy())
            average_similarity_score = total_similarity / len(image_embeddings) if len(image_embeddings) > 0 else 0

            if average_similarity_score >=1:
                self.imagery = {
                    "score":1,
                    "reason":average_similarity_score,
                    "images":str(get_all_images)                
                }
            else:
                self.imagery = {
                    "score":0,
                    "reason":average_similarity_score,
                    "images":str(get_all_images)
                }
            

        except Exception as error:
            LogEvent(self.queue_item, "ImageryRelevance", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)

        if len(self.imagery) == 0:
            self.imagery = {
                "score":0,
                "reason":0,
                "images":"Something is wrong"
            }
        return self.imagery
