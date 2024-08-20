from helpers.requester.requester import HttpRequestHandler
from concurrent.futures import ThreadPoolExecutor
from colorthief import ColorThief
import numpy as np
import datetime,re,json,sys
from db.connection import *
from helpers.parser.parser import Parser
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from error.error import Error
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from logger.json_logger import LogEvent


class Seo:
    def __init__(self,**kwargs):
        self.seo_questions = {}
        self.seo_consistency = {}
        self.heading_optmize = {}
        self.over_optimization = {}

        self.site = kwargs['site']
        self.sitename =self.site['name']        
        self.reco_id = str(self.site['_id'])
        self.url_structure=""
        self.top_links = kwargs['collected']['top_links']
        self.sv_m = kwargs['collected']['dump_helper']
        self.queue_item = kwargs['queue_item']
        

    async def HeadingOptimization(self):
        try:
            h6 = Parser(self.sv_m['dump']).find_all("h6")
            h5 = Parser(self.sv_m['dump']).find_all("h5")
            h4 = Parser(self.sv_m['dump']).find_all("h4")
            h3 = Parser(self.sv_m['dump']).find_all("h3")
            h2 = Parser(self.sv_m['dump']).find_all("h2")
            h1 = Parser(self.sv_m['dump']).find_all("h1")

            if len(h1) > 1:
                if h1[-1].find_all_next(lambda x: x.name == "h2" or x.name == "h3" or x.name == "h4" or x.name == "h5" or x.name == "h6") != None:
                    if h2[-1].find_all_next(lambda x: x.name == "h2" or x.name == "h3" or x.name == "h4" or x.name == "h5" or x.name == "h6") != None:
                        if h3[-1].find_all_next(lambda x: x.name == "h3" or x.name == "h4" or x.name == "h5" or x.name == "h6") != None:
                            if h4[-1].find_all_next(lambda x: x.name == "h4" or x.name == "h5" or x.name == "h6") != None:
                                if h5[-1].find_all_next(lambda x: x.name == "h5" or x.name == "h6") != None:
                                    if h6[-1].find_all_next(lambda x: x.name == "h6") != None:
                                        self.heading_optmize = {
                                            "status":True,
                                            "reason":"The website have optimized headings because {},{},{},{},{},{}".format(h1[-1],h2[-1],h3[-1],h4[-1],h5[-1],h6[-1]),
                                            "data":{
                                                "h1":str(h1[-1]),
                                                "h2":str(h2[-1]),
                                                "h3":str(h3[-1]),
                                                "h4":str(h4[-1]),
                                                "h5":str(h5[-1]),
                                                "h6":str(h6[-1]),
                                            }
                                        }

            else:
                self.heading_optmize = {
                    "status":False,
                    "reason":"The website look like does'nt have any optimized heading structure.",
                    "data":{
                        "h1":"",
                        "h2":"",
                        "h3":"",
                        "h4":"",
                        "h5":"",
                        "h6":""
                    }
                }
        except Exception as error:
            LogEvent(self.queue_item, "HeadingOptimization", LogEvent.ERROR)
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)
        if len(self.heading_optmize) == 0:
            self.heading_optimize = {
                "status":False,
                "reason":"The website did'nt allow to track the Heading optimizations for ranking or  protection by catpcha or any firewall.",
                "data":{
                    "h1":"",
                    "h2":"",
                    "h3":"",
                    "h4":"",
                    "h5":"",
                    "h6":""
                }
            }

        return self.heading_optmize


    async def SeoQuestions(self):
        site_id = str(self.site['site_id'])
        siteurl = str(self.site['url'])

        if "https" in siteurl or  "http" in siteurl:
            site_host = siteurl.split("://")[1].split("/")[0]
            seo_data_handle = list(seo_dump.find({"id":str(self.site['_id'])}))

            ########################### SEO OPTIMIZATION ##################
            title_obj,meta_obj,content_freshness,image_optimization,schema_markup,check_https,keyword_optimize = {},{},{},{},{},{},{}
            try:
                if len(seo_data_handle) > 0:
                    if len(seo_data_handle[-1]['seo_dump']) > 0:
                        seo_data = json.loads(seo_data_handle[-1]['seo_dump'])


                        title_optimization = seo_data['pages'][0]['title']
                        if len(re.findall("[A-Z].*|.*",title_optimization,re.IGNORECASE)) > 0 and len(str(title_optimization)) >= 10 and len(str(title_optimization)) <=70: #and len(list(set(str(title_optimization).split("|")))) == len(title_optimization.split("|")):
                            title_obj['status'] = True
                            title_obj['reason'] = "The website is optimized with title because {}".format(str(title_optimization))
                            title_obj['data']=str(title_optimization)
                        else:
                            title_obj['status'] = False
                            title_obj['reason'] = "The website does'nt have any optimization for title",
                            title_obj['data']=str(title_optimization)

                        meta_description = [description for description in seo_data['pages'] if description['description'] !=""]
                        if len(meta_description) > 0:
                            for meta in meta_description:
                                if len(meta['description']) >=150 and len(meta['description']) <=160 and len([get_keyword for get_keyword in meta if str(get_keyword[1]) in meta['description']]) >0:
                                    meta_obj['status']=True
                                    meta_obj['reason'] = "The website have meta <meta> description optimization because '{}'".format(str(meta['description']))
                                    meta_obj['data']= {
                                        "meta_description":str(meta['description']),
                                        "meta_keywords":str(meta['keywords'])
                                    }
                                    break
                        
                        if len(meta_obj.keys()) == 0:
                            meta_obj['status']=False
                            meta_obj['reason'] = "The website look like does'nt have any meta optimization.",
                            meta_obj['data']=str(meta_description)

                        content_ = [result['bigrams'] for result in seo_data['pages'] if "regular updates" or "communication regular updates" in result['bigrams']]
                        if len(content_) > 0:
                            content_freshness['status'] =True
                            content_freshness['reason']="The website regularly updates its content, ensuring freshness and relevance.",
                            content_freshness['data']=content_[-1]
                        else:
                            content_freshness['status'] =False
                            content_freshness['reason']=str(content_),
                            content_freshness['data']="The website not regularly updates its content, ensuring freshness and relevance."

                        image_optimize = [images['warnings'] for images in seo_data['pages'] if len(re.findall("Image missing alt tag",str(images['warnings']),re.IGNORECASE)) > 0]
                        if len(image_optimize) > 0:
                            image_optimization['status']=True
                            image_optimization['reason']="The website employs image optimization techniques including filename and alt attributes , enhancing accessibility in SEO."
                            image_optimization['data']=str(image_optimize)
                        else:
                            image_optimization['status']=False
                            image_optimization['reason']="The website does'nt have any optimization for image"
                            image_optimization['data']=str(image_optimization)

                        #implemting schema markup
                        telephone = [get_telephone for get_telephone in seo_data['pages'][0]['warnings'] if "tel:" in  get_telephone]
                        email_address  = [get_email for get_email in seo_data['pages'][0]['warnings'] if "mailto:" in  get_email]
                        
                        get_url = seo_data['pages'][0]['url']
                        get_type = title_optimization.replace("|",",")
                        telphone_get = telephone[-1].split(":")[-1] if len(telephone) > 0 else False
                        email_get = email_address[-1].split(":")[-1] if len(email_address) > 0 else False

                        schema_markup['url']=get_url
                        schema_markup['type']=get_type
                        schema_markup['telephone']=telphone_get
                        schema_markup['email']=email_get


                        # Ensure HTTPS Connection
                        http_handle =[http_link.split(" ")[-1] for http_link in seo_data['pages'][0]['warnings'] if "https" in http_link]
                        if len(http_handle) > 0:
                            check_https['status']=True
                            check_https['reason']="The website have HTTPS Connection because or TLS Layer Security"
                            check_https['data']=str(http_handle)
                        else:
                            check_https['status']=False
                            check_https['reason']="The website does'nt have any HTTPS Connection"
                            check_https['data']=str(http_handle)

                        # keyword optmization
                            
                        for page in seo_data['pages']:
                            if len(page['keywords']) > 0:
                                for words in page['keywords']:
                                    if str(words[-1]) in page['title'] and str(words[-1]) in page['description']:
                                        keyword_optimize['status']=True                                        
                                        keyword_optimize['reason']="The website have keyword optimized because {}".format(words)
                                        keyword_optimize['data']={
                                            "page_title":page['title'],
                                            "page_description":page['description']
                                        }
                                        break
                        if len(keyword_optimize.keys()) == 0:
                            keyword_optimize['status']=False
                            keyword_optimize['reason']="The website does'nt have optimization",
                            keyword_optimize['data']={
                                "page_title":page['title'],
                                "page_description":page['description']
                            }                            


            except Exception as error:
                LogEvent(self.queue_item, "SeoQuestions", LogEvent.ERROR)
                
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)    

            self.seo_questions = {
                "sitename":self.sitename,
                "site_url":siteurl,
                "site_id":site_id,
                "id":self.reco_id,
                "seo_slu_":{
                    "title_optimization":title_obj if len(title_obj) else {"status":False,"reason":"The website did'nt allow to track the title optimization"},
                    "meta_optimize":meta_obj if len(meta_obj) else {"status":False,"reason":"The website does'nt allow to get optmized meta."},
                    "fresh_content":content_freshness if len(content_freshness) else {"status":False,"reason":"The website does'nt allow to get the fresh content."},
                    "image_optimization":image_optimization if len(image_optimization) else {"status":False,"reason":"The website does'nt allow to check optimized images."},
                    "schema_markup":schema_markup,
                    "enable_https":check_https if len(check_https) else {"status":False,"reason":"The website does'nt allow to check HTTPS Enabled. "},
                    "keyword_optimize":keyword_optimize if len(keyword_optimize) else {"status":False,"reason":"The website does'nt allow to get optmized keywords."},
                },
                "created_at":str(datetime.datetime.now()),
                "category":["seo"]                    
            }
        return self.seo_questions



    async def Over_optimization(self):

        try:
            os.popen("timeout 1m seoanalyze {} > test.json".format(self.site['url'])).read()
            data = json.load(open("test.json"))

            if os.path.exists("test.json") and len(data['pages']) > 0:
                all_iters = []
                get_keywords = [get_key['keywords'] for get_key in data['pages'] if len(get_key['keywords']) > 0]
                for first_iter in get_keywords:
                    for second_iter in first_iter:
                        all_iters.append(second_iter)

                total_keywords_occurrences = sum(count[0] for count in all_iters)
                keyword_density = [(word, count / total_keywords_occurrences * 100) for count, word in all_iters]
                high_density_keywords = [(word, density) for word, density in keyword_density if density > 5]
                try:
                    diversity_ratio = len(high_density_keywords) / len(keyword_density)    
                except:
                    diversity_ratio = 0

                # for word, density in keyword_density:
                #     print(f"{word}: {density:.2f}%")

                # if high_density_keywords:
                #     print("\nPotential Keyword Stuffing (High Density Keywords):")
                #     for word, density in high_density_keywords:
                #         print(f"{word}: {density:.2f}%")
                # else:
                #     print("\nNo keywords with unusually high density.")

                if len(high_density_keywords) > 0 or diversity_ratio > 0.1:  # Adjust the threshold based on your SEO strategy.
                    self.over_optimization= {
                        "status":False,
                        "reason":"The website look like does'nt over optimized for diversity ratio {}".format(diversity_ratio),
                        "data":{"words":high_density_keywords,"diversity_ratio":diversity_ratio,"keyword_density":keyword_density,"total_keyword":total_keywords_occurrences}
                    }
                else:
                    self.over_optimization= {
                        "status":True,                        
                        "data":{"words":high_density_keywords,"diversity_ratio":diversity_ratio,"keyword_density":keyword_density,"total_keyword":total_keywords_occurrences},
                        "reason":"The website is over optimized for diversity ratio is {}".format(diversity_ratio)
                    }

        except Exception as error:
            LogEvent(self.queue_item, "Over_optimization", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)  
        try:
            os.remove("test.json")
        except:
            pass
        if len(self.over_optimization) == 0:
            self.over_optimization = {
                "status":False,
                "reason":"The website did'nt allow to track the Seo optimizations. please try again latter",
                "data":{}
            }
        return self.over_optimization
    
    async def URL_Structure(self):
        site_host = self.site['url'].split("://")[1].split("/")[0]
        all_links = []
        handle_url = Parser(self.sv_m['dump']).find_all("a",href=re.compile("^https|http.*{}".format(self.site_host)))
        
        if len(handle_url) > 0:
            for links in handle_url:
                if len(re.findall("^(?:http://|https://){}.*/[A-Za-z].*".format(self.site['url']),links.get("href"),re.IGNORECASE)) > 0:

                    self.url_structure = {
                        "status":True,
                        "reason":"The website has optimized url structure because {}".format(links.get("href")),
                        "data":links[0:10]

                    }
                    break
            if len(self.url_structure) > 0:
                self.url_structure = {
                    "status":False,
                    "reason":"The website does'nt have any optimized url",
                    "data":all_links[0:10]
                }
        else:
            self.url_structure = {
                "status":False,
                "reason":"The website did'nt allow to track the functionality",
                "data":all_links[0:10]
            }
        self.url_structure
