from helpers.parser.parser import Parser
import requests,re,sys,threading
import random,sys,os,re
from error.error import Error
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from translate import Translator
from selenium import webdriver
from db.connection import *
from helpers.urls.urls import GetURL
from helpers.requester.requester import HttpPostRequestHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import re,sys,os,pytesseract
from db.connection import *
from helpers.requester.requester import HttpRequestHandler
from helpers.byte_converter.bytes import convert_bytes


def get_broken_links(domain,url):
    broken_links = []
    valid_link = []
    try:
        root_domain = domain

        def _validate_url(url):
            r = requests.head(url)
            if r.status_code == 404:
                broken_links.append(url)
            else:
                valid_link.append(url)
                
        data = requests.get(url,verify=False).text
        soup = Parser(data)
        links = [link.get("href") for link in soup.find_all("a") if f"//{root_domain}" in link.get("href")]
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(_validate_url, links)
        if len(broken_links) > 0:
            return {
                "status":False,
                "reason":"The website does have broken link"
            }
        else:
            return {
                "status":True,
                "reason":str(broken_links)
            }
    except Exception as error:
        pass
    return broken_links



def BackLinkHandler(url,host,req):
    dmp,backlink_collection,authentication,follow,nofollow =[],[],0,[],[]
    
    req = HttpRequestHandler(url)
    
    form_type,image_type,frame_type,text_type=[],[],[],[]
    handle_parser = Parser(req.text)

    links=handle_parser.find_all(lambda x: x.name == "a" and "href" in x.attrs and not (".pdf" in x.get("href") or ".pps" in x.get("href") or ".jpeg" in x.get("href") or ".jpg" in x.get("href") or ".svg" in x.get("href") or ".mp3" in x.get("href") or ".mp4" in x.get("href") or ".m4v" in x.get("href"))  and (x.get("href").startswith("/") or re.findall("^(https|http).*{}".format(host),str(x.get("href")))))

    if links != None:
        for link in links:
            backlink = ""
            if "https" in link.get("href") or "http"  in link.get("href"):
                backlink=link.get("href")
            else:
                backlink=url+link.get("href")        
            dmp.append(backlink)

        def Pooler(urls):
        
            handle_par = Parser(HttpRequestHandler(urls).text)
            linkss = handle_par.find_all("a")
            title = handle_par.find("title").text

            for data in linkss:
                bclink = ""
                if len(re.findall("http|https",data.get("href"))) > 0:
                    bclink=data.get("href")
                else:
                    bclink=url+bclink


                backlink_collection.append({"link":bclink,"anchorText":data.text.strip()})

                if data.get("rel"):
                    nofollow.append(1)
                else:
                    follow.append(1)


            
            
            form_type.append(len(handle_par.find_all("form")))
            
            image_type.append(len(handle_par.find_all("img")))

            frame_type.append(len(handle_par.find_all("iframe")))
            
            if len(handle_par.find_all("form")) == 0 and  len(handle_par.find_all("img")) == 0 and len(handle_par.find_all("iframe")) == 0:
                text_type.append(len(handle_par.text))
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(Pooler, dmp)


    form_link_per = sum(form_type)/len(dmp)*100
    img_link_per = sum(image_type)/len(dmp)*100
    text_link_per = sum(text_type)/len(dmp)*100
    frame_link_per = sum(frame_type)/len(dmp)*100

    return {
        "backlink":len(backlink_collection),
        "auth":authentication,
        "backlink_collection":backlink_collection[0:50],
        "percentage":{"follow":len(follow)/len(backlink_collection)*100,"nofollow":len(nofollow)/len(backlink_collection)*100},
        "backlink_types_per":{"form":form_link_per,"frame":frame_link_per,"text":text_link_per,"img":img_link_per}
    }

class Navigation:
    def __init__(self,**kwargs):
        self.site_url=kwargs['site_url'].strip("/")
        self.site_host=kwargs['site_host']
        self.lighthouse=kwargs['lighthouse']
        self.across_site_domain=False
        self.backlink = None
        self.total_requests=0
        self.correct_title_page=False
        self.codes=None
        self.site_map=False
        self.insight_id = kwargs['random_id']
        self.click_depth_range="No Given Page found"
        self.sv_m = kwargs['sv_m']['dump_helper']
        self.link_collection = kwargs['sv_m']['dump_links']
        self.error_content = kwargs['sv_m']['dump_helper']['error_400_500']

        self.code_404_500=False
        self.link_disti=False
        self.is_bread_crumb=False
        self.home_page_linked=False
        self.faq_question=False
        self.static=[]
        self.broken_link=False
        self.queue_item = kwargs['queue_item']
    
    
    async def has_site_map(self):
        try:
            if len(re.findall("<?xml version",str(self.sv_m['sitemap']))) > 0:
                self.site_map={
                    "status":True,
                    "data":str(self.sv_m['sitemap']),
                    "reason":"The website have a sitemap.",
                }
            else:
                self.site_map={
                    "status":False,
                    "data":"",
                    "reason":"The website does'nt have any sitemap"
                }
            sitemap_data = Parser(self.sv_m['dump']).find_all("a",attrs={"href":re.compile("sitemap|site-map|site_map",re.IGNORECASE)})
            sitemap_text = Parser(self.sv_m['dump']).find_all("a",string=re.compile("sitemap|site-map|site_map",re.IGNORECASE))

            if len(sitemap_data) > 0  or len(sitemap_text) > 0:
                self.site_map={
                    "status":True,
                    "reason":"The website have a sitemap.",
                    "data":str([sitemap_data,sitemap_text])
                }


        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.site_map == False:
            self.site_map ={
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of sitemap look like blocked by firewall."
            }             
        return self.site_map
        


    async def has_faq(self,run_type):
        try:
            def GraphNormal(data_collection):
                result = []
                def Faq(link):
                    data = link['data']
                    pattern = r'''
                    (?i)                        # Case-insensitive mode
                    (
                      faq                       # Match 'faq'
                      |freq(uently)?(-| )?asked(-| )?questions?  # Match 'frequently-asked-questions' with optional parts
                      |freq(uent)?(.+)?quest(ions?)?  # Match 'frequent', 'frequently', 'questions', etc., with any characters in between
                    )
                    '''
                    if len(re.findall(pattern,str(data), re.IGNORECASE)) > 0:
                    # if len(re.findall("(frequently-asked-questions|faq|frequent.*question|frequently.*asked.*question|freq.*quest|freq)",str(data),re.IGNORECASE)) > 0:

                        self.faq_question={
                            "status":True,
                            "data":str(re.findall(pattern,str(data),re.IGNORECASE)),
                            "reason":"The website provides a FAQ section to address common queries for users."
                        }
                    
                        
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(Faq, data_collection)

                if self.faq_question == False:
                    self.faq_question={
                        "status":False,
                        "reason":"The website doesn't feature an FAQ section for addressing common queries.",
                        "data":""
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.link_collection)
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.faq_question == False:
            self.faq_question={
                "status":False,
                "reason":"The website didn't allow to track the FAQ Pages whether present or not."
            }
        return self.faq_question


    async def bread_crumb(self,run_type):
        try:
            def GraphNormal(data_collection,url):
                def Pooler(link):
                    data = Parser(link['data']).text
                    if len(re.findall(">",str(data),re.IGNORECASE)) != 0 or  len(re.findall("»",str(data),re.IGNORECASE)) != 0:
                        self.is_bread_crumb={
                            "status":True,
                            "reason":"The website have a breadcumb",
                            "data":str([str(re.findall(">",str(data),re.IGNORECASE)),str(re.findall("»",str(data),re.IGNORECASE))])
                        }

                data = Parser(self.sv_m['dump'])
                
                if len(re.findall(">",data.text,re.IGNORECASE)) != 0 and len(re.findall("<",data.text,re.IGNORECASE)) !=0:
                    self.is_bread_crumb={
                        "status":True,
                        "reason":"The website have a breadcumb",
                        "data":str([str(re.findall(">",data.text,re.IGNORECASE)),str(re.findall("<",data.text,re.IGNORECASE))])
                    }

                elif len(re.findall("»",data.text,re.IGNORECASE)) != 0:
                    self.is_bread_crumb={
                        "status":True,
                        "reason":"The website have a breadcrumb",
                        "data":str(re.findall("»",data.text,re.IGNORECASE))
                    }
                else:
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(Pooler, data_collection)
                
                if self.is_bread_crumb == False:
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument("--headless=new")
                    chrome_options.add_argument('--ignore-ssl-errors=yes')
                    chrome_options.add_argument('--ignore-certificate-errors')
                    chrome_options.add_argument('--disable-gpu')
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-setuid-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                    driver.get(url)
                    executor_script = "window.getComputedStyle(document.querySelector('ul li:nth-child(2)'),'::before').content"
                    if "|" or "»" or ">"  in executor_script:
                        self.is_bread_crumb={
                            "status":True,
                            "reason":"The website have a breadcumb",
                            "data":str(executor_script)
                        }
                    
                if self.is_bread_crumb == False:
                    self.is_bread_crumb={
                        "status":False,
                        "data":"",
                        "reason":"The website does'nt have any breadcrumbs"
                    }

            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.link_collection,self.site_url)

        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        if self.is_bread_crumb == False:
            self.is_bread_crumb={
                "status":False,
                "data":"",
                "reason":"The website didn't allow to track the BreadCrumbs whether present or not."
            }
        return self.is_bread_crumb
            
    async def code_count(self):
        try:
            total_request=self.lighthouse['audits']['network-requests']['details']['items']
            code_403,code_200,code_301=0,0,0
            for request in total_request:
                if request['statusCode'] == 200:
                    code_200+=1
                elif request['statusCode']== 301:
                    code_301+=1
                elif request['statusCode'] == 403:
                    code_403+=1
            self.codes={
                "code_403":code_403,
                "code_200":code_200,
                "code_301":code_301,
            }
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
            self.codes={
                "code_403":0,
                "code_200":0,
                "code_301":0,
            }
        return self.codes

    async def total_request(self):
        try:
            total_request=self.lighthouse['audits']['network-requests']['details']['items']
            self.total_requests=len(total_request)
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.total_requests

    async def BackLink(self,run_type):
        def GraphNormal():
            try:
                self.backlink = BackLinkHandler(self.site_url,self.site_host,self.sv_m['dump'])
            except Exception as error:
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal()
        return self.backlink

    async def navigation_cmp_across_site(self,run_type):
        def GraphNormal(data_,data_collection):
            try:
                data =[]
                result = Parser(data_)
                if  len(result.find_all(lambda x: x.name == "a" and "href" in x.attrs and not (".pdf" in x.get("href") or ".pps" in x.get("href") or ".jpeg" in x.get("href") or ".jpg" in x.get("href") or ".svg" in x.get("href") or ".mp3" in x.get("href") or ".mp4" in x.get("href") or ".m4v" in x.get("href"))  and not re.findall("^(https|http).*{}".format(self.site_host),str(x.get("href"))))) > 0:
                    self.across_site_domain={
                        "status":True,
                        "reason":"The website look like have Navigation Accross site.",
                        "data":str(result.find_all(lambda x: x.name == "a" and "href" in x.attrs and not (".pdf" in x.get("href") or ".pps" in x.get("href") or ".jpeg" in x.get("href") or ".jpg" in x.get("href") or ".svg" in x.get("href") or ".mp3" in x.get("href") or ".mp4" in x.get("href") or ".m4v" in x.get("href"))  and not re.findall("^(https|http).*{}".format(self.site_host),str(x.get("href")))))
                    }
                else:
                    def Pooler(link):
                        inter_result = Parser(link['data']).find_all("a",attrs={"href":lambda x : not(str(self.site_host) in x) and len(re.findall("^(htt|https)",x)) > 0})

                        if len(inter_result) > 0:
                            self.across_site_domain={
                                "status":True,
                                "reason":"The website look like have Navigation Accross site.",
                                "data":str(inter_result)
                            }
            
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(Pooler, data_collection)
                    if self.across_site_domain == False:
                        self.across_site_domain={
                            "status":False,
                            "reason":"The website does'nt look like have Navigation Accross site.",
                            "data":str(result)
                        }

            except Exception as error:
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'],self.link_collection) 
        
        if self.across_site_domain ==  False:
            self.across_site_domain = {
                "status":False,
                "data":"",
                "reason":"The website didn't allow to track the external links for website or blocked by firewall."
            }
        return self.across_site_domain
    

    async def homepage_linked(self,run_type):
        try:
            def GraphNormal(data_collection):
                dumb = []
                result = []
                def LinkPooler(link):
                    fnd_home = Parser(link['data']).find_all("a")
                    for data in fnd_home:
                        if len(re.findall("Home.*",data.text,re.IGNORECASE)) > 0 and len(re.findall("^(javascript|#)",data.get("href"),re.IGNORECASE)) == 0:
                            href_link=None
                            if data.get("href").startswith("/"):
                                href_link=self.site_url+data.get("href")
                            else:
                                href_link=data.get("href")
                            dumb.append(True)
                    result.append(str(fnd_home))   

            
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(LinkPooler, data_collection)

                if len(data_collection) == len(dumb):
                    self.home_page_linked={
                        "status":True,
                        "data":str(dumb),
                        "reason":"The website is linked with homepage",
                    }
                else:
                    self.home_page_linked={
                        "status":False,
                        "data":"",
                        "reason":"The website looks missing linked to all pages"
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.link_collection)
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name) 

        if self.home_page_linked ==  False:
            self.home_page_linked = {
                "status":False,
                "data":"",
                "reason":"The website didn't allow to track the All home pages linked to webpages."
            }
        return self.home_page_linked


    async def click_depth(self,run_type):
        try:
            def GraphNormal(data_):
                data = Parser(data_).find_all("a",href=re.compile("about.*"))
                if len(data) > 0 and re.findall("about",data[0].text,re.IGNORECASE):
                    response = None
                    if data[0].get("href").startswith("/"):
                        response=HttpRequestHandler(self.site_url+data[0].get("href"))
                    else:
                        response=HttpRequestHandler(data[0].get("href"))
                    if len(Parser(response.text).find_all(["h1","h2","h3","h4","h5","h6"],string=re.compile("Abou.*",re.IGNORECASE))) > 0:
                        self.click_depth_range={
                            "status":True,
                            "reason":"1 for about page"
                        }
                    else:
                        self.click_depth_range={
                            "status":True,
                            "reason":"more than 1 about page"
                        }
                
                if self.click_depth_range == "No Given Page found":
                    data_x = Parser(data_).find_all("a",string=re.compile("about",re.IGNORECASE))
                    if len(data_x) > 0:
                        result_set = data_x[-1].parent.find_all("li")[-1].find("a").get("href")
                        if not (result_set.startswith("https") and result_set.startswith("http")):
                            result_set = result_set.split("en")[-1] if result_set.startswith("/en") or result_set.startswith("en") else result_set
                            href_ = self.site_url+result_set
                        else:
                            href_ = result_set

                                        
                        respond = HttpRequestHandler(href_)
                        if len(Parser(respond.text).find_all(["h1","h2","h3","h4","h5","h6"],string=re.compile("{}.*".format(data_x[-1].parent.find_all("li")[-1].find("a").text),re.IGNORECASE))) > 0:
                            self.click_depth_range={
                                "status":True,
                                "reason":"1 for about page"
                            }
                        else:
                            self.click_depth_range={
                                "status":True,
                                "reason":"more than 1 about page"
                            }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])

        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
    
        if self.click_depth_range == 'No Given Page found':
            self.click_depth_range={
                "status":False,
                "reason":"No about page"
            }      

        return self.click_depth_range


    async def correct_title(self,run_type):
        try:
            def GraphNormal(data_):
                if Parser(data_).find("title").text != "":
                    self.correct_title_page = {
                        "status":True,
                        "reason":str(Parser(data_).find("title").text)
                    }
                else:
                    self.correct_title={
                        "status":False,
                        "reason":"The website does'nt have any correct title"
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.correct_title_page ==  False:
            self.correct_title_page={
                "status":False,
                "reason":"The website didn't allow to track the Title of website or blocked by firewall for assets protection."
            }
        return self.correct_title_page

    async def link_distiguishable(self,run_type):
        try:
            def GraphNormal(data_):
                data= Parser(data_).find_all("a")
                class_link =[]
                for i in data:
                    class_link.append(i.get("class"))
                if all(i == None for i in class_link) == True:                
                    self.link_disti={
                        "status":False,
                        "reason":"The website doesn't have any distinguishable links or elements",
                        "data":str(data)
                    }
                else:
                    self.link_disti={
                        "status":True,
                        "reason":"The website may have distinguishable links.",
                        "data":str(class_link)
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.link_disti ==  False:
            self.link_disti={
                "status":False,
                "data":"",
                "reason":"The website didn't allow to track the functionality of link distiguishable."
            }
        return self.link_disti



    async def is_nobroken_link(self,run_type):
        def GraphNormal():
            try:
                broken_links=get_broken_links(self.site_host,self.site_url)
                if len(broken_link) == 0:
                    self.broken_link = {
                        "status":True,
                        "reason":"The website does'nt have any broken link",
                        "data":broken_links
                    }
                else:
                    self.broken_link = {
                        "status":False,
                        "reason":"The website may have broken links",
                        "data":broken_links
                    }                    
            except Exception as error:
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal()
        if self.broken_link ==  False:
            self.broken_link={
                "status":False,
                "reason":"The website didn't allow to track the broken links for security reasons.",
                "data":""
            }
            
        return self.broken_link



    async def is_404_500_page(self):
        try:
            code_500_400 = re.findall("500|Internal-server|server error|encountered|404|Not-found|not found|page not found|page-not.*",self.error_content,re.IGNORECASE)
            if len(code_500_400) > 0:
                self.code_404_500={
                    "status":True,
                    "reason":"The website may have Internal Error pages or not Found pages.",
                    "data":str(self.error_content)
                }

            if self.code_404_500 ==  False:
                link = Parser(self.sv_m['dump']).find("a",href=lambda x: not (".pdf" in x or ".pps" in x or ".jpeg" in x or ".jpg" in x or ".svg" in x or ".mp3" in x or ".mp4" in x or ".m4v" in x)  and (x.startswith("/") or re.findall("^(http|https).*{}.*".format(self.site_host),str(x)) and x not in self.site_url))[0]

                href_link=None
                if link.startswith("/"):
                    href_link=self.site_url+link
                else:
                    href_link=link

                data= HttpRequestHandler(href_link+"/LKJLKFJLKJFWW").text
                code_404_500 = re.findall("500|Internal-server|server error|encountered|404|Not-found|not found|page not found|page-not.*",data,re.IGNORECASE)

                if len(code_404_500) > 0:
                    self.code_404_500={
                        "status":True,
                        "reason":"The website may have Internal Error pages or not Found pages.",
                        "data":str(data)
                    }
            if self.code_404_500 ==  False:
                self.code_404_500 = {
                    "status":False,
                    "data":"",
                    "reason":"The website doesn't have any error page or internal server page"
                }

        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        if self.code_404_500 == False:
            self.code_404_500={
                "status":False,
                "data":"",
                "reason":"The website didn't allow to track the Error pages like 404(Not Found) or 500(Internal Server Error)."
            }

        return self.code_404_500

    async def static_assets(self):
        try:
            image_size,javascript_size,css_size,font_size,html_size=0,0,0,0,0
            total_images,total_javascript,total_css,total_html,total_font=0,0,0,0,0
            js_ar,js_thr,img_ar,img_thr,link_ar,link_thr,font_thr=[],[],[],[],[],[],[]
            
            nf=Parser(self.sv_m['dump'])

            def GetRequest(url,type):
                try:
                    cs = HttpRequestHandler(url)
                    csx=0
                    try:
                        csx=cs.headers['Content-Length']
                    except:
                        csx=int(len(str(cs.text)))
                    if type == "js":
                        javascript_size=int(csx)
                        total_javascript=1
                        js_ar.append(javascript_size)
                        js_ar.append(total_javascript)
                    elif type == "img":
                        image_size=int(csx)
                        total_images=1
                        img_ar.append(image_size)
                        img_ar.append(total_images)
                    elif type == "link":
                        css_size=int(csx)
                        total_css=1
                        link_ar.append(css_size)
                        link_ar.append(total_css)
                except Exception as error:
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
                
        
            for js in nf.find_all("script",attrs={"src":False}):
                total_javascript+=1
                javascript_size+=len(js.get_text())
            
            for csx in nf.find_all("script",attrs={"src":True}):
                hoturl = ""
                jsurl = csx.get("src")
                
                if not (jsurl.startswith("https") or jsurl.startswith("http")):
                    hoturl=self.site_url.strip("/")+"/"+jsurl
                else:
                    hoturl=jsurl

                jsth = threading.Thread(target=GetRequest,args=(hoturl,"js"))
                jsth.setDaemon=True
                js_thr.append(jsth)



            for images in nf.find_all("img"):
                hoturl = ""
                imgurl = images.get("src")
                if not (imgurl.startswith("https") or imgurl.startswith("http")):
                    hoturl=self.site_url.strip("/")+"/"+imgurl
                else:
                    hoturl = imgurl
                imgth = threading.Thread(target=GetRequest,args=(hoturl,"img"))
                imgth.setDaemon=True
                img_thr.append(imgth)
            
            for exten in [".ACFM",".AMFM" ".DFON",".EOT",".FNT",".GDR" ,".GTF",".MMM" ,".OTF",".PFA" ,".TPF", ".TTC",".TTF" ]:

                font_js = nf.find_all("script",attrs={"src":re.compile("${}".format(exten.lower()))})
                font_css = nf.find_all("link",attrs={"href":re.compile("${}".format(exten.lower()))})

                if len(font_js) > 0:
                    total_font+=1
                    for result in font_js:
                        href = result.get("src")
                        js_url = ""
                        if not (href.startswith("https") or href.startswith("http")):
                            js_url=self.site_url.strip("/")+"/"+imgurl
                        else:
                            js_url = href                    
                        fonts_js = threading.Thread(target=GetRequest,args=(href,"font_js"))
                        fonts_js.setDaemon=True
                        font_thr.append(fonts_js)
                
                if len(font_css) > 0:
                    total_font+=1
                    for result in font_js:
                        href = result.get("href")
                        css_url = ""
                        if not (href.startswith("https") or href.startswith("http")):
                            css_url=self.site_url.strip("/")+"/"+imgurl
                        else:
                            css_url = href                    
                        fonts_css = threading.Thread(target=GetRequest,args=(href,"font_js"))
                        fonts_css.setDaemon=True
                        font_thr.append(fonts_css)            
                    
            for cs in nf.find_all("style"):
                css_size+=len(cs.get_text())
                total_css+=1

            for csx in nf.find_all("link"):
                hoturl = ""
                linkurl = csx.get("href")
                if not (linkurl.startswith("https") or linkurl.startswith("http")):
                    hoturl=self.site_url.strip("/")+"/"+linkurl
                else:
                    hoturl = linkurl

                linkgth = threading.Thread(target=GetRequest,args=(hoturl,"link"))
                linkgth.setDaemon=True
                link_thr.append(linkgth)

            for jss in js_thr:
                jss.start()
            for jss in js_thr:
                jss.join()


            for img in img_thr:
                img.start()
            for img in img_thr:
                img.join()


            for link in link_thr:
                link.start()
            for link in link_thr:
                link.join()


            for fon_t in font_thr:
                fon_t.start()
            for font_t in font_thr:
                font_t.join()



            for x in js_ar:
                if x == 1:
                    total_javascript+=x
                else:
                    javascript_size+=x

            for x in img_ar:
                if x == 1:
                    total_images+=x
                else:
                    image_size+=x


            for x in link_ar:
                if x == 1:
                    total_css+=x
                else:
                    css_size+=x

            for f_c in font_thr:
                font_size+=f_c


            for tag in nf.find_all("script"): nf.script.decompose()
            for tag in nf.find_all("style"): nf.style.decompose()
            total_html+=1
            html_size=len(str(nf))
                                        
            #calculate size of static files                                    

            image_size=convert_bytes(image_size)
            javascript_size=convert_bytes(javascript_size)
            css_size=convert_bytes(css_size)
            font_size=convert_bytes(font_size)
            html_size=convert_bytes(html_size)

            # Calculate percentage 

            total_static = total_images+total_javascript+total_html+total_css
            javascript_percentage = str(total_javascript/total_static*100)+"%"
            html_percentage = str(total_html/total_static*100)+"%"
            css_percentage = str(total_css/total_static*100)+"%"
            font_percentage = str(total_font/total_static*100)+"%"
            image_percentage = str(total_images/total_static*100)+"%"

            self.static=[{"name":"javascript","percentage":javascript_percentage,"size":javascript_size},{"name":"image","percentage":image_percentage,"size":image_size},{"name":"css","percentage":css_percentage,"size":css_size},{"name":"html","percentage":html_percentage,"size":html_size},{"name":"font-size","percentage":font_percentage,"size":font_size}],
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.static
