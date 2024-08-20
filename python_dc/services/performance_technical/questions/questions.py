
from helpers.requester.requester import HttpPostRequestHandler,HttpRequestHandler
from error.error import Error
import requests,json
import sys,os,uuid,base64,re,datetime,time
from helpers.byte_converter.bytes import convert_bytes
from helpers.parser.parser import Parser
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from helpers.urls.urls import GetURL
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver
from db.connection import *
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from logger.json_logger import LogEvent
from python_dc.utils.selenium_utils import get_driver, get_firefox_driver



load_dotenv()
def Comptability(data):
    browser_based = []
    
    try:
        for reqbase in data:
            resp = reqbase['data']
            performance_based = resp['lighthouseResult']['categories']['performance']['score']*100
            main_audit = resp['lighthouseResult']['audits']
            js_based = main_audit['legacy-javascript']['score']
            response_based = main_audit['server-response-time']['score']
            css_based = main_audit['unminified-css']['score']
            redirect_based = main_audit['redirects']['score']
            font_based = main_audit["font-display"]["score"]

            fcp = str(resp["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"]/1000)+"s"
            fid = str(resp["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["percentile"]/1000)+"s"
            lcp = str(resp["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]/1000)+"s"
            cls = str(resp["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100)+"s"

            browser_based.append({reqbase['name']:{"js":js_based,"css":css_based,"redirect":redirect_based,"response":response_based,"performance":performance_based,"font":font_based,"metrics":{"fcp":fcp,"fid":fid,"lcp":lcp,"cls":cls}}})
            return {"data":browser_based}
    except Exception as error:
        Error(error,"None","None")
        return {"data":browser_based}

class PerformanceandTechnical:
    def __init__(self,**kwargs):
        self.data=kwargs['data']
        self.record=kwargs['sv_m']['page_speed']
        self.cache=kwargs['cache']
        self.site_url=kwargs['site_url']
        self.result_2={}
        self.site_host=kwargs['site_host']
        self.is_cdn=False
        self.page_speed_time=None
        self.user_experience={}
        self.page_size=0
        self.browser_status={}
        self.network_latency = {}
        self.lighthouse=kwargs['lighthouse']
        self.cached=False
        self.error_rate = {}
        self.cacheability=False
        self.load_time=0
        self.cdn_performance = {}
        self.third_party_scripts = False
        self.uid = str(uuid.uuid4())
        self.insight_id = kwargs['random_id']
        self.sv_m = kwargs['sv_m']['dump_helper']
        self.top_links = kwargs['sv_m']['top_links'] 
        self.mobile_insight = kwargs['sv_m']['mobile_insight']     
        self.link_collection = kwargs['sv_m']['dump_links']
        self.mobile_friendly = {}
        self.render_time = {}
        self.compatabilitys=None
        self.third_party_service=False
        self.time_to_first_byte = {}
        self.loading_page  = {}
        self.minimize_request = {}
        self.page_size_loading = {}
        self.queue_item = kwargs['queue_item']


    async def cross_browser_testing(self):
        path = os.getcwd()+"/screenshot/"
        browser = {}
        try:
            browser_list = ["firefox","chrome"]
            for bro in browser_list:
                if bro == "firefox":
                    try:
                        options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
                        
                        driver = webdriver.Firefox(options=options)
                        driver.get("{}".format(self.site_url))
                        driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}.png".format("firefox",self.site_host,"cross_browser_testing"))
                        driver.close()
                        driver.quit()                    
                    except Exception as error:
                        LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                        
                elif bro == "chrome":
                    try:
                        options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
                        driver = get_driver(options)
                        driver.get("{}".format(self.site_url))
                        driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}.png".format("chrome",self.site_host,"cross_browser_testing"))
                        driver.close()
                        driver.quit()                    
                    except Exception as error:
                        LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
        except Exception as error:
            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)

        dummy_images = []
        for images in os.listdir(path):
            if "cross_browser_testing" in str(images):
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
                    LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                    
                if "firefox" in images:
                    browser['firefox'] ={"status":True,"image":json_image_response['message']}
                elif "chrome" in images:
                    browser['chrome'] = {"status":True,"image":json_image_response['message']}        

                os.remove("{}{}".format(path,images))
        
        if not browser.get("chrome"):
            browser['chrome']={"status":False,"image":"Missing"}
            LogEvent(self.queue_item, "image missing ", LogEvent.WARN)
            
        elif not browser.get("firefox"):
            browser['firefox'] = {"status":False,"image":"Missing"}
            LogEvent(self.queue_item, "image missing ", LogEvent.WARN)
        
        self.browser_status = browser
        return self.browser_status

    async def Result_2s(self):
        try:
            options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
            driver = get_driver(options=options)
            driver.maximize_window()
            driver.get("{}".format(self.site_url))
            page_source = driver.page_source
            get_search_inputs = Parser(str(page_source)).find_all("input",attrs={"placeholder":re.compile("search",re.IGNORECASE)})
            if len(get_search_inputs):
                search_input = driver.find_elements(By.ID,"{}".format(get_search_inputs[-1].get("id")))
                if len(search_input):
                    get_all_inputs = driver.find_elements(By.TAG_NAME,"input")
                    get_all_buttons = driver.find_elements(By.TAG_NAME,"button")
                    for inputs in get_all_inputs:
                        if inputs.get_attribute("value") in ["search","Search"]:
                            search_btn = inputs

                    for inputs in get_all_buttons:
                         if inputs.get_attribute("title") == ["Search","search"]:
                            search_btn = inputs
                    

                    get_void = Parser(str(page_source)).find_all("a",attrs={"href":"javascript:void(0);","title":re.compile("Search",re.IGNORECASE)})
                    if len(get_void) == 0:
                        get_void = Parser(str(page_source)).find_all("a",attrs={"href":"javascript:void(0);","id":re.compile("toggleSearch",re.IGNORECASE)})


                    if len(get_void) > 0:
                        get_void_sel = driver.find_elements(By.ID,"{}".format(get_void[-1].get("id")))
                        if len(get_void_sel) > 0:
                            get_void_sel[-1].click()
                        else:
                            get_void_sel = driver.find_elements(By.XPATH,"//a[@title='{}']".format(get_void[-1].get("title")))
                            if len(get_void_sel) > 0:
                                get_void_sel[-1].click()
                    search_input[-1].send_keys("Helloworld")
                    start_date = datetime.datetime.now()
                    search_btn.click()
                    end_date = datetime.datetime.now()

                    get_seconds = (end_date - start_date).seconds
                    if int(get_seconds) <=2:
                        self.result_2 = {
                            "status":True,
                            "reason":"Search Result time is {}".format(get_seconds),
                            "data":""
                        }
                    else:
                        self.result_2 = {
                            "status":False,
                            "reason":"Search Result time is {}".format(get_seconds)
                        }
        
        except Exception as error:
            LogEvent(self.queue_item, "ERROR", LogEvent.ERROR)
            
            # this_function_name = sys._getframe(  ).f_code.co_name                     
            # Error(error,self.__class__.__name__,this_function_name)
        if len(self.result_2) == 0:
            self.result_2 = {
                "status":False,
                "reason":"The website did'nt allow to track the Response time."
            }
            LogEvent(self.queue_item, "The website did'nt allow to track the Response time", LogEvent.WARN)

        return self.result_2

    async def page_load_speed(self):
        try:
            page_speed_time = self.record['insights']['loadingExperience']['metrics']
            fcp = page_speed_time["FIRST_CONTENTFUL_PAINT_MS"]["percentile"]/1000
            fid = page_speed_time["FIRST_INPUT_DELAY_MS"]["percentile"]/1000
            lcp = page_speed_time["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]/1000
            cls = page_speed_time["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100
            total_time_blocking = self.lighthouse["audits"]["total-blocking-time"]["displayValue"]
            speed_index = self.lighthouse["audits"]["speed-index"]["displayValue"]

            self.page_speed_time=str(fcp+lcp+fid+cls)+" s"

            options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
            driver = get_driver(options=options)

            first_user,second_user,third_user = None,None,None
            for test_range in range(0,3):
                start_time = datetime.datetime.now()
                driver.get("{}".format(self.site_url))
                end_time = datetime.datetime.now()
                if test_range == 0:
                    first_user = (end_time - start_time).seconds
                elif test_range == 1:
                    second_user = (end_time - start_time).seconds
                elif test_range == 2:
                    third_user = (end_time - start_time).seconds
                time.sleep(5)
            page_speed_value = False
            if (first_user >=8) and (second_user > 3 and second_user <=8) and (third_user > 0 and third_user <= 3):
                page_speed_value=True

            self.user_experience={"first_contentful_paint":fcp,"largest_contentful_paint":lcp,"total_time_blocking":total_time_blocking,"cumulative_layout_shift":cls,"speed_index":speed_index,"page_speed_time":self.page_speed_time,"page_speed_value":page_speed_value}
        except Exception as error:
            LogEvent(self.queue_item, "ERROR", LogEvent.ERROR)
            
            # this_function_name = sys._getframe(  ).f_code.co_name                     
            # Error(error,self.__class__.__name__,this_function_name)
            self.user_experience={"first_contentful_paint":0,"largest_contentful_paint":0,"total_time_blocking":0,"cumulative_layout_shift":0,"speed_index":0,"page_speed_time":0,"page_speed_value":-1}
        return self.user_experience

    async def load_times(self):
        try:
            load_times = self.lighthouse['audits']['metrics']['details']['items'][0]
            self.load_time = (load_times['observedLargestContentfulPaint']+load_times['cumulativeLayoutShift']+load_times['totalBlockingTime']/1000)/1000
        except Exception as error:
            LogEvent(self.queue_item, "ERROR", LogEvent.ERROR)

            # print("Error is",error)
            # this_function_name = sys._getframe(  ).f_code.co_name                     
            # Error(error,self.__class__.__name__,this_function_name)
        if self.load_time == 0:
            self.load_time = "The website does'nt allow to get load time."
            LogEvent(self.queue_item, "ERROR", LogEvent.ERROR)
            
        return self.load_time

    async def compatability(self):
        comptability = []
        try:
            browser_list = ["firefox","chrome"]
            for bro in browser_list:
                if bro == "firefox":
                    try:
                        options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
                        driver = get_firefox_driver(options=options)
                        driver.get("view-source:{}".format(GetURL(type="comptability",url=self.site_url)))
                        pretend = driver.find_element(By.TAG_NAME,"pre").text
                        data = json.loads(pretend)                        
                        driver.close()
                        driver.quit()
                        check_firefox = Comptability(data)      
                        comptability.append(check_firefox)
                    except Exception as error:
                        LogEvent(self.queue_item, "compatability error", LogEvent.ERROR)
                        # this_function_name = sys._getframe(  ).f_code.co_name                     
                        # Error(error,self.__class__.__name__,this_function_name)

                elif bro == "chrome":
                    try:
                        options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
                        driver = get_driver(options=options)
                        driver.get("{}".format(GetURL(type="comptability",url=self.site_url)))
                        pre = driver.find_element(By.TAG_NAME,"pre").text
                        datax = json.loads(pre)
                        driver.close()
                        driver.quit()   

                        check_chrome = Comptability(datax)      
                        comptability.append(check_chrome)                 
                    except Exception as error:
                        LogEvent(self.queue_item, "compatability error", LogEvent.ERROR)
                        
                        this_function_name = sys._getframe(  ).f_code.co_name                     
                        Error(error,self.__class__.__name__,this_function_name)
        except Exception as error:
            LogEvent(self.queue_item, "compatability error", LogEvent.ERROR)
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        return comptability

    async def uptime(self):
        pass

    async def page_sizes(self):
        try:
            total_request=self.lighthouse['audits']['network-requests']['details']['items']

            self.page_size = convert_bytes(sum([each['resourceSize'] for each in total_request]))
        except Exception as error:
            LogEvent(self.queue_item, "page size error", LogEvent.ERROR)
            
            # this_function_name = sys._getframe(  ).f_code.co_name                     
            # Error(error,self.__class__.__name__,this_function_name)
        return self.page_size


    async def cache_compression_optimization(self):
        try:
            if self.cache:
                self.cached = True
        except Exception as error:
            LogEvent(self.queue_item, "cache_compression_optimization error", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.cached
        

    async def is_cdns(self,run_type):
        try:
            def GraphNormal(data_,data_collection):
                def LinkPooler(link):
                    check_for_css = Parser(link['data']).find_all("link",attrs={"href":lambda x: not(self.site_host in x) and  (x.startswith("http") or x.startswith("https"))})
                    js_check = Parser(link['data']).find_all("script",attrs={"src":True})
                    check_for_js = [result for result in js_check if not self.site_host in result.get("src")  and  (result.get("src").startswith("http") or result.get("src").startswith("https"))]
                    if len(check_for_css) > 0 or len(check_for_js) > 0:
                        self.is_cdn={
                            "status":True,
                            "reason":str([str(check_for_css),str(check_for_js)])
                        }
                            
                        self.third_party_service=True
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(LinkPooler, data_collection)
                
                if  self.is_cdn == False:
                    self.is_cdn={
                        "status":False,
                        "reason":str(data_)
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m,self.link_collection)
        except Exception as error:
            LogEvent(self.queue_item, "is_cdns error", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.is_cdn 
           
    async def recovery_plan(self):
        pass

    async def Cacheability(self):
        try:
            check_cache = requests.session()
            for repeat in range(0,2):
                result = check_cache.get(self.site_url).headers
                if result.get("Cache-Control") == True and "public" in result['Cache-Control'] and result.get("Etag") == True:
                    self.cacheability = {
                        "status":True,
                        "data":str(result),
                        "reason":"The website effectively utilize a browser Caching to enhance cacheability."
                    }
            if self.cacheability == False:
                self.cacheability={
                    "status":False,
                    "reason":"The website look like does'nt have any caching machenism."
                }
        except Exception as error:
            LogEvent(self.queue_item, "Cacheability error", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.cacheability ==  False:
            self.cacheability = {
                "status":False,
                "reason":"The website did'nt allow to track the Response or Caching functionality for security reason."
            }
        return self.cacheability
    
    async def ErrorRate(self):
        dummy = []
        def TestLink(link):
            check_error = HttpRequestHandler(link).status_code
            if check_error == 200:
                dummy.append(check_error)

    
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(TestLink, self.top_links)
        
        if len(dummy) == len(self.top_links):
            self.error_rate= {
                "status":True,
                "data":str(dummy),
                "reason":"The website have any link that include error."
            }
        else:
            self.error_rate = {
                "status":False,
                "reason":"The website does'nt have link that include error.",
                "data":str(dummy)
            }
      
        if self.error_rate == False:
            self.error_rate = {
                "status":False,
                "reason":"The website did'nt allow to track calculate the error rate for security reasons.",
                
            }
        return self.error_rate
        
    async def ThirdPartyScripts(self):
        try:
            self.third_party_scripts = {
                "status":True,
                "reason":[self.lighthouse['audits']['third-party-summary']]
            }
        except Exception as error:
            LogEvent(self.queue_item, "ThirdPartyScripts error", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.third_party_scripts == False:
            self.third_party_scripts={
                "status":False,
                "reason":"The website did'nt found any thirdparty scripts."
            }
        return self.third_party_scripts         
        
    async def NetworkLatency(self):
        try:
            self.network_latency = {
                "status":True,
                "reason":[self.lighthouse['audits']['server-response-time']]
            }
        except Exception as error:
            LogEvent(self.queue_item, "NetworkLatency error", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if len(self.network_latency) == 0:
            self.network_latency = {
                "status":False,
                "reason":[{"data":"The website did'nt found any faster response time"}]
            }

        return self.network_latency   


    async def TIME_TO_FIRST_BYTE(self):
        try:
            endpoint = GetURL(type="psi", url=self.site_url)
            # print("endpoint", endpoint)
            response = HttpRequestHandler(endpoint)
            data = response.json()
            ttfb = data.get('loadingExperience', {}).get('metrics', {}).get('EXPERIMENTAL_TIME_TO_FIRST_BYTE', {}).get('percentile')

            if ttfb:
                self.time_to_first_byte = {
                    "status": True,
                    "reason": int(ttfb)
                }
            else:
                self.time_to_first_byte = {
                    "status": False,
                    "reason": int(ttfb)
                }

        except Exception as error:
            # print("wor1")
            LogEvent(self.queue_item, "TIME_TO_FIRST_BYTE error", LogEvent.ERROR)
            
            this_function_name = sys._getframe().f_code.co_name
            Error(error, self.__class__.__name__, this_function_name)
            
        if self.time_to_first_byte == {}:
            self.time_to_first_byte = {
                "status": False,
                "reason": 0
            }

        return self.time_to_first_byte

    async def quicker_loading_page(self):
        try:
            endpoint = GetURL(type="psi", url=self.site_url)
            # print("endpoint", endpoint)
            response = HttpRequestHandler(endpoint)
            data = response.json()
            loading = data.get("originLoadingExperience")
            # print("loading", loading)
            if len(loading) > 0:
                self.loading_page = {
                    "status": True,
                    "reason": str(loading)
                }

            else:
                self.loading_page  = {
                    "status": False,
                    "reason": str(loading)
                }
        except Exception as error:
            # print("wor2")
            LogEvent(self.queue_item, "quicker_loading_page error", LogEvent.ERROR)
            
            this_function_name = sys._getframe().f_code.co_name
            Error(error, self.__class__.__name__, this_function_name)
        if self.loading_page == {}:
            self.loading_page  = {
                    "status": False,
                    "reason": "Faild to detect"
                }    
        return self.loading_page
    
        


    async def loading_page_size(self):
        try:
            endpoint = GetURL(type="psi", url=self.site_url)
            # print("endpoint", endpoint)
            response = HttpRequestHandler(endpoint)
            data = response.json()
            page_size = data.get("loadingExperience", {}).get("metrics", {}).get("FIRST_CONTENTFUL_PAINT_MS")

            # print("page size data", page_size)

            if len(page_size) > 0:
                self.page_size_loading = {
                    "status": True,
                    "reason": str(page_size)
                }
                # print("page_size", page_size)

            else:
                self.page_size_loading = {
                    "status": False,
                    "reason": str(page_size)
                }
        except Exception as error:
            # print("wor3")
            LogEvent(self.queue_item, "loading_page_size error", LogEvent.ERROR)
            
            this_function_name = sys._getframe().f_code.co_name
            Error(error, self.__class__.__name__, this_function_name)
        if self.page_size_loading =={}:
            self.page_size_loading = {
                    "status": False,
                    "reason": "The website did'nt allow to get page size there can be firewall."
                }   
        return self.page_size_loading

    async def minimize_numbers_requests(self):
        try:
            endpoint = GetURL(type="psi", url=self.site_url)
            # print("endpoint", endpoint)
            response = HttpRequestHandler(endpoint)
            data = response.json()
            minimize_requests = data.get("lighthouseResult", {}).get("audits", {}).get("diagnostics")
            # print("minimize_requests", minimize_requests)

            if len(minimize_requests) > 0:
                self.minimize_request = {
                    "status": True,
                    "reason": str(minimize_requests)
                }
            else:
                self.minimize_request = {
                    "status": False,
                    "reason": str(minimize_requests)
                }

        except Exception as error:
            # print("wor1")
            LogEvent(self.queue_item, "minimize_numbers_requests error", LogEvent.ERROR)
            
            this_function_name = sys._getframe().f_code.co_name
            Error(error, self.__class__.__name__, this_function_name)
        if self.minimize_request == {}:
            self.minimize_request = {
                    "status": False,
                   "reason": "Firewall blocked the website for found that website has minimum 1 request and maximum 10 request."
                }
        return self.minimize_request


    async def RenderTime(self):
        try:
            result = self.lighthouse['audits']['interactive']['displayValue']
            self.render_time = {
                "status":True,
                "reason":str(result)
            }
        except Exception as error:
            self.render_time = {
                "status":False,
                "reason":"The website does'nt have any Render time"
            }
        return self.render_time
    
    async def CDNPerformace(self):
        try:
            def LinkPooler(link):
                if len(re.findall("(?:http|https).*(cdn.|static.)",link['data'],re.IGNORECASE)) > 0:
                    self.cdn_performance = {
                        "status":True,
                        "reason":str(re.findall("(?:http|https).*(cdn.|static.)",link['data'],re.IGNORECASE))
                    }        
            if len(re.findall("(?:http|https).*(cdn.|static.)",self.sv_m['dump'],re.IGNORECASE)) > 0:
                self.cdn_performance = {
                    "status":True,
                    "reason":str(re.findall("(?:http|https).*(cdn.|static.)",self.sv_m['dump'],re.IGNORECASE))
                }
            if len(self.cdn_performance) == 0:
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(LinkPooler, self.link_collection)
                

        except Exception as error:
            # print("wor1")
            LogEvent(self.queue_item, "CDNPerformace error", LogEvent.ERROR)
            
            this_function_name = sys._getframe().f_code.co_name
            Error(error, self.__class__.__name__, this_function_name)
        if len(self.cdn_performance) == 0:
            self.cdn_performance = {
                "status":False,
                "reason":"The website did'nt found any CDN or third party scripts."
            }
        return self.cdn_performance
    

    async def MobileFriendly(self):
        try:
            mobile_test = self.mobile_insight['loadingExperience']['metrics']
            self.mobile_friendly = mobile_test
        except Exception as error:
            # print("wor1")
            LogEvent(self.queue_item, "MobileFriendly error", LogEvent.ERROR)
            
            this_function_name = sys._getframe().f_code.co_name
            Error(error, self.__class__.__name__, this_function_name)
        if len(self.mobile_friendly) == 0:
            self.mobile_friendly = {
                "status":False,
                "reason":{}
            }
        return self.mobile_friendly
