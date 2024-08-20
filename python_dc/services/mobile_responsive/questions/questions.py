from error.error import Error
from helpers.parser.parser import Parser
from selenium import webdriver
from db.connection import *
from helpers.urls.urls import GetURL
from helpers.requester.requester import HttpPostRequestHandler,HttpRequestHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
from Screenshot import Screenshot
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import re,sys,os,pytesseract,requests
import ftplib,uuid,base64
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import PIL.Image
from PIL import Image
import PIL
import imquality.brisque as brisque


load_dotenv()
class MobileResponsiveness:
    def __init__(self,**kwargs):
        self.different_size=False
        self.is_meta=False
        self.lighthouse=kwargs['lighthouse']
        self.site_url=kwargs['site_url']
        self.is_metric=True
        self.total_percentage = {}
        self.form_input = False
        self.site_host =kwargs['site_host']
        self.insight_id = kwargs['random_id']
        self.record=kwargs['sv_m']['page_speed']
        self.sv_m = kwargs['sv_m']['dump_helper']
        self.browser_status={}
        self.link_collection = kwargs['sv_m']['dump_links']
        self.get_images = kwargs['sv_m']['images']
        self.uid = str(uuid.uuid4())
        self.site_url=kwargs['site_url']
        self.green_metrics = {}
        self.responsive_image=False
        self.size_44_44 = False
        self.zoom_screen_content=False
      
        self.user_agent="Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36"

    async def smooth_adjust_screen(self):
        path = os.path.abspath("../../screenshot/")
        path_list = []
        path = os.getcwd()+"/screenshot/"
        files = os.listdir(path)
        ob = Screenshot.Screenshot()
        try:
            chrome_options = webdriver.ChromeOptions()

            mobile_emulation = { "deviceName": "iPhone 5" }
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver1.get(self.site_url)
            ob.full_screenshot(driver1, save_path=os.getcwd()+"/screenshot/", image_name='_{}_{}_{}_{}_responsive_compatability_firefox.png'.format(384,self.site_host,str(uuid.uuid4()),"smooth_adjust_screen"), is_load_at_runtime=True,load_wait_time=3)
            driver1.close()
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)

        try:
            chrome_options = webdriver.ChromeOptions()
            mobile_emulation = { "deviceName": "iPad" }
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument("--headless=new")
            chrome_options.add_experimental_option("mobileEmulation",mobile_emulation)
            driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver2.get(self.site_url)
            driver2.close()
            ob.full_screenshot(driver2, save_path=os.getcwd()+"/screenshot/", image_name='_{}_{}_{}_{}_responsive_compatability_firefox.png'.format(768,self.site_host,str(uuid.uuid4()),"smooth_adjust_screen"), is_load_at_runtime=True,load_wait_time=3)
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)


        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            chrome_options.add_argument('--ignore-certificate-errors')

            driver3 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver3.maximize_window()
            driver3.get(self.site_url)
            driver3.close()
            ob.full_screenshot(driver3, save_path=os.getcwd()+"/screenshot/", image_name='_{}_{}_{}_{}_responsive_compatability_firefox.png'.format(1280,self.site_host,str(uuid.uuid4()),"smooth_adjust_screen"), is_load_at_runtime=True,load_wait_time=3)

        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)


        alltext = []
        for filex in files:
            if "smooth_adjust_screen" in filex:
                image = Image.open(path+filex)

                text = pytesseract.image_to_string(image)
                alltext.append(str(text).replace("\n","").strip())


        if len(alltext) > 0:
            self.zoom_screen_content={
                "status":True,
                "reason":"The website looks like adjust to its content",
            }
        if len(alltext) == 0:
            self.zoom_screen_content = {
                "status":False,
                "reason":"The website looks like it doesn't fit to its layout."
            }


        if self.zoom_screen_content == False:
            self.zoom_screen_content = {
                "status":False,
                "reason":"The website didn't allow to track the functionality of finding the layout adjustment."
            }
        dummy_images =[]
        for images in os.listdir(path):
            if "smooth_adjust_screen" in str(images):
                with open("{}{}".format(path,images),"rb") as fp:
                    base_image = base64.b64encode(fp.read()).decode('ascii')
                    if ".jpg" or ".jpeg" in images:
                        base_image = "data:image/jpeg;base64,{}".format(base_image)
                    elif ".png" in images:
                        base_image = "data:image/png;base64,{}".format(base_image)

                try:
                    json_image_response = HttpPostRequestHandler(data=base_image,url=GetURL(type="save_img"))
                    dummy_images.append({"viewport_"+images.split("_")[1]:json_image_response['message']})
                    os.remove("{}{}".format(path,images))
                except:
                    this_function_name = sys._getframe(  ).f_code.co_name
                    Error(error,self.__class__.__name__,this_function_name)


        self.zoom_screen_content['response_image'] = dummy_images
        return {"zoom_screen_content":self.zoom_screen_content,"screenshot_path":path_list}


    async def different_browser_size(self):
        path = os.getcwd()+"/screenshot/"         
        try:
            site_host = self.site_url.split("://")[1].replace("/","")
            screen_size = [{"screen":1280,"status":False},{"screen":768,"status":False},{"screen":384,"status":False}]
            for screens in screen_size:
                driver=None
                if screens['screen'] == 384:
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument("--headless=new")
                    chrome_options.add_argument('--ignore-ssl-errors=yes')
                    chrome_options.add_argument('--disable-gpu')
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-setuid-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    chrome_options.add_argument('--ignore-certificate-errors')                
                    mobile_emulation = { "deviceName": "iPhone 5" }

                    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                    driver.get(self.site_url)
                    driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",site_host,str(uuid.uuid4()),"different_browser_size"))
                elif screens['screen'] == 768:
                    mobile_emulation = {"deviceName": "iPad"}

                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument("--headless=new")
                    chrome_options.add_argument('--disable-gpu')
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-setuid-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')                
                    chrome_options.add_argument('--ignore-ssl-errors=yes')
                    chrome_options.add_argument('--ignore-certificate-errors')
                    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                    driver.get(self.site_url)
                    driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",site_host,str(uuid.uuid4()),"different_browser_size"))

                elif screens['screen'] == 1280:
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument('--disable-gpu')
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-setuid-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    chrome_options.add_argument("--headless=new")
                    chrome_options.add_argument('--ignore-ssl-errors=yes')
                    chrome_options.add_argument('--ignore-certificate-errors')                
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                    driver.maximize_window()
                    driver.get(self.site_url)
                    driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",site_host,str(uuid.uuid4()),"different_browser_size"))


                element=[]
                if len(driver.find_elements(By.TAG_NAME,"video")) != 0:
                    element.extend(driver.find_elements(By.TAG_NAME,"video"))
                if len(driver.find_elements(By.TAG_NAME,"iframe")) != 0:
                    element.extend(driver.find_elements(By.TAG_NAME,"iframe"))
                if len(driver.find_elements(By.TAG_NAME,"img")) != 0:
                    element.extend(driver.find_elements(By.TAG_NAME,"img"))

                if len(element) > 0:
                    check_size = []
                    for data in element:
                        get_screen_size = driver.get_window_size()['width']
                        if int(data.size['width']) <= int(get_screen_size):
                            check_size.append(True)
                        else:
                            driver.execute_script("arguments[0].scrollIntoView();", data)                         
                            driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",site_host,str(uuid.uuid4()),"different_browser_size"))
                            check_size.append(False)
                    if check_size.count(True) == len(element):
                        screens['status']=True
                    else:
                        screens['status']=False
                driver.close()
                driver.quit()
            test_screen_size=[x['status'] for x in screen_size]
            if test_screen_size.count(True) == 3:
                self.different_size={
                    "status":True,
                    "reason":str(test_screen_size)
                }
            
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        if self.different_size ==  False:
            self.different_size={
                "status":False,
                "reason":''
            }
        dummy_img = []
        for images in os.listdir(path):
            if "different_browser_size" in str(images):
                with open("{}{}".format(path,images),"rb") as fp:
                    base_image = base64.b64encode(fp.read()).decode('ascii')
                    if ".jpg" or ".jpeg" in images:
                        base_image = "data:image/jpeg;base64,{}".format(base_image)
                    elif ".png" in images:
                        base_image = "data:image/png;base64,{}".format(base_image)
                try:
                    json_image_response = HttpPostRequestHandler(data=base_image,url=GetURL(type="save_img"))
                    dummy_img.append(json_image_response['message'])
                    os.remove("{}{}".format(path,images))
                except Exception as error:
                    this_function_name = sys._getframe(  ).f_code.co_name
                    Error(error,self.__class__.__name__,this_function_name)


        self.different_size['response_image'] = dummy_img
        
        return self.different_size  

    async def form_input_responsive(self):
        path = os.getcwd()+"/screenshot/"
        mobile_emulation = { "deviceName": "iPad" }

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(self.site_url)
        driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",self.site_host,str(uuid.uuid4()),"form_input_responsive"))
        get_source = str(driver.page_source)
        result = [data for data in Parser(get_source).find_all("form") if len(re.findall("<input",str(data),re.IGNORECASE)) != 0]
    

        if len(result) > 0:
            tmp_data = []
            for i in result:
                forms = None
                try:
                    get_void = Parser(get_source).find_all("a",attrs={"href":"javascript:void(0);","title":re.compile("Search",re.IGNORECASE)})
                    get_void_sel = driver.find_elements(By.ID,"{}".format(get_void[-1].get("id")))
                    if len(get_void_sel) > 0:
                        get_void_sel[-1].click()
                except:
                    pass
                if forms == None:
                    try:
                        try:
                            forms = driver.find_element(By.NAME,i.get("name"))
                        except NoSuchElementException:
                            forms=driver.find_element(By.ID,i.get("id"))
                        except:
                            pass
                    except Exception as error:
                        pass
                    
                if forms == None:
                    try:
                        tmp_string = ""
                        for key,value in zip(result[-1].attrs.keys(),result[-1].attrs.values()):
                            tmp_string+="""[@{}='{}']""".format(key,value)
                            forms = driver.find_element(By.XPATH,"//form".format(tmp_string))
                    except:
                        pass


                try:
                    if forms.size['width'] <= driver.get_window_size()['width']:
                        driver.execute_script("arguments[0].scrollIntoView();", forms)                           
                        driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",self.site_host,str(uuid.uuid4()),"form_input_responsive"))
                        inputs_ =forms.find_elements(By.TAG_NAME,"input")
                        input_size = []
                        for check in inputs_:
                            input_size.append(check.size['width'])
                        if all(forms.size['width'] >= data for data in input_size) == True:
                            
                            self.form_input={
                                "status":True,
                                "data":str(input_size),
                                "reason":"The website ensures that its forms and input fields are user friendly and responsive when accessed on mobile devices."
                            }
                            break
                        else:
                            tmp_data.append(input_size)

                except Exception as error:
                    this_function_name = sys._getframe().f_code.co_name
                    Error(error,self.__class__.__name__,this_function_name)

        driver.close()
        driver.quit()
        # except Exception as error:
        #     this_function_name = sys._getframe(  ).f_code.co_name                     
        #     Error(error,self.__class__.__name__,this_function_name)

        if self.form_input == False:
            self.form_input = {
                "status":False,
                "reason":"The website forms and input field are not optimized for mobile devices.",
                "data":""
            }
        dummy_img = []
        for images in os.listdir(path):
            if "form_input_responsive" in str(images):
                with open("{}{}".format(path,images),"rb") as fp:
                    base_image = base64.b64encode(fp.read()).decode('ascii')
                    if ".jpg" or ".jpeg" in images:
                        base_image = "data:image/jpeg;base64,{}".format(base_image)
                    elif ".png" in images:
                        base_image = "data:image/png;base64,{}".format(base_image)
                try:
                    json_image_response = HttpPostRequestHandler(data=base_image,url=GetURL(type="save_img"))
                    dummy_img.append(json_image_response['message'])
                    os.remove("{}{}".format(path,images))
                except Exception as error:
                    this_function_name = sys._getframe(  ).f_code.co_name
                    Error(error,self.__class__.__name__,this_function_name)

        self.form_input['response_image'] = dummy_img

        return self.form_input

    async def input_44_css_pixel(self):
        try:
            mobile_emulation = { "deviceName": "iPhone 5" }

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("mobileEmulation",mobile_emulation)
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')        
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(self.site_url)
            result = Parser(driver.page_source)
            get_all_inputs = driver.find_elements(By.TAG_NAME,"input")
            not_found = []
            for input_ in get_all_inputs:
                if input_.value_of_css_property('width') == "44px" and input_.value_of_css_property('height') == "44px":
                    self.size_44_44={
                        "status":True,
                        "data":str(input_),
                        "reason":"The website have 44 by 44 css input pixels"
                    }
                    break
                else:
                   not_found.append(input_.size)
            driver.close()
            driver.quit()

            if self.size_44_44 == False:
                self.size_44_44={
                    "status":False,
                    "data":str(not_found),
                    "reason":"The website does'nt have any 44 by 44 css pixels"
                }
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        
        if self.size_44_44 == False:
            self.size_44_44 = {
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of checking element is 44 by 44"
            }

        return self.size_44_44

    async def view_port_meta(self,run_type):
        def GraphNormal(data_):
            try:
                header = {
                    "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
                    "Accept":"*/*",
                    "Accept-Encoding":"gzip, deflate, br",
                    "Accept-Language":"en-US,en;q=0.5",
                    "Alt-Used":self.site_host,
                    "Connection":"keep-alive",
                }
                data_ = requests.get(self.site_url,headers=header).text
                if len(Parser(data_).find_all("meta",attrs={"name":"viewport"})) > 0:
                    self.is_meta={
                        "status":True,
                        "reason":"The website have viewport meta tag <meta>.",
                        "data":str(Parser(data_).find_all("meta",attrs={"name":"viewport"}))
                    }
                else:
                    self.is_meta={
                        "status":False,
                        "reason":"The website doesn't have any viewport meta tag <meta>."
                    }
            except Exception as error:
                this_function_name = sys._getframe(  ).f_code.co_name
                Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'])

        if len(self.is_meta) == 0:
            self.is_meta = {
                "status":False,
                "reason":"The website didn't allow to track the functionality of viewport meta <meta>."
            }
        return self.is_meta

    async def fcp_fid_cls(self):
        try:
            self.is_metric=True
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)            
        return self.is_metric
    

    async def GreenMetrics(self):
        try:
            metrics = self.record['insights']['loadingExperience']['metrics']
            fcp = metrics["FIRST_CONTENTFUL_PAINT_MS"]["percentile"]/1000
            fid = metrics["FIRST_INPUT_DELAY_MS"]["percentile"]/1000
            lcp = metrics["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]/1000
            cls = metrics["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100
            
            tbt = self.lighthouse["audits"]["total-blocking-time"]["score"]

            self.green_metrics = {
                "status"
                "data":{
                    "fcp":True if fcp <= 1.8 else False,
                    "lcp":True if fid <= 2.5  else False,
                    "cls":True if cls <= 0.1 else False,
                    "tbt":True if tbt <= 0.8 else False
                },
                "reason":""
            }
        except Exception as error:

            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if len(self.green_metrics) == 0:
            self.green_metrics = {
                "status":False,
                "data":{
                    "fcp":False,
                    "fcp":False,
                    "fcp":False,
                    "fcp":False,                    
                },
                "reason":""
            }
        return self.green_metrics

    async def ResponsiveImage(self):
        try:
            for single_link in self.get_images:
                if "srcset" in str(single_link.attrs) and "@media" in str(single_link.attrs):
                    self.responsive_image = {
                        "status":True,
                        "data":str(single_link),
                        "reason":"The website has responsive image technique."
                    }
            def Pooler(link):
                check_css = HttpRequestHandler(link).text
                # Improved regular expression pattern
                responsive_image_pattern = r'(@media[^{]+{[^}]*?(img|background(-image)?)\s*:\s*url\([^)]+\)\s*(;|}))'
                if re.findall(responsive_image_pattern, check_css, re.IGNORECASE):
                    self.responsive_image = {
                        "status": True,
                        "data": str(check_css)[0:20000],
                        "reason": "The website has responsive image techniques"
                    }

                # if len(re.findall("img {| img{",check_css,re.IGNORECASE)) > 0:
                #     self.responsive_image = {
                #         "status":True,
                #         "data":str(check_css)[0:20000],
                #         "reason":"The website have a responsive image techniques"
                #     }

            if self.responsive_image == False:
                tmp = []
                get_all_style = Parser(HttpRequestHandler(self.site_url).text).find_all("link",attrs={"href":True})
                for data in get_all_style:
                    if data.get("href").startswith("/"):
                        tmp.append(self.site_url+data.get("href"))
                    else:
                        tmp.append(data.get("href"))

                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(Pooler, tmp)

            if self.responsive_image == False:
                self.responsive_image = {
                    "status":False,
                    "data":"",
                    "reason":"The websites looks like doesn't have any responsive images."
                }

        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)

        if self.responsive_image ==  False:
            self.responsive_image = {
                "status":False,
                "data":"",
                "reason":"The website didn't allow to track the responsive images whether present or not."
            }
        return self.responsive_image
## New update
    # import logging
    # import re
    # from typing import List
    # from concurrent.futures import ThreadPoolExecutor, as_completed
    # import requests
    #
    # async def check_responsive_images(html_content: str, images: List) -> bool:
    #     for img in images:
    #         if "srcset" in str(img.attrs) and "@media" in str(img.attrs):
    #             return True
    #
    #         # Check for CSS rules related to responsive images
    #     css_rules = re.findall(r'(@media[^{]+{[^}]*?})', html_content, re.MULTILINE | re.DOTALL)
    #     for rule in css_rules:
    #         if re.search(r'(max-width|min-width|width)', rule, re.IGNORECASE):
    #             if re.search(r'(img|background(-image)?)', rule, re.IGNORECASE):
    #                 return True
    #
    #     return False
    # async def ResponsiveImage(self):
    #     try:
    #         if check_responsive_images(HttpRequestHandler(self.site_url).text, self.get_images):
    #             self.responsive_image = {
    #                 "status": True,
    #                 "reason": "The website has responsive image techniques."
    #             }
    #         else:
    #             css_urls = [url.get("href") for url in Parser(HttpRequestHandler(self.site_url).text).find_all("link",
    #                                                                                                            attrs={
    #                                                                                                                "rel": "stylesheet"})]
    #
    #             with ThreadPoolExecutor(max_workers=10) as executor:
    #                 futures = [executor.submit(requests.get, url) for url in css_urls]
    #                 for future in as_completed(futures, timeout=10):
    #                     try:
    #                         css_content = future.result().text
    #                         if check_responsive_images(css_content, []):
    #                             self.responsive_image = {
    #                                 "status": True,
    #                                 "reason": "The website has responsive image techniques."
    #                             }
    #                             break
    #                     # except Exception as e:
    #                     #     logging.warning(f"Error fetching CSS content: {e}")
    #
    #             if not self.responsive_image:
    #                 self.responsive_image = {
    #                     "status": False,
    #                     "reason": "The website doesn't have any responsive image techniques."
    #                 }
    #
    #     except Exception as e:
    #         self.responsive_image = {
    #             "status": False,
    #             "reason": "The website didn't allow to track the responsive images whether present or not."
    #         }
    #
    #     return self.responsive_image

## New update end

    
    async def CrossBrowserCompatability(self):
        path = os.getcwd()+"/screenshot/"        
        browser = {}
        ob = Screenshot.Screenshot()
        for data in ["firefox","chrome"]:
            if data == "firefox":
                try:
                    firefox_options = webdriver.FirefoxOptions()
                    firefox_options.add_argument("--headless")
                    firefox_options.add_argument('--ignore-ssl-errors=yes')
                    firefox_options.add_argument('--ignore-certificate-errors')
                    firefox_options.add_argument('--disable-gpu')
                    firefox_options.add_argument('--no-sandbox')
                    firefox_options.add_argument('--disable-setuid-sandbox')
                    firefox_options.add_argument('--disable-dev-shm-usage')
                    user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
                    firefox_options.set_preference("general.useragent.override", user_agent)            
                    driver = webdriver.Firefox(options=firefox_options)
                    driver.get("{}".format(self.site_url))
                    img_url_firefox = ob.full_screenshot(driver, save_path=os.getcwd()+"/screenshot/", image_name='responsive_compatability_firefox.png', is_load_at_runtime=True,load_wait_time=3)                    
                    driver.close()
                    driver.quit()                    
                except Exception as error:
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
            else:

                try:
                    mobile_emulation = { "deviceName": "iPhone 5" }

                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_experimental_option("mobileEmulation",mobile_emulation)
                    chrome_options.add_argument("--headless=new")
                    chrome_options.add_argument('--ignore-ssl-errors=yes')
                    chrome_options.add_argument('--ignore-certificate-errors')
                    chrome_options.add_argument('--disable-gpu')
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-setuid-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')        
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                    driver.get(self.site_url)
                    img_url_chrome = ob.full_screenshot(driver, save_path=os.getcwd()+"/screenshot/", image_name='responsive_compatability_chrome.png', is_load_at_runtime=True,load_wait_time=3)                    
            
                except Exception as error:
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
            
        
            dummy_images = []
            for images in os.listdir(path):
                if "responsive_compatability" in str(images):
                    img = PIL.Image.open(path+images)
                    #score_result = brisque.score(img)
                    with open("{}{}".format(path,images),"rb") as fp:
                        base_image = base64.b64encode(fp.read()).decode('ascii')
                        if ".jpg" or ".jpeg" in images:
                            base_image = "data:image/jpeg;base64,{}".format(base_image)
                        elif ".png" in images:
                            base_image = "data:image/png;base64,{}".format(base_image)
                    try:
                        json_image_response = HttpPostRequestHandler(data=base_image,url=GetURL(type="save_img"))
                        dummy_images.append(json_image_response['message'])
                    except Exception as error:
                        this_function_name = sys._getframe(  ).f_code.co_name
                        Error(error,self.__class__.__name__,this_function_name)

                    if "firefox" in images:
                        browser['firefox'] ={"status":True,"image":json_image_response['message'],"score":1}
                    elif "chrome" in images:
                        browser['chrome'] = {"status":True,"image":json_image_response['message'],"score":1}        

                    os.remove("{}{}".format(path,images))
            
            if not browser.get("chrome"):
                browser['chrome']={"status":False,"image":"The Image Capturing blocked for this site try again latter","score":0}
            elif not browser.get("firefox"):
                browser['firefox'] = {"status":False,"image":"The Image Capturing blocked for this site try again latter","score":0}
            self.browser_status = browser
        return self.browser_status
            

    async def MediaQuery(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--ignore-certificate-errors')                
            mobile_emulation = { "deviceName": "iPhone 5" }

            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(self.site_url)
            data = str(driver.page_source)
            if len(re.findall("@media",data,re.IGNORECASE)) > 0:
                self.media_query = {
                    "status":True,
                    "reason":"The website may have media query for different resolutions",
                    "data":str(data)
                }
            else:
                self.media_query = {
                    "status":False,
                    "reason":"The website may not have media query for different resolutions",
                    "data":str(data)
                }    
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)            
        if len(self.media_query) == 0:
            self.media_query = {
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the resolutions of media query."
            }
        return self.media_query



