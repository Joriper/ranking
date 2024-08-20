from error.error import Error
from helpers.requester.requester import HttpPostRequestHandler
from helpers.urls.urls import GetURL
from helpers.parser.parser import Parser
from selenium.webdriver.common.action_chains import ActionChains
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from db.connection import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re,sys,os,uuid,base64
from logger.json_logger import LogEvent
from utils.selenium_utils import get_driver, get_firefox_driver


load_dotenv()
class InteractivityandEngagement:
    def __init__(self,**kwargs):
        self.site_url=kwargs['site_url']
        self.social_media=False
        self.online_consult = False
        self.online_transaction=False
        self.site_host=kwargs['site_host']
        self.insight_id = kwargs['random_id']
        self.oppt = False
        self.interactive_buttons = False
        self.sv_m = kwargs['sv_m']['dump_helper']
        self.link_collection = kwargs['sv_m']['dump_links']
        self.user_generated_content = {}
        self.opportunitis=0
        self.bot_dectection = False
        self.easy_signup=False
        self.form_stats=False
        self.queue_item = kwargs['queue_item']
        

    async def is_pool_cosultation_survey(self,run_type):
        try:
            def GraphNormal(data,data_collection):
                if re.findall("feedback|consult|survey|submit feedback",str(Parser(data).find("form")),re.IGNORECASE):
                    self.online_consult={
                        "status":True,
                        "reason":"The website have pool consulation survey form and feedback",
                        "data": str(re.findall("feedback|consult|survey|submit feedback",str(Parser(data).find("form"))))
                    }
                else:
                    res=Parser(self.sv_m['dump']).find_all(lambda x: x.name == "a" and "href" in x.attrs and not (".pdf" in x.get("href") or ".pps" in x.get("href") or ".jpeg" in x.get("href") or ".jpg" in x.get("href") or ".svg" in x.get("href") or ".mp3" in x.get("href") or ".mp4" in x.get("href") or ".m4v" in x.get("href"))  and (x.get("href").startswith("/") or re.findall("^(https|http).*{}".format(self.site_host),str(x.get("href")))))
                
                    def Pooler(link):
                        if re.findall("feedback|consult|survey|submit feedback",str(Parser(link['data']).text),re.IGNORECASE):
                            self.online_consult={
                                "status":True,
                                "reason":"The website have pool consulation survey form and feedback",
                                "data":str(re.findall("feedback|consult|survey|submit feedback",str(Parser(link['data']).text),re.IGNORECASE))
                            }

                    with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(Pooler, data_collection)

                if self.online_consult == False:
                    self.online_consult={
                        "status":False,
                        "data":"",
                        "reason":"The website does'nt  have feedback consult or submission of any feedback"
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'],self.link_collection)

        except Exception as error:
            LogEvent(self.queue_item, "is_pool_cosultation_survey ERROR", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        if self.online_consult == False:
            self.online_consult ={
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of feedback or submission of feedback"
            }
        return self.online_consult
                    

    async def opportunity(self,run_type):
        try:
            def GraphNormal(data,data_collection):
                opportunity_data =[]
                if re.findall("prize pool|hurry up|opportunity|free cost|no cost",str(Parser(data).text),re.IGNORECASE):
                    self.opportunitis+=1
                    opportunity_data.append(str(re.findall("prize pool|hurry up|opportunity|free cost|no cost",str(Parser(data).text),re.IGNORECASE)))

                try:
                    def Pooler(link):
                        url_dump = Parser(link['data']).text
                        if re.findall("(prize pool|hurry up|opportunity|free cost|no cost|Be involved|participate.*)",str(url_dump),re.IGNORECASE):
                            self.opportunitis+=1
                            opportunity_data.append(str(re.findall("(prize pool|hurry up|opportunity|free cost|no cost|Be involved|participate.*)",str(url_dump),re.IGNORECASE)))
                            
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(Pooler, data_collection)

                except Exception as error:
                    LogEvent(self.queue_item, "opportunity ERROR", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name                     
                    Error(error,self.__class__.__name__,this_function_name)

                if len(opportunity_data) >0:
                    self.oppt={
                        "status":self.opportunitis,
                        "reason":str(opportunity_data)
                    }
                else:
                    self.oppt={
                        "status":0,
                        "reason":"The website does'nt have any price pool or opportunity"
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'],self.link_collection)
            return self.opportunitis
        except Exception as error:
            LogEvent(self.queue_item, "opportunity ERROR", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                    
            Error(error,self.__class__.__name__,this_function_name)
        if self.oppt ==0:
            self.oppt={
                "status":0,
                "reason":"The website did'nt allow to track the functionality of price participation or participation in opportunity."
            }
        return self.opportunitis

    async def is_online_transaction(self,run_type):
        try:
            def GraphNormal(data,data_collection):
                if len(re.findall("(EMI Options|use coupon|M.R.P.: ₹|select quantity|cash on delivery|discount|shopping|rupay|credit card|debit card|maintaince|upgrade|purchase now|new plan|sale product now|subscription plan|buy now|premium subscription|premium plan)",str(Parser(data).text),re.IGNORECASE)) > 0:
                    self.online_transaction={
                        "status":True,
                        "reason":"The website offer online transaction",
                        "data": str(re.findall("(EMI Options|use coupon|M.R.P.: ₹|select quantity|cash on delivery|discount|shopping|rupay|credit card|debit card|upgrade|purchase now|new plan|sale product now|subscription plan|buy now|premium subscription|premium plan)",str(Parser(data).text),re.IGNORECASE))
                    }
                else:
                    def Pooler(link):
                        if len(re.findall("(EMI Options|use coupon|M.R.P.: ₹|select quantity|cash on delivery|discount|rupay|credit card|shopping|debit card|upgrade|purchase now|new plan|sale product now|subscription plan|buy now|premium subscription|premium plan)",str(Parser(link['data']).text),re.IGNORECASE)) > 0:
                            self.online_transaction={
                                "status":True,
                                "reason":"The website offer online transaction",
                                "data":str(re.findall("(EMI Options|use coupon|M.R.P.: ₹|select quantity|cash on delivery|discount|rupay|credit card|shopping|debit card|upgrade|purchase now|new plan|sale product now|subscription plan|buy now|premium subscription|premium plan)",str(Parser(link['data']).text),re.IGNORECASE))
                            }
                                                
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(Pooler, data_collection)
                if self.online_transaction == False:
                    self.online_transaction={
                        "status":False,
                        "data":"",
                        "reason":"The website does'nt facilitate any online transaction ,coupon,credit card options"
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'],self.link_collection)
        except Exception as error:
            LogEvent(self.queue_item, "is_online_transaction ERROR", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        if self.online_transaction ==  False:
            self.online_transaction = {
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of online transaction."
            }
        return self.online_transaction
 
    async def social_media_integration(self,run_type):
        try:
            def GraphNormal(data):
                social_Sc = Parser(data).find_all("a",attrs={"href":re.compile("facebook|instagram|twitter|pintrest|linkedin|tiktok|youtube|reddit|whatsapp|wechat")})
                if len(social_Sc) > 0:
                    self.social_media={
                        "status":True,
                        "data":str(social_Sc),
                        "reason":"The website have social media integration.",
                    }
                else:
                    self.social_media={
                        "status":False,
                        "data":"",
                        "reason":"The website does'nt have any social media links like facebook whatsapp twitter etc."
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])
        except Exception as error:
            LogEvent(self.queue_item, "social_media_integration ERROR", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)                
        
        if self.social_media ==  False:
            self.social_media={
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of social media collection."
            }
        return self.social_media


    async def is_realtime_chatbot(self):
        try:
            assitant_text = Parser(self.sv_m['dump']).find_all("input")
            assistant_text_ = Parser(self.sv_m['dump']).find_all("textarea")
            options = ['--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
            driver = get_driver(options=options)
            driver.get(self.site_url)  

            tm_id=None
            ins=None
            res=None
            data=[]
            bot_msg = []
            
            if len(re.findall("chat",str(assitant_text),re.IGNORECASE)) > 0:
                data=assitant_text
            elif len(re.findall("chat",str(assistant_text_),re.IGNORECASE)) > 0:
                data=assistant_text_
            
            for inputs in data:
                attrs = list(inputs.attrs.values())
                tmp_value = None

                for atr in attrs:
                    if re.findall("(Type of message|message|your message|Type here|start|typing|Type mess.*)",str(attrs),re.IGNORECASE):
                        break

                get_input_or_text = inputs.get("id")
                res = inputs.findNext(re.compile("path|button|svg"))
                if res.name == "button" or res.name == "path" or res.name == "svg":
                    tm_id = res.get("id")
                    ins = driver.find_element(By.ID,inputs.get("id"))
                    ins.send_keys("Hello")
                    driver.find_element(By.ID,tm_id).click()
                    self.bot_dectection={
                        "status":True,
                        "reason":str(driver.page_source)
                    }
                else:
                    self.bot_dectection={
                        "status":True,
                        "reason":"The website does'nt have any chatbot or real time communication mode"
                    }

        except Exception as error:
            LogEvent(self.queue_item, "is_realtime_chatbot ERROR", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.bot_dectection == False:
            self.bot_dectection={
                "status":False,
                "reason":"The website did'nt allow to track the functionality of realtime chatbot or can be blocked by firewall please try again latter."
            }
        return self.bot_dectection
        

    async def is_easy_signup_email(self):
        stay_touch = [

            "stay in touch",
            "get update"
            "for more offer"
            "newsletter"
        ]
        get_ = Parser(self.sv_m['dump'])
        path = os.getcwd()+"/screenshot/"

        try:  

            try:
                get_forms = get_.find_all("form")                

                get_all_label=get_.find("label",attrs={"for":re.compile("(news|newletter|furture|support)")})

                if_not_label = None
                input_submit=None
                get_all_inputs=None
                input_submit=None

                if get_all_label != None:

                    get_all_inputs=get_.find("input",attrs={"name":get_all_label.get("for")})
                    input_submit = get_all_inputs.findNext(re.compile("input|button"),attrs={"type":"submit"})

                else:

            
                    if_not_label = get_.find("input",attrs={"type":"email"})
                    if if_not_label == None:
                        if_not_label = get_.find("input",attrs={"name":"email"})
                        for prob in stay_touch:

                            if re.findall(prob,str(if_not_label.parent.parent.parent.parent.parent.parent.find().text),re.IGNORECASE):
                                input_submit=if_not_label.findNext(re.compile("input|button"),attrs={"type":"submit"})
                                break

                options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
                driver = get_driver(options=options)
                driver.get(self.site_url)
                email_input,button_input = None,None
                try:
                    email_input = driver.find_element(By.NAME,get_all_inputs.get("name"))
                except:
                    email_input = driver.find_element(By.ID,get_all_inputs.get("id"))
                
                try:
                    button_input = driver.find_element(By.ID,input_submit.get("id"))
                except:
                    button_input = driver.find_element(By.NAME,input_submit.get("name"))
                try:
                    email_input.send_keys("test@gmail.com")
                    driver.implicitly_wait(3)           

                    driver.execute_script("arguments[0].click();", button_input)
                    result =  str(driver.page_source)
                    if "Thanku" or "Thanks" in result:
                        driver.get_screenshot_as_file(os.getcwd()+"/screenshot/image_{}_{}_{}_{}.png".format("chrome",self.site_host,str(uuid.uuid4()),"is_easy_signup_email"))
                        self.easy_signup={
                            "status":True,
                            "reason":"The website may have promotional emails or newsletter metrics.",
                            "data":str(result)[0:10000]
                        }
                except Exception as error:
                    self.easy_signup={
                        "status":False,
                        "data":"",
                        "reason":"The website does'nt have any newletter input or promotional email forms."
                    }
                driver.close()
                driver.quit()
            except Exception as error:
                LogEvent(self.queue_item, "is_easy_signup_email ERROR", LogEvent.ERROR)
                
                this_function_name = sys._getframe(  ).f_code.co_name                     
                Error(error,self.__class__.__name__,this_function_name)
        except Exception as error:
            LogEvent(self.queue_item, "is_easy_signup_email ERROR", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        if self.easy_signup ==  False:
            self.easy_signup ={
                "status":False,
                "reason":"The website did'nt allow to track the promotional email or newsletters.",
                "data":str(get_)[0:10000]
            }

        dummy_img = []
        for images in os.listdir(path):
            if "is_easy_signup_email" in str(images):
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
                    LogEvent(self.queue_item, "is_easy_signup_email ERROR", LogEvent.ERROR)
                    
                    this_function_name = sys._getframe(  ).f_code.co_name
                    Error(error,self.__class__.__name__,this_function_name)

        self.easy_signup['response_image'] = dummy_img
        return self.easy_signup

    async def form_autofill_error_prevent(self,run_type):
        try:
            def GraphNormal(data):
                forms = Parser(data).find("form").find_all("input",attrs={"autocomplete":"on","required":True})
                if len(forms) > 0:
                    forms_lab = Parser(data).find("form").find_all("label")
                    label_s = len([lab for lab in forms_lab if lab.get("for") in "".join(str(forms))])
                    if label_s > 0:
                        self.form_stats={
                            "status":True,
                            "reason":"The website may have autofill or error handling machenism.",
                            "data":str([lab for lab in forms_lab if lab.get("for") in "".join(str(forms))])
                        }
                    else:
                        self.form_stats={
                            "status":False,
                            "data":"",
                            "reason":"Failed to Find form or any input of tested page"
                        }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])

        except Exception as error:
            LogEvent(self.queue_item, "form_autofill_error_prevent ERROR", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if self.form_stats == False:
            self.form_stats={
                "status":False,
                "reason":"The website did'nt allow to track the autofill error handling.",
                "data":""
            }
        return self.form_stats

    async def is_inputerror_detection(self):
        return False

    async def active_user_registered(self):
        return False



    async def Social_Media_Comment(self,run_type):
        def GraphNormal(data):
            social_Sc = Parser(data).find_all("a",attrs={"href":re.compile("facebook|instagram|twitter|pintrest|linkedin|tiktok|youtube|reddit|whatsapp|wechat")})
            if len(social_Sc) > 0:
                if len(re.findall("Leave a Reply|fa fa-reply",str(data),re.IGNORECASE)) > 0:

                    self.interactive_buttons={
                        "status":True,
                        "data":str(social_Sc),
                        "reason":"The webite may have comment share or likes on media profile."
                        
                    }
                else:
                    self.interactive_buttons={
                        "status":False,
                        "data":"",
                        "reason":"The website does'nt have any comment or share or like buttons or links."
                    }
        if run_type == "GRAPH":
            pass
        else:
            GraphNormal(self.sv_m['dump'])
            
        
        if self.interactive_buttons ==  False:
            self.interactive_buttons={
                "status":False,
                "data":"",
                "reason":"The website did'nt allow to track the functionality of media,comments,or likes for security reasons."
            }
        return self.interactive_buttons
    

    async def UserGeneratedContent(self,run_type):
        try:
            def GraphNormal(data):
                article_tag = Parser(data).find_all("article")
                textarea_tag = Parser(data).find_all("textarea")
                div_tag =Parser(data).find_all("div")

                for article in article_tag:
                    if len(re.findall("testimonial|comment|review",str(article.attrs),re.IGNORECASE)) > 0:
                        self.user_generated_content={
                            "status":True,
                            "reason":str(re.findall("testimonial|comment|review",str(article.attrs),re.IGNORECASE))
                        }
                if len(self.user_generated_content) == 0:
                    for textarea in textarea_tag:
                        if len(re.findall("testimonial|comment|review",str(textarea.attrs),re.IGNORECASE)) > 0:
                            self.user_generated_content={
                                "status":True,
                                "reason":str(re.findall("testimonial|comment|review",str(textarea.attrs),re.IGNORECASE))
                            }
                if len(self.user_generated_content) == 0:

                    for div in div_tag:
                        if len(re.findall("testimonial|comment|review",str(div.attrs),re.IGNORECASE)) > 0:
                            self.user_generated_content={
                                "status":True,
                                "reason":str(re.findall("testimonial|comment|review",str(div.attrs),re.IGNORECASE))
                            }
                if len(self.user_generated_content) == 0:
                    self.user_generated_content = {
                        "status":False,
                        "reason":"The website does'nt have any Comment section or testimonila or review."
                    }

            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])
        except Exception as error:
            LogEvent(self.queue_item, "UserGeneratedContent ERROR", LogEvent.ERROR)
            
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)        
        return self.user_generated_content
