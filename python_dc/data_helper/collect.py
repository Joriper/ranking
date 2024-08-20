from helpers.parser.parser import Parser
import datetime,sys,re
from helpers.requester.requester import HttpRequestHandler
from helpers.urls.urls import GetURL
from db.connection import *
from concurrent.futures import ThreadPoolExecutor
from error.error import Error
from selenium import webdriver
from db.connection import *
from error.error import Error
from helpers.urls.urls import GetURL
import requests
import textstat
from bs4 import BeautifulSoup
import pandas as pd
from serpapi import GoogleSearch
import json,bson
import googlemaps
from statistics import median
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from logger.json_logger import LogEvent


class NIC_TransporterDataCollectionHandler:
    def __init__(self,**kwargs):
        self.site_url=kwargs['site_url']
        self.site_host=kwargs['site_host']
        self.site_id = kwargs['site_id']
        self.queue_id = kwargs['queue_id']
        self.rand_id = kwargs['random_id']
        self.site_name = kwargs['site_name']
        self.queue_item = kwargs['queue_item']
        self.error_404_500 = ''
        self.result = []


    async def Transport(self):
        links = []
        datacol=[]
        LogEvent(self.queue_item, "entered transporter data collector", LogEvent.INFO)
        try:
            LogEvent(self.queue_item, "making request", LogEvent.INFO)
            self.sv_m = str(HttpRequestHandler(self.site_url).text)
            LogEvent(self.queue_item, "request success", LogEvent.INFO)
        except:
            LogEvent(self.queue_item, "exception occurred. putting item as processed. Exiting", LogEvent.ERROR)

            queue_collection.update_one({"_id":bson.ObjectId(str(self.queue_id))},{"$set":{"processed":2,"status":"error"}})
            
            sys.exit()
        LogEvent(self.queue_item, "Fetching SiteMap", LogEvent.INFO)
        
        sitemap = HttpRequestHandler(self.site_url+"/sitemap.xml").text
        try: 
            LogEvent(self.queue_item, "Looking error page 404 / 500, requesting wrong URL", LogEvent.INFO)
            self.error_404_500 = HttpRequestHandler(self.site_url+"/VBlIUVWFUXPOWYFHXGJWGBBV").text
        except:
            pass
        try:
            LogEvent(self.queue_item, "checking insights", LogEvent.INFO)
            self.insight = HttpRequestHandler(GetURL(type="normal",url=self.site_url)).json()
        except:
            self.insight = {}
        try:
            LogEvent(self.queue_item, "checking accessiblity", LogEvent.INFO)
            self.accessiblity = HttpRequestHandler(GetURL(type="access",url=self.site_url)).json()
        except:
            self.accessiblity = {}


        try:
            LogEvent(self.queue_item, "mobile insight", LogEvent.INFO)
            self.mobile_insight = HttpRequestHandler(GetURL(type="mobile",url=self.site_url)).json()
        except:
            self.mobile_insight = {}

        dump_helper = {"site_url":self.site_url,"timestamp":str(datetime.datetime.now()).split(" ")[-1].split(".")[0],"created_at":str(datetime.datetime.now()).split(" ")[0],"dump":self.sv_m,"sitemap":sitemap,"error_400_500":self.error_404_500,"id":self.rand_id,"queue_id":self.queue_id}

        page_speed = {"queue_id":self.queue_id,"site_id":self.site_id,"access":self.accessiblity,"insights":self.insight,"created_at":str(datetime.datetime.now()).split(" ")[0],"id":self.rand_id}

        def HandleLinks(tmp_data):
            link_handler=Parser(tmp_data).find_all(lambda x: x.name == "a" and "href" in x.attrs and not (".pdf" in x.get("href") or ".pps" in x.get("href") or ".jpeg" in x.get("href") or ".jpg" in x.get("href") or ".svg" in x.get("href") or ".mp3" in x.get("href") or ".mp4" in x.get("href") or ".m4v" in x.get("href"))  and (x.get("href").startswith("/") or re.findall("^(https|http)://(www.{}|{}|[A-Za-z/{}])".format(self.site_host,self.site_host,self.site_host),str(x.get("href")))))

            try:
                for link in link_handler:
                    if link.get("href").startswith("/"):
                        links.append(self.site_url.strip("/")+link.get("href"))
                    else:
                        links.append(link.get("href"))
            except Exception as error:
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
        LogEvent(self.queue_item, "Initiating HandleLinks", LogEvent.INFO)

        HandleLinks(self.sv_m)
        
        ################## SEO LINK INSERTS top 10 ##################
            
        LogEvent(self.queue_item, "SEO LINK INSERTS top 10", LogEvent.INFO)
        setting_dump = str(os.popen("timeout 1m seoanalyze {}".format(self.site_url)).read())

        temp_obj_dump = {
            "sitename":self.site_name,
            "site_url":self.site_url,
            "site_id":self.site_id,
            "id":self.queue_id,
            "seo_dump":setting_dump,
            "processed":0,
            "created_at":str(datetime.datetime.now()),
            "category":["seo"]            
        }
        LogEvent(self.queue_item, "SEO DUMPS", LogEvent.INFO)

        seo_dump.insert_one(temp_obj_dump)
        
        if len(list(set(links))) > 10:
            top_10_links = list(set(links))[0:10]
        
        else:
            try:
                LogEvent(self.queue_item, "Chrome Webdriver arguments ", LogEvent.INFO)
                chrome_options = webdriver.ChromeOptions()        
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-setuid-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--ignore-ssl-errors=yes')
                chrome_options.add_argument("--headless")
                chrome_options.add_argument('--ignore-certificate-errors')
                LogEvent(self.queue_item, "Chrome Webdriver Initiating", LogEvent.INFO)
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                LogEvent(self.queue_item, "Chrome Webdriver URL Requested", LogEvent.INFO)
                
                driver.get(self.site_url)     
                LogEvent(self.queue_item, "Chrome Webdriver URL HandleLinks", LogEvent.INFO)
                       
                HandleLinks(str(driver.page_source))
                top_10_links = list(set(links))[0:10]
            except Exception as error:
                LogEvent(self.queue_item, "Chrome Webdriver URL HandleLinks", LogEvent.ERROR)
                top_10_links = []
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)



        temp_obj = {
            "sitename":self.site_name,
            "site_url":self.site_url,
            "site_id":self.site_id,
            "id":self.queue_id,
            "top_links":top_10_links,
            "top_10_sem_link":"",
            "processed":0,
            "created_at":str(datetime.datetime.now()),
            "category":["seo"]            
        }
   
        # Get Images

        LogEvent(self.queue_item, "fetching image", LogEvent.DEBUG)

        get_image = Parser(self.sv_m).find_all("img",attrs={"src":True})
        seo_nic.insert_one(temp_obj)


        def Pooler(link):
            try:
                result = HttpRequestHandler(link).text
                return {"url":self.site_url,"link":link,"data":str(result),"created_at":str(datetime.datetime.now()).split(" ")[1],"id":self.rand_id,"queue":self.queue_id,"children":[]}
            except Exception as error:
                this_function_name = sys._getframe(  ).f_code.co_name
                Error(error,self.__class__.__name__,this_function_name)
                return {}
            
        with ThreadPoolExecutor(max_workers=5) as executor:
            LogEvent(self.queue_item, "Pool Executor", LogEvent.DEBUG)

            for data in executor.map(Pooler,links[0:20]):
                self.result.append(data)


        for data in self.result:
            if len(data.values()) > 0:
                datacol.append(data)

        LogEvent(self.queue_item, "Data APpended", LogEvent.DEBUG)

        return {
            "dump_links":datacol,
            "page_speed":page_speed,
            "dump_helper":dump_helper,
            "link_data":links,
            "images":get_image,
            "top_links":top_10_links,
            "mobile_insight":self.mobile_insight,
            "seo_urls":[]
        }

class SerpCollectionHandler:
    def __init__(self,**kwargs):
        self.site_url=kwargs['site_url']
        self.site_host=kwargs['site_host']
        self.site_id = kwargs['site_id']
        self.queue_id = kwargs['queue_id']
        self.rand_id = kwargs['random_id']
        self.site_name = kwargs['site_name']

    def serp(self,query, num_results, api_key):
        params = {
            "q": query,
            "location": "United States",
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "device": "desktop",
            "num": num_results,
            "api_key": api_key}

        search = GoogleSearch(params)
        results = search.get_dict()

        return results
    
    def get_serp_comp(self,results, mydomain):
        serp_links = []
        mydomain_url = "n/a"
        mydomain_rank = "n/a"

        for count, x in enumerate(results["organic_results"], start=1):
            serp_links.append(x["link"])

            if mydomain in x["link"]:
                mydomain_url = x["link"]
                mydomain_rank = count

        return serp_links, mydomain_url, mydomain_rank
    

    def get_reading_level(self,serp_links,mydomain):
        reading_levels = []
        reading_times = []
        word_counts = []
        mydomain_reading_level= "n/a"
        mydomain_reading_time= "n/a"
        mydomain_word_count= "n/a"
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

        for x in serp_links:
            res = requests.get(x,headers=headers)
            html_page = res.text

            soup = BeautifulSoup(html_page, 'html.parser')
            for tag in soup(["script", "noscript","nav","style","input","meta","label","header","footer","aside",'head']):
                tag.decompose()
            page_text = (soup.get_text()).lower()

            reading_level = int(round(textstat.flesch_reading_ease(page_text)))
            reading_levels.append(reading_level)

            reading_time = textstat.reading_time(page_text, ms_per_char=25)
            reading_times.append(round(reading_time/60))

            word_count = textstat.lexicon_count(page_text, removepunct=True)
            word_counts.append(word_count)

            if mydomain in x:
                mydomain_reading_level = int(round(reading_level))
                mydomain_reading_time = round(reading_time/60)
                mydomain_word_count = word_count

        reading_levels_mean = median(reading_levels)
        reading_times_mean = median(reading_times)
        word_counts_median = median(word_counts)

        return reading_levels, reading_times, word_counts, reading_levels_mean, reading_times_mean, word_counts_median, mydomain_reading_level, mydomain_reading_time, mydomain_word_count
    

    def InitializeSerp(self):
        set_actual=[]
        try:
            keyword=self.site_host
            num_results = 10
            mydomain=self.site_host
            mydomain_url = self.site_url
            results = self.serp(keyword,num_results,"5165f037947e017b4a256eb02100d10f7fefc06553d16c9497018d5177bf6218")
            links, mydomain_url, mydomain_rank = self.get_serp_comp(results,mydomain)
            reading_levels, reading_times, word_counts, reading_levels_mean, reading_times_mean, word_counts_median, mydomain_reading_level, mydomain_reading_time, mydomain_word_count = self.get_reading_level(links,mydomain)

            
            reading_ease_data = len(links) - len(reading_levels)
            word_count_data = len(links) - len(word_counts)
            reading_time_data = len(links) - len(reading_times)

            for test_data in range(reading_ease_data):
                reading_levels.append(0)

            for test_dump in range(word_count_data):
                word_counts.append(0)

            for read_data in range(reading_time_data):
                reading_times.append(0)

            for url,time,word,ease in zip(links,reading_times,word_counts,reading_levels):
                set_actual.append({"url":url,"reading_time":time,"word_count":word,"reading_ease":ease})
            seo_nic.update_one({"id":self.queue_id},{"$set":{"seo_urls":set_actual}})
            print(set_actual)
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if len(set_actual) == 0:
            seo_nic.update_one({"id":self.queue_id},{"$set":{"seo_urls":[]}})



class Google_maps_details:
    def __init__(self,**kwargs):
        self.site_url=kwargs['site_url']
        self.site_host=kwargs['site_host']
        self.site_id=kwargs['site_id']
        self.site_name=kwargs['site_name']
        self.queue_id=kwargs['queue_id']
        self.queue_item = kwargs['queue_item']
        self.details = {}
    async def get_place_id(self):
        try:
            gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAPS_APIKEY"))
            places = gmaps.find_place(input= self.site_url, input_type="textquery")
            if places['status'] == 'OK' and places['candidates']:
                return places['candidates'][0]['place_id']
            else:
                return None
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name) 

    async def get_place_details(self):
        try:
            LogEvent(self.queue_item, "process initiated get_place_details", LogEvent.INFO)
            
            place_id = await self.get_place_id()
            if place_id:
                data = HttpRequestHandler(GetURL(type="google_maps", place_id = place_id, api_key = os.environ.get("GOOGLE_MAPS_APIKEY")))
                if data.ok:
                    self.details = {
                        "status": True,
                        "reason":data.json()
                    }
                    print("self details",self.details)
                else:
                    self.details = {
                        "status": False,
                        "reason": data.json()
                    }
                base_store = {
                    "id" : self.queue_id,
                    "sitename": self.site_name,
                    "site_id": self.site_id,
                    "siteurl": self.site_url,
                    "googlemap_details":self.details,
                    "created_at":str(datetime.datetime.now()),
                    "processed": 0

                }
                googlemaps_details.insert_one(base_store)
                LogEvent(self.queue_item, "process Over", LogEvent.INFO)
                
                return self.details
        except Exception as error:
            LogEvent(self.queue_item, "process Exception", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name) 

