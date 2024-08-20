from db.connection import *
from helpers.parser.parser import Parser
import re,sys,pytesseract
from helpers.requester.requester import HttpPostRequestHandler,HttpRequestHandler
from helpers.urls.urls import GetURL
from transformers import pipeline
import textstat,hashlib,os,datetime
from error.error import Error
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from db.connection import *
from selenium.webdriver.common.by import By
from db.connection import *
from language_detector import detect_language
from spellchecker import SpellChecker
from langdetect import detect
from concurrent.futures import ThreadPoolExecutor
from textblob import Word
import numpy as np
import uuid,base64
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
from sentence_transformers import SentenceTransformer, util
from PIL import Image
from io import BytesIO
from logger.json_logger import LogEvent
from utils.selenium_utils import get_driver, get_firefox_driver


class ContentandInformation:
    def __init__(self,**kwargs):
        self.lighthouse=kwargs['lighthouse']
        self.site_url=kwargs['site_url']
        self.site_host=kwargs['site_host']
        self.info_score = False
        self.insight_id = kwargs['random_id']
        self.flag_ship_handler=False
        self.about_page = False
        self.contact_page = False
        self.change_detected =False
        self.multi_lang = False
        self.copy_right_terms = False
        self.site_base = False
        self.regular_update = False
        self.content_effective = False
        self.uid = str(uuid.uuid4())
        self.is_grammer_error =False
        self.tree_map = False
        self.performance_grade = 0
        self.is_descriptive=False
        self.filter_search={}
        self.sv_m = kwargs['sv_m']['dump_helper']
        self.link_collection = kwargs['sv_m']['dump_links']
        self.queue_item = kwargs['queue_item']

    async def is_web_regular_updated(self,run_type):
        try:
            async def GraphNormal(data):
                main_date = str(datetime.datetime.now()).split(" ")[0]
                day = main_date.split("-")[-1]
                year = main_date.split("-")[0]
                month = str(datetime.datetime.now().strftime("%b"))            
                result = re.findall("Last updated.*|Last reviewed.*",str(Parser(data).text),re.IGNORECASE)
                if len(result) > 0:
                    if month in result[-1] and day in result[-1] and year in result[-1]:
                        self.change_detected = {
                            "status":True,
                            "reason":str([result[-1]]),
                        }
                else:
                    all_sites = list(process_collection.find({"site_url":self.site_url}))
                    if len(all_sites) > 0:
                        all_hash = [hash_text['web_hash'] for hash_text in all_sites if hash_text.get("web_hash")]
                        new_hash = await self.Web_base()
                        if str(new_hash) not in  all_hash:
                            self.change_detected = {
                                "status":True,
                                "reason":"The website have some change detection by today.",
                            }
                    else:
                        self.change_detected = {
                            "status":True,
                            "reason":"The website have some change detection by today.",
                        }

            if run_type == "GRAPH":
                pass
            else:
                await GraphNormal(self.sv_m['dump'])
            

        except Exception as error:
            LogEvent(self.queue_item, "is_web_regular_updated", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        if self.change_detected == False:
            self.change_detected = {
                "status":False,
                "reason":"The website did'nt allow to track the functionality of regular updates"
            }         
        return self.change_detected
                
    async def clear_and_understandable_info(self,run_type):
        def GraphNormal(data_):
            try:
                data = Parser(data_).text.replace("\n","")
                result = int(textstat.flesch_reading_ease(data))
                score=None
                if result <=100 and result>=90:
                    score="Very Easy"

                elif result <=89 and result >=80:
                    score="Easy"
                
                elif result <=79 and result >=70:
                    score="Standard"
                
                elif result <=69 and result >= 40:
                    score="Difficult"
                else:
                    score="Very Difficult"

                info_clear = {
                    "readablity":score,
                    "score":result,
                    "status_reason_data":data           
                }
                self.info_score =  info_clear
            except Exception as error:
                LogEvent(self.queue_item, "clear_and_understandable_info", LogEvent.ERROR)
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'])

        if len(self.info_score) == 0:
            self.info_score = {
                "readability":0,
                "score":0,
                "status_reason_data":0
            }   
        return self.info_score


    async def multilingual_support(self,run_type):
        try:
            def GraphNormal(data):
                vh = Parser(str(data)).find_all("a",string=re.compile("english|hindi|हिंदी|हिन्दी|español|français|deutsch|中文|русский",re.IGNORECASE))
                if len(vh) > 0:
                    self.multi_lang={
                        "status":True,
                        "data":str(vh),
                        "reason":"The website offers multi-lingual support,accommodating users with various language preferences."
                    }
                else:
                    self.multi_lang={
                        "status":False,
                        "reason":"The website doesn't offer multi-lingual support, hindering its availability to accommodate users from various languages backgrounds.",
                        "data":""
                    }

            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])
               
            
        except Exception as error:
            LogEvent(self.queue_item, "multilingual_support", LogEvent.ERROR)
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)


        if len(self.multi_lang) == 0:
            self.multi_lang = {
                "status":False,
                "reason":"The website did'nt allow to track the functionality of multilanguage"
            }

 
        return self.multi_lang


    async def grammer_mistake(self,run_type):

        def GraphNormal(data_):
            selected_p_text = Parser(data_).find_all("p")
            selected_span_text = Parser(data_).find_all("span")

            sentences = []
            for paragraph_text in selected_p_text:
                if paragraph_text.text != "" and len(paragraph_text.text.strip().split(" ")) > 3:
                    sentences.append(paragraph_text.text.strip())
            
            for paragraph_texts in selected_span_text:
                if paragraph_texts.text != "" and len(paragraph_texts.text.strip().split(" ")) > 3:
                    sentences.append(paragraph_texts.text.strip())

            start = 0
            end = 2

            start_tag = 0
            end_tag = 50
            list_of_error,correct_data = [],[]
            error_data= {}
            if len(str(sentences)) > 20000:
                
                for execute in range(start,end):      
                    with open("eng_grab.text","w+") as fp:
                        for i in sentences[start_tag:end_tag]:
                            fp.write(f"{i}\n")

                
                    result=os.popen("""pylanguagetool < {}""".format("eng_grab.text")).read()
                    is_grammer_errors=str(result)
                    errors = is_grammer_errors.split("\n")
                    for data in errors:
                        if "✓ " not in  data and data != "":
                            list_of_error.append(data)
                        else:
                            correct_data.append(data)
                
                    start_tag+=50
                    end_tag+=50
                    os.remove("eng_grab.text") if os.path.exists("eng_grab.text") else False
                if len(list_of_error) > 0:
                    error_data['status'] = False
                    error_data['data']=list_of_error,
                    error_data['reason']="The content on the website  contain  spelling errors and may lack factual correctness."
                                                
                if len(error_data) > 0:
                    self.is_grammer_error = error_data
                else:
                    self.is_grammer_error = {
                        "status":True,
                        "data":correct_data,
                        "reason":"The content on the website is free from spelling errors and ensures factual correctness."
                    }
            else:
                with open("eng_grab.text","w+") as fp:
                    for i in sentences[start_tag:end_tag]:
                        fp.write(f"{i}\n")
                if os.path.exists("eng_grab.text") == True and os.path.getsize("eng_grab.text") > 0:
                    result=os.popen("""pylanguagetool < {}""".format("eng_grab.text")).read()
                    is_grammer_errors=str(result)
                    list_of_error = []
                    error_data= {}
                    errors = is_grammer_errors.split("\n")
                    for data in errors:
                        if "✓ " not in  data and data != "":
                            list_of_error.append(data)
                        else:
                            correct_data.append(data)

                    if len(list_of_error) > 0:
                        error_data['status'] = False
                        error_data['reason']="The content on the website  contain  spelling errors and may lack factual correctness."                        
                        error_data['data']=list_of_error
                                                
                    if len(error_data) > 0:
                        self.is_grammer_error = error_data
                    else:
                        self.is_grammer_error = {
                            "status":True,
                            "data":correct_data,
                            "reason":"The content on the website is free from spelling errors and ensures factual correctness."
                        }
                    os.remove("eng_grab.text") if os.path.exists("eng_grab.text") else False
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'])

        if self.is_grammer_error == False:
            self.is_grammer_error={
                "status":"Unknown",
                "reason":"!!Seems text not found for tested page"
            }
        return self.is_grammer_error

    async def descriptive_hyperlink(self,run_type):
        def GraphNormal(data_):
            try:
                if len(Parser(data_).find_all("a",string=re.compile("(Read more|more about|read-.*|about.*info|view-all|view all|view)",re.IGNORECASE))) > 0:
                    self.is_descriptive={
                        "status":True,
                        "reason":"The website may have descriptive hyperlinks",
                        "data":str(Parser(data_).find_all("a",string=re.compile("(Read more|more about|read-.*|about.*info|view-all|view all|view)",re.IGNORECASE)))
                    }
                else:
                    self.is_descriptive={
                        "status":False,
                        "data":"",
                        "reason":"the website doesn't contain a 'Read More / View-all' section"
                    }
            except Exception as error:
                LogEvent(self.queue_item, "multilingual_support", LogEvent.ERROR)
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'])
        
        if len(self.is_descriptive) == 0:
            self.is_descriptive = {
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of descriptive or readmore links"
            }

        return self.is_descriptive 



    async def sorting_and_filtering(self):
        path = os.getcwd()+"/screenshot/"
        try:
            dump = []
            form_handler = Parser(self.sv_m['dump'])
            def Pooler(link):
                if len(re.findall("(filters|sort by|sort-.*|Apply.*filter|filter)",str(Parser(link['data']).text),re.IGNORECASE)) > 0:
                    self.filter_search['search_keyword'] = False
                    self.filter_search['filter'] = True
                    self.filter_search['result']=str(re.findall("(filters|sort by|sort-.*|Apply.*filter|filter)",str(Parser(link['data']).text),re.IGNORECASE))
                    dump.append(str( re.findall("(filters|sort by|sort-.*|Apply.*filter|filter)",str(Parser(link['data']).text),re.IGNORECASE)))
            
            get_search_form = form_handler.find_all("form")
            try:
                for result in get_search_form:
                    if len(re.findall('search',str(result),re.IGNORECASE)) > 0:
                        
                        # options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
                        # driver = get_driver(options=options)

                        chrome_options = webdriver.ChromeOptions()
                        chrome_options.add_argument('--disable-gpu')
                        chrome_options.add_argument('--no-sandbox')
                        chrome_options.add_experimental_option("detach", True)       
                        chrome_options.add_argument('--disable-setuid-sandbox')
                        chrome_options.add_argument('--disable-dev-shm-usage')
                        chrome_options.add_argument('--ignore-ssl-errors=yes')
                        chrome_options.add_argument('--ignore-certificate-errors')                

                        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                        driver.maximize_window()
                        driver.get(self.site_url)
                        d_source = str(driver.page_source)
                        driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",self.site_host,str(uuid.uuid4()),"sorting_and_filtering"))

                        forms = driver.find_elements(By.ID,result.get("id"))
                        get_all_inputs = forms[-1].find_elements(By.TAG_NAME,"input")
                        
                        search_input = None
                        search_btn = None        

                        try:
                            for inputs in get_all_inputs:
                                if inputs.get_attribute("type") == "text" or inputs.get_attribute("type") == "search":
                                    search_input = inputs
                                elif inputs.get_attribute("type") == "submit":
                                    search_btn = inputs


                            search_input.send_keys("Iphone")
                            search_btn.click()

                            if len(re.findall("{}".format("Iphone"),str(Parser(driver.page_source).text),re.IGNORECASE)) >0:
                                driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",self.site_host,str(uuid.uuid4()),"sorting_and_filtering"))
                                self.filter_search['search_keyword'] = "Iphone"
                                self.filter_search['result'] = str(driver.page_source)
                                
                                dump.append(str(Parser(driver.page_source)))
                        except:
                            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                            

                        if len(self.filter_search) > 0:
                            get_void = Parser(str(d_source)).find_all("a",attrs={"href":"javascript:void(0);","title":re.compile("Search",re.IGNORECASE)})
                            if len(get_void) == 0:
                                get_void = Parser(str(d_source)).find_all("a",attrs={"href":"javascript:void(0);","id":re.compile("toggleSearch",re.IGNORECASE)})


                            if len(get_void) > 0:
                                get_void_sel = driver.find_elements(By.ID,"{}".format(get_void[-1].get("id")))
                                if len(get_void_sel) > 0:
                                    get_void_sel[-1].click()
                                else:
                                    get_void_sel = driver.find_elements(By.XPATH,"//a[@title='{}']".format(get_void[-1].get("title")))
                                    if len(get_void_sel) > 0:
                                        get_void_sel[-1].click()
                                search_input.send_keys("Helloworld")
                                search_btn.click()
                                p_source = str(driver.page_source)
                                if len(re.findall("{}".format("Helloworld"),str(Parser(p_source).text),re.IGNORECASE)) >0 or len(re.findall("(filters|sort by|sort-.*|Apply.*filter|filter)",str(Parser(p_source).text),re.IGNORECASE)) > 0:
                                    driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",self.site_host,str(uuid.uuid4()),"sorting_and_filtering"))
                                    self.filter_search['search_keyword'] = "Helloworld"
                                    self.filter_search['result'] = str(p_source)
                                    self.filter_search['filter']=True
            except:
                LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
            
            if len(self.filter_search) == 0 :
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(Pooler, self.link_collection)

        except Exception as error:
            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        dummy_img=[]
        for images in os.listdir(path):
            if "sorting_and_filtering" in str(images):
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
                    LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name
                    Error(error,self.__class__.__name__,this_function_name)

        if len(self.filter_search) == 0:
            self.filter_search = {
                "search_keyword":False,
                "result":"The website did'nt allow to track the functionality of sort or filter",
                "filter":"The website did'nt allow to track the functionality of sort or filter"
            }
        self.filter_search['response_image']=dummy_img
                        
        return self.filter_search


    async def use_of_multimedia_video_audio(self,run_type):
        def GraphNormal():
            try:

                model = ResNet50(weights='imagenet')
                get_web = Parser(HttpRequestHandler(self.site_url).text)
                unmasker = pipeline('fill-mask', model='distilbert-base-uncased')            
                get_text = str(get_web.text).split("\n")
                exact_match = [strline for strline in get_text if strline !=""]
                text_label = []
                image_labels = []
                for data in exact_match:
                    try:
                        result_for_sentence = unmasker(data+"[MASK]")
                        for i in result_for_sentence:
                            text_label.append(i['token_str'])
                    except:
                        LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                        
                p = [re.sub('[^a-zA-Z0-9]+', '', _) for _ in text_label]
                text_new_label = [text_handler for text_handler in p if text_handler != ""]
                applied_images,name_image = [],[]
                get_all_images = get_web.find_all("img")
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
                        if ".jpg" or ".jpeg" in img_url.get("src"):
                            base_image = "data:image/jpeg;base64,{}".format(img_response.content)
                        elif ".png" in img_url.get("src"):
                            base_image = "data:image/png;base64,{}".format(img_response.content)

                        applied_images.append(base64.b64encode(img_response.content))                
                    except:
                        LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                        

                def UploadPooler(baseimage):
                    json_image_response = HttpPostRequestHandler(data=baseimage.decode(),url=GetURL(type="save_img"))
                    name_image.append(json_image_response['message'])

                with ThreadPoolExecutor(max_workers=10) as execs:
                    execs.map(UploadPooler, applied_images)
                models = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
                text_embeddings = models.encode(text_label)
                image_embeddings = models.encode(image_labels)
                total_similarity = 0
            
                for img_emb in image_embeddings:
                    similarities = util.cos_sim(img_emb, text_embeddings)
                    total_similarity += np.max(similarities.numpy())
                average_similarity_score = total_similarity / len(image_embeddings) if len(image_embeddings) > 0 else 0

                if average_similarity_score >=1:
                    self.content_effective = {
                        "score":1,
                        "reason":average_similarity_score,
                        "apply_image":name_image                
                    }
                else:
                    self.content_effective = {
                        "score":0,
                        "reason":average_similarity_score,
                        "apply_image":name_image
                    }
            except Exception as error:
                LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                
                this_function_name = sys._getframe(  ).f_code.co_name
                Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal()

        return self.content_effective

    async def is_about_page(self,run_type):
        data = []
        check_word = list(free_text.find({"target":"about"}))
        def GraphNormal(data_,data_collection):
            if len(check_word) > 0:
                keywords = [show_key['keyword'] for show_key in check_word]
                def Pooler(link):
                    try:
                        if len(Parser(link['data']).find_all("a",href=re.compile("({})".format("|".join(keywords)),re.IGNORECASE))) > 0:
                            self.about_page={
                                "status":True,
                                "reason":"The website have a about page.",
                                "data":str(Parser(link['data']).find_all("a",href=re.compile("({})".format("|".join(keywords)),re.IGNORECASE)))
                            }
                            
                        elif Parser(link['data']).find_all(re.compile('^h[1-6]$'),string=re.compile("{}".format("|".join(keywords)),re.IGNORECASE)):
                            self.about_page={
                                "status":True,
                                "reason":"The website have a about page.",
                                "data":str(Parser(link['data']).find_all(re.compile('^h[1-6]$'),string=re.compile("{}".format("|".join(keywords)),re.IGNORECASE)))
                            }
                    except:
                        LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                        
                try:
                    about_pages=Parser(data_).find_all(lambda x: x.name == "a" and "href" in x.attrs and not (".pdf" in x.get("href") or ".pps" in x.get("href") or ".jpeg" in x.get("href") or ".jpg" in x.get("href") or ".svg" in x.get("href") or ".mp3" in x.get("href") or ".mp4" in x.get("href") or ".m4v" in x.get("href"))  and (x.get("href").startswith("/") or re.findall("^(https|http).*{}".format(self.site_host),str(x.get("href")))))
                    all_pages = Parser(data_).find_all("a")

                    for test in all_pages:
                        if re.findall("({})".format("|".join(keywords)),test.get("href"),flags = re.IGNORECASE):
                            self.about_page={
                                "status":True,
                                "reason":"The website have a about page.",
                                "data":str(test.get("href"))
                            }
                            break                
                        elif re.findall("({})".format("|".join(keywords)),test.text,flags = re.IGNORECASE):
                            self.about_page={
                                "status":True,
                                "reason":"The website have a about page.",
                                "data":str(test.text)
                            }
                            break

                
                    if Parser(data_).find_all(re.compile('^h[1-6]$'),string=re.compile("^({})".format("|".join(keywords)),re.IGNORECASE)):
                        self.about_page={
                            "status":True,
                            "reason":"The website have a about page.",
                            "data":str(Parser(data_).find_all(re.compile('^h[1-6]$'),string=re.compile("^({})".format("|".join(keywords)),re.IGNORECASE)))
                        }


                    if self.about_page == False:
                        with ThreadPoolExecutor(max_workers=5) as executor:
                            executor.map(Pooler, data_collection)

                    if self.about_page == False:
                        self.about_page ={
                            "status":False,
                            "data":"",
                            "reason":"The website doesnt 'About us' contain"
                        }
                except Exception as error:
                    LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'],self.link_collection)
        if self.about_page == False:
            self.about_page = {
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of about pages"
            }

        return self.about_page


    async def is_contact_page(self,run_type):
        data = []
        check_word = list(free_text.find({"target":"contact"}))
        
        def GraphNormal(data_,data_collection):
            if len(check_word) > 0:
                keywords = [show_key['keyword'] for show_key in check_word]
                def Pooler(link):
                    try:
                        if len(Parser(link['data']).find_all("a",attrs={"href":re.compile("({})".format("|".join(keywords)),re.IGNORECASE)})) > 0:
                            self.contact_page={
                                "status":True,
                                "reason":"The website have a contact page.",
                                "data":str(Parser(link['data']).find_all("a",attrs={"href":re.compile("({})".format("|".join(keywords)),re.IGNORECASE)}))
                            }
                        elif Parser(link['data']).find_all(re.compile('^h[1-6]$'),string=re.compile("{}".format("|".join(keywords)),re.IGNORECASE)):
                            self.contact_page={
                                "status":True,
                                "reason":"The website have a contact page.",
                                "data":str(Parser(link['data']).find_all(re.compile('^h[1-6]$'),string=re.compile("{}".format("|".join(keywords)),re.IGNORECASE)))
                            }
                    except:
                        LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                        

                try:
                    contact_page=Parser(data_).find_all(lambda x: x.name == "a" and "href" in x.attrs and not (".pdf" in x.get("href") or ".pps" in x.get("href") or ".jpeg" in x.get("href") or ".jpg" in x.get("href") or ".svg" in x.get("href") or ".mp3" in x.get("href") or ".mp4" in x.get("href") or ".m4v" in x.get("href"))  and (x.get("href").startswith("/") or re.findall("^(https|http).*{}".format(self.site_host),str(x.get("href")))))
                    for test in contact_page:
                        if re.findall("({})".format("|".join(keywords)),test.get("href"),flags = re.IGNORECASE):
                            self.contact_page={
                                "status":True,
                                "reason":"The website have a contact page.",
                                "data":str(test.get("href"))
                            }
                            break
                        elif re.findall("({})".format("|".join(keywords)),test.text,flags = re.IGNORECASE):
                            self.contact_page={
                                "status":True,
                                "reason":"The website have a contact page.",
                                "data":str(re.findall("({})".format("|".join(keywords)),test.text,flags = re.IGNORECASE))
                            }
                            break
                    if Parser(data_).find_all(re.compile('^h[1-6]$'),string=re.compile("{}".format("|".join(keywords)),re.IGNORECASE)):
                        self.contact_page={
                            "status":True,
                            "reason":"The website have a contact page.",
                            "data":str(Parser(data_).find_all(re.compile('^h[1-6]$'),string=re.compile("{}".format("|".join(keywords)),re.IGNORECASE)))
                        }

                    if self.contact_page ==  False:                            
                        with ThreadPoolExecutor(max_workers=5) as executor:
                            executor.map(Pooler, data_collection)

                    if self.contact_page == False:
                        self.contact_page={
                            "status":False,
                            "data":"",
                            "reason":"The website doesnt 'Contact us' contain"
                        }

                except Exception as error:
                    LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'],self.link_collection)

        if self.contact_page == False:
            self.contact_page = {
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of contact page"
            }
        return self.contact_page



    async def is_tree_map(self):
        try:
            if self.lighthouse['audits']['script-treemap-data']:
                self.tree_map={
                    "status":True,
                    "reason":"The website may have detailed analyzed.",
                    "data":[self.lighthouse['audits']['script-treemap-data']]
                }
        except Exception as error:
            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.tree_map == False:
            self.tree_map={
                "status":False,
                "reason":"The website did'nt have detailed analyzed structure.",
                "data":[]
            }
         
        return self.tree_map

    async def flagship_priorities(self,run_type):
        def GraphNormal(data_):
            data=[]
            try:
                def Pooler(link):
                    if re.findall("flagship|programmes",Parser(link['data']).text):
                        self.flag_ship_handler={
                            "status":True,
                            "reason": str(Parser(link['data']).text)
                        }        

                form_handler=Parser(data_).find_all(lambda x: x.name == "a" and "href" in x.attrs and not (".pdf" in x.get("href") or ".pps" in x.get("href") or ".jpeg" in x.get("href") or ".jpg" in x.get("href") or ".svg" in x.get("href") or ".mp3" in x.get("href") or ".mp4" in x.get("href") or ".m4v" in x.get("href"))  and (x.get("href").startswith("/") or re.findall("^(https|http).*{}".format(self.site_host),str(x.get("href")))))
                
                for link in form_handler:
                    if len(re.findall("flagship|programmes|department|departments",link.get("href"))) > 0:
                        self.flag_ship_handler={
                            "status":True,
                            "reason":str(link.get("href"))
                        }
                        break
                if self.flag_ship_handler==False:
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(Pooler, form_handler)
                if self.flag_ship_handler ==False:
                    self.flag_ship_handler={
                        "status":False,
                        "reason":"The Website does'nt contain a flagship priorities section departments or programs"
                    }
            except Exception as error:
                LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
                
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'])

        if self.flag_ship_handler == False:
            self.flag_ship_handler = {
                "status":False,
                "reason":"The website did'nt allow to track the functionality of Flagship or departments or programs"
            }
        return self.flag_ship_handler
                

    async def performance_indicator(self):
        try:
            self.performance_grade=self.lighthouse['categories']['performance']['score']*100
            return self.performance_grade
        except Exception as error:
            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.performance_grade
    
    async def is_copyright_and_term_policy(self,run_type):
        try:
            def GraphNormal(data):

                resp = Parser(data)
                if len(re.findall("(copyright|all.*righ.*reserved)",str(resp.text),re.IGNORECASE)) != 0 and len(re.findall("(terms and condition| Terms.*cond|policy.*)",str(resp.text),re.IGNORECASE))!= 0:
                    self.copy_right_terms={
                        "status":True,
                        "data":str(data),
                        "reason":"The website may have copyright terms and condition policy",
                    }
                else:
                    self.copy_right_terms={
                        "status":False,
                        "data":"",
                        "reason":str(data)
                    }
                copyrightcheck = resp.find_all(attrs={"class":re.compile("copyright",re.IGNORECASE)})
                copyright_check = resp.find_all(attrs={"id":re.compile("copyright",re.IGNORECASE)})
                
                if len(copyrightcheck) > 0 or len(copyright_check) > 0:
                    self.copy_right_terms = {
                        "status":True,
                        "reason":"The website may have copyright terms and condition policy",
                        "data":str([copyrightcheck,copyright_check])
                    }
                else:
                    self.copy_right_terms = {
                        "status":False,
                        "data":"",
                        "reason":"The website does not have a copyright terms and policy"
                    }
            
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])
        except Exception as error:
            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        
        if self.copy_right_terms == False:
            self.copy_right_terms = {
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of copyright or terms and conditions."
            }
        return self.copy_right_terms
        

    
    async def is_seo_optimzed(self):
        pass

    async def analytics_visitor_behavior(self):
        pass


    async def Web_base(self):
        try:
            result= Parser(self.sv_m['dump']).text
            data = hashlib.sha224()
            data.update(str(result).encode("utf-8"))
            hash_cal = data.hexdigest()
            self.site_base=hash_cal
        except Exception as error:
            LogEvent(self.queue_item, "STEP", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)            
        return self.site_base


