from helpers.requester.requester import HttpRequestHandler
from helpers.parser.parser import Parser
from language_detector import detect_language
from error.error import Error
from concurrent.futures import ThreadPoolExecutor
import re,sys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from axe_selenium_python import Axe

class Accessibility:
    def __init__(self,**kwargs):
        self.site_url=kwargs['site_url']
        self.site_host=kwargs['site_host']
        self.heading_optmize = {}
        self.url_structure = {}
        self.sv_m= HttpRequestHandler(self.site_url).text
        #self.accessiblity = HttpRequestHandler("https://content-pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?category=ACCESSIBILITY&url={}&strategy=DESKTOP".format(self.site_url)).json()
        self.access = {}
        self.heading_label_purpose=None
        self.human_language=False
        self.dub_it_attr=False
        self.link_purpose=False
        self.contrast_ratio_4_=False
        self.contrast_ratio_3_=False

    async def keyboard_interface_time(self):
        pass
    async def keyboard_focus_indicator(self):
        pass

    async def display_orientation(self):
        pass
    async def without_loss_content(self):
        pass
    async def non_text_alternative(self):
        pass
    async def heading_label_purp(self):
        try:
            check_head_labels = Parser(self.sv_m)
            head_check = False

            for jx in check_head_labels.find_all(re.compile("^h[1-6]$")):
                if jx.text != "":
                    head_check=True
                else:
                    break

            input_lab = False
            all_input=[x.get("name") for x in check_head_labels.find_all("input")]
            for sets in check_head_labels.find_all("label"):
                if sets.get("for") in all_input:
                    input_lab=True
                else:
                    break

            if head_check == False and input_lab == False:
                self.heading_label_purpose=False
            else:
                self.heading_label_purpose=True
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.heading_label_purpose

    async def web_app_screen(self):
        pass
    async def keyboard_focus_away_with_key(self):
        pass
    
    async def  default_human_language(self):
        try:
            tmp = Parser(self.sv_m).find_all("a",href=lambda x: not (".pdf" in x  or ".pps" in x or  ".jpeg" in x or ".jpg" in x or ".pps" not in x or  ".svg" in x or ".mp3" in x or ".mp4" in x or ".m4v" in x)  and (x.startswith("/") or re.findall("^(http|https).*{}.*".format(self.site_host),str(x))))

            links=[]
            for i in tmp:
                if i.get("href").startswith("/"):
                    links.append(self.site_url.strip("/")+i.get("href"))
                else:
                    links.append(i.get("href"))
            total_len = []

            def LanguageDetect(url):
                res = Parser(HttpRequestHandler(url).text).text
                lan = detect_language(res)
                if lan != None:
                    total_len.append(lan)

            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(LanguageDetect, links)

            if len(total_len) == len(links):
                self.human_language = True
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.human_language


    async def html_markup_uniqueuser(self):
        try:
            id_dub = False
            attr_dub = False

            html_handle = Parser(self.sv_m)
            html_dub_id = [x.get("id") for x in html_handle.find_all(attrs={"id":True})]
            html_dub_attr = [x.attrs.keys() for x in html_handle.find_all()]
            for x in html_dub_id:
                if html_dub_id.count(x) > 1:
                    id_dub = True
            
            for i in html_dub_attr:
                for h in list(i):
                    if list(i).count(h) > 1:
                        attr_dub = True
            
            if id_dub == True or attr_dub == True:
                self.dub_id_attr=False
            else:
                self.dub_id_attr=True
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.dub_id_attr

    async def user_interface_component(self):
        pass
    async def content_without_loss(self):
        pass
    async def info_structure_relationship(self):
        pass
    async def line_height_spacing(self):
        pass
    async def recv_removing_pointer(self):
        pass
    async def color_not_used_visual(self):
        pass
    async def mechanism_bypass_dublicate(self):
        pass
    async def correct_secquence_programmatically(self):
        pass
    async def sensor_char_visual_orientation(self):
        pass
    async def purpose_input_programatically(self):
        pass
    async def contrast_ration_4_5_1(self):
        try:
            cont1 = self.accessiblity['lighthouseResult']['audits']['color-contrast']['details']['items']

            for con in cont1:
                if "Expected contrast ratio of 4.5:1"  in con['node']['explanation']:
                    self.contrast_ratio_4_=False
                    break
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)                
        return self.contrast_ratio_4_
                               
    async def contrast_ration_3_1(self):
        try:
            cont1 = self.accessiblity['lighthouseResult']['audits']['color-contrast']['details']['items']
            for con in cont1:
                if "Expected contrast ratio of 3:1" in con['node']['explanation']:
                    self.contrast_ratio_3_=False
                    break
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)
        return self.contrast_ratio_3_

         
    async def webpage_navigate_sequence(self):
        pass

    async def link_purpose_alone(self):
        try:
            purpose = Parser(self.sv_m).find_all("a",href=lambda x: not (".pdf" in x or ".pps" in x  or ".jpeg" in x or ".jpg" in x or ".svg" in x or ".mp3" in x or ".mp4" in x or ".m4v" in x)  and (x.startswith("/") or re.findall("^(https|http).*{}".format(self.site_host),str(x))))
            for i in purpose:
                res = [x for x in i.get("href").split("/") if x]
                for s in res:
                    if i.text.find(s):
                        self.link_purpose=True
                    else:
                        self.link_purpose=False
                        break
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)                    
        return self.link_purpose

    async def more_than_way_locate_webpage(self):
        pass
    async def multipoint_pathbased_gesture(self):
        pass
    async def reversal_essential(self):
        pass



    async def URL_Structure(self):
        handle_url = Parser(self.sv_m).find_all("a",href=re.compile("^https|http.*{}".format(self.site_host)))
        if len(handle_url) > 0:
            for links in handle_url:
                if len(re.findall("^(?:http://|https://){}.*/[A-Za-z].*".format(self.site_host),re.IGNORECASE)) > 0:

                    self.url_structure = {
                        "status":True,
                        "reason":links
                    }
                    break
            if len(self.url_structure) > 0:
                self.url_structure = {
                    "status":False,
                    "reason":handle_url
                }
        else:
            self.url_structure = {
                "status":False,
                "reason":"The "
            }

        
    async def accessibility_find(self):
        try:

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            chrome_options.add_argument('--ignore-certificate-errors')                
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            driver.get(self.site_url)
            axe = Axe(driver)
            axe.inject()
            results = axe.run()
            driver.close()
            if len(results) > 0:
                
                self.access = {
                    "status" : True,
                    "reason" : [results]

                }
            else:
                self.access = {
                    "status": False,    
                    "reason": [results]

                }
        except Exception as error:
            this_function_name = sys._getframe().f_code.co_name
            Error(error, self.__class__.__name__, this_function_name)
        
        return self.access





