
from helpers.parser.parser import Parser
import re,sys
from db.connection import *
from selenium import webdriver
from error.error import Error
from helpers.requester.requester import HttpRequestHandler
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class IntegrationandService:
    def __init__(self,**kwargs):
        self.site_url=kwargs['site_url']
        self.document_excel_pdf=False
        self.permit_apply=False
        self.site_host=kwargs['site_host']
        self.insight_id = kwargs['random_id']
        self.sv_m = kwargs['sv_m']['dump_helper']
        self.data_links = kwargs['sv_m']['link_data']
        self.form_exists = {}
        self.gov_services = False
        self.link_collection = kwargs['sv_m']['dump_links']
        self.is_grievance = False

    async def avail_government_service(self):
        try:
            chrome_options = webdriver.ChromeOptions()

            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            #chrome_options.add_argument("--headless=new")
            chrome_options.add_argument('--ignore-certificate-errors')
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.site_url)

            user_input = driver.find_elements(By.XPATH,"//input[@type='text']")
            password_input = driver.find_elements(By.XPATH,"//input[@type='password']")

            if len(user_input) > 0 and len(password_input) > 0:
                user_input[-1].send_keys("adgsolution@gmail.com")
                password_input[-1].send_keys("dummypassword")

                if len(re.findall("(Invalid username|Incorrect|Password is missing|Incorrect username)",str(driver.page_source),re.IGNORECASE)) > 0:
                    self.gov_services = {
                        "score":1,
                        "reason":str(driver.page_source)
                    }

            else:
                for words in ["Signin","Sign in","Login","Log in","LOG IN","Sign In","dashboard"]:
                    login_elements = driver.find_elements(By.XPATH,"//*[contains(text(), '{}')]".format(words))
                    if len(login_elements) > 0:
                        login_sel = login_elements[-1]
                        login_sel.click()
                        check_for_password = Parser(driver.page_source).find_all("input",attrs={"type":"password"})
                        if len(check_for_password) >0:
                            submit_login = driver.find_elements(By.XPATH,"//input[@type='submit']")
                            email_input = driver.find_elements(By.XPATH,"//input[@type='text']")
                            password_input = driver.find_elements(By.XPATH,"//input[@type='password']")
                            if len(submit_login) > 0 and len(email_input) > 0 and len(password_input) > 0:
                                for send_inputs in email_input:
                                    send_inputs.send_keys("test@gmail.com")
                                password_input[-1].send_keys("ABCDKLfweJLK@$##$")
                                submit_login[-1].click()
                                page_source = driver.page_source
                                if len(re.findall("(Invalid username|Incorrect|Password is missing|Incorrect username|Sorry, unrecognized username)",str(page_source),re.IGNORECASE)) > 0:
                                    self.gov_services = {
                                        "score":1,
                                        "reason":str(page_source)
                                    }
                                    break
            if self.gov_services ==  False:
                call_ = None
                
                link_handler=Parser(self.sv_m['dump']).find_all(lambda x: x.name == "a" and "href" in x.attrs and not (".pdf" in x.get("href") or ".pps" in x.get("href") or ".jpeg" in x.get("href") or ".jpg" in x.get("href") or ".svg" in x.get("href") or ".mp3" in x.get("href") or ".mp4" in x.get("href") or ".m4v" in x.get("href"))  and (x.get("href").startswith("/") or re.findall("^(https|http).*{}".format(self.site_url.split("://")[1].split("/")[0]),str(x.get("href")))) and len(re.findall("facebook|twitter|linkedin|instagram|whatsapp",x.get("href"),re.IGNORECASE)) == 0)

                for call_link in link_handler:
                    if len(re.findall("Signin|Sign in|Login|Log in|LOG IN|Sign In|signup|dashboard|dashboard_login|joinus",str(call_link),re.IGNORECASE)) > 0:
                        call_ = call_link
                
                if call_ != None:
                    driver.get(call_)

                    check_for_password = Parser(driver.page_source).find_all("input",attrs={"type":"password"})
                    if len(check_for_password) >0:
                        submit_login = driver.find_elements(By.XPATH,"//input[@type='submit']")
                        email_input = driver.find_elements(By.XPATH,"//input[@type='text']")
                        password_input = driver.find_elements(By.XPATH,"//input[@type='password']")
                        if len(submit_login) > 0 and len(email_input) > 0 and len(password_input) > 0:
                            for send_inputs in email_input:
                                send_inputs.send_keys("test@gmail.com")
                            password_input[-1].send_keys("ABCDKLfweJLK@$##$")
                            submit_login[-1].click()
                            page_source = driver.page_source
                            if len(re.findall("(Invalid username|Incorrect|Password is missing|Incorrect username|Sorry, unrecognized username)",str(page_source),re.IGNORECASE)) > 0:
                                self.gov_services = {
                                    "score":1,
                                    "reason":str(page_source)
                                }

                if call_ == None:
                    caller = []
                    for x_link in link_handler:
                        if not(x_link.get("href").startswith("https") and x_link.get("href").startswith("http")):
                            if x_link.get("href").startswith("en") or x_link.get("href").startswith("hi") or x_link.get("href").startswith("/en") or x_link.get("href").startswith("/hi"):
                                caller.append(self.site_url+x_link.get("href").split("en")[-1])
                            else:
                                caller.append(x_link.get("href"))


                    tmp_link = []
                    def Pooler(link):
                        if len(Parser(HttpRequestHandler(link).text).find_all("input",attrs={"type":"password"})) > 0:
                            tmp_link.append(link)
                            
                    if call_ == None:
                        with ThreadPoolExecutor(max_workers=5) as executor:
                            executor.map(Pooler, caller)

                    if len(tmp_link) > 0:
                        driver.get(tmp_link[-1].get("href"))

                        check_for_password = Parser(driver.page_source).find_all("input",attrs={"type":"password"})
                        if len(check_for_password) >0:
                            submit_login = driver.find_elements(By.XPATH,"//input[@type='submit']")
                            email_input = driver.find_elements(By.XPATH,"//input[@type='text']")
                            password_input = driver.find_elements(By.XPATH,"//input[@type='password']")

                            if len(submit_login) > 0:
                                submit_login = driver.find_elements(By.XPATH,"//button[@type='submit']")
                            if len(submit_login) > 0 and len(email_input) > 0 and len(password_input) > 0:
                                for send_inputs in email_input:
                                    send_inputs.send_keys("test@gmail.com")
                                password_input[-1].send_keys("ABCDKLfweJLK@$##$")
                                submit_login[-1].click()
                                page_source = driver.page_source
                                if len(re.findall("(Invalid Captcha|Captcha needed|Enter the correct captcha value|Invalid username|Incorrect|Password is missing|Incorrect username|Sorry, unrecognized username)",str(page_source),re.IGNORECASE)) > 0:
                                    self.gov_services = {
                                        "score":1,
                                        "reason":"Invalid Captcha"
                                    }


            if self.gov_services == False:
                self.gov_services = {
                    "score":0,
                    "reason":str(driver.page_source)
                    }
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.gov_services
            



    async def _end_permit_benifits(self,run_type):
        try:
            def GraphNormal(data_):
                result_permit = Parser(data_)
                link_permit = result_permit.find_all("a")
                for data in link_permit:
                    # if len(re.findall("Labour welfare|Incentive Schemes|Maternity Benefit|sarkari yojana|INITIATIVES|subsidy|pension-scheme|pension scheme|financial assistance|financial support|allotment|careers|health-care|health care|health insurance|better education|best-education|better-education",str(data),re.IGNORECASE)) > 0:
                    if len(re.findall(
                            r"labour welfare|incentive schemes?|maternity benefit(s?)|sarkari yojana|INITIATIVES|subsid(y|ies)|pension(-| )scheme(s?)|financial (assistance|support)|allotment(s?)|career(s?)|health(-| )care|health insurance|better education|best(-| )education|child(ren)?(-| )benefit(s?)|family(-| )benefit(s?)|employ(ee|er) benefit(s?)|social(-| )security|welfare(-| )scheme(s?)|government(-| )aid|unemployment(-| )benefit(s?)|disability(-| )benefit(s?)|provident(-| )fund|gratuity(-| )fund|medical(-| )benefit(s?)|insurance(-| )benefit(s?)|accident(-| )benefit(s?)|retirement(-| )benefit(s?)",
                            str(data), re.IGNORECASE)) > 0:
                        self.permit_apply={
                            "status":True,
                            "reason":"The website include end to end benifits such as labour welfare incentives scheme maternity etc.",
                            "data":str(data)
                        }
                        break
                if self.permit_apply==False:
                    if len(re.findall(
                            r"labour welfare|incentive schemes?|maternity benefit(s?)|sarkari yojana|INITIATIVES|subsid(y|ies)|pension(-| )scheme(s?)|financial (assistance|support)|allotment(s?)|career(s?)|health(-| )care|health insurance|better education|best(-| )education|child(ren)?(-| )benefit(s?)|family(-| )benefit(s?)|employ(ee|er) benefit(s?)|social(-| )security|welfare(-| )scheme(s?)|government(-| )aid|unemployment(-| )benefit(s?)|disability(-| )benefit(s?)|provident(-| )fund|gratuity(-| )fund|medical(-| )benefit(s?)|insurance(-| )benefit(s?)|accident(-| )benefit(s?)|retirement(-| )benefit(s?)", str(data), re.IGNORECASE)) > 0:
                        # if len(re.findall("Labour welfare|Incentive Schemes|sarkari yojana|Maternity Benefit|INITIATIVES|subsidy|pension-scheme|pension scheme|financial assistance|financial support|allotment|careers|health-care|health care|health insurance|better education|best-education|better-education",str(result_permit.text),re.IGNORECASE)) > 0:

                        self.permit_apply={
                            "status":True,                            
                            "reason":"The website include end to end benifits such as labour welfare incentives scheme maternity etc.",
                            "data":str(link_permit)
                        }
                        
                if self.permit_apply == False:
                    self.permit_apply={
                        "status":False,
                        "reason":"The website doesn't include end to end benifits such as labour welfare incentives scheme maternity etc."
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if len(self.permit_apply) ==0:
            self.permit_apply = {
                "status":False,
                "reason":"The website didn't allow to track the functionality of benifits or any schema benifits,maternity."
            }
        return self.permit_apply
        
    async def can_download(self,run_type):
        
        def Download(link):
            if len(Parser(link['data']).find_all("a",href=re.compile(".pdf|.xlsx|.csv"))) > 0:
                self.document_excel_pdf={
                    "status":True,
                    "data":str(Parser(link['data']).find_all("a",href=re.compile(".pdf|.xlsx|.csv"))),
                    "reason":"Users have the option to download to documents in diffrent formats like PDF,XLS,and more through website functionality."

                }
        try:
            def GraphNormal(data_,data_collection):

                data = Parser(data_)
                if len(data.find_all("a",href=re.compile(".pdf|.xlsx|.csv"))) > 0:
                    self.document_excel_pdf={
                        "status":True,
                        "data":str(data.find_all("a",href=re.compile(".pdf|.xlsx|.csv"))),
                        "reason":"Users have the option to download to documents in diffrent formats like PDF,XLS,and more through website functionality."
                    }
                elif len(re.findall("Download pdf| pdf format| download csv",str(data))):
                    self.document_excel_pdf={
                        "status":True,
                        "data":str(data)[0:10000],
                        "reason":"Users have the option to download to documents in diffrent formats like PDF,XLS,and more through website functionality."
                    }
                else:
                    pdfxls = data.find_all("a",href=lambda x: not (".pdf" in x or ".pps" in x  or ".jpeg" in x or ".jpg" in x or ".svg" in x or ".mp3" in x or ".mp4" in x or ".m4v" in x)  and (x.startswith("/") or re.findall("^(https|http).*{}".format(self.site_host),str(x))))
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(Download, data_collection)
                if self.document_excel_pdf == False:
                    self.document_excel_pdf={
                        "status":False,
                        "reason":"The website doesn't provide the option to download documents in diffenret formats like PDF,XLS etc.",
                        "data":""
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'],self.link_collection)
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        
        if self.document_excel_pdf == False:
            self.document_excel_pdf = {
                "status":False,
                "reason":"The website doesn't allow to track the functionality of whether PDF or Excel file available or not."
            }
        return self.document_excel_pdf

    async def grienvance_system(self,run_type):
        try:
            def GraphNormal(data):
                if re.findall("(raise complaint|help and support|technical support|for any query|file a complaint|Help Center|help.*support|help|contact us|feedback)",str(Parser(data).find_all("a")),re.IGNORECASE):  #update contact us, feedback
                    self.is_grievance={
                        "status":True,
                        "data":str(Parser(data).find_all("a")),
                        "reason":"The website provides tracking option for service requests and support queries."
                    }
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'])

        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)
        if self.is_grievance == False:
            self.is_grievance={
                "status":False,
                "reason":"The website doesn't have help / support or complaint features.",
                "data":""
            }
        return self.is_grievance
    
    async def is_api_third_party_integration(self):
        pass

    async def comply_government_policy(self):
        pass

    async def security_patches(self):
        pass

    async def form_submission_exits(self,run_type):
        try:
            def GraphNormal(data,data_collection):
                forms = Parser(data).find_all("form")
                if len(forms) > 0:
                    form_types = {
                        "input": [],
                        "textarea": [],
                        "select": [],
                        "button": []
                    }
                    for form in forms:
                        for key in form_types:
                            form_types[key].extend(form.find_all(key))
                    self.form_exists = {
                        "status": True,
                        "reason": "Found forms with various input types",
                        "form_types": {k: len(v) for k, v in form_types.items()},
                        "forms": str(forms)[:1000]  # First 1000 chars to avoid huge output
                    }
                else:
                    def Pooler(data_links):
                        forms = Parser(data_links['data']).find_all("form")
                        if len(forms) > 0:
                            for form in forms:
                                method = form.get("method", "").lower()
                                action = form.get("action", "")
                                if method in ["post", "get"] and action:
                                    self.form_exists = {
                                        "status": True,
                                        "reason": f"Found form with method='{method}' and action='{action}'",
                                        "form": str(form)[:500]  # First 500 chars
                                    }
                                    break
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(Pooler, data_collection)
            if run_type == "GRAPH":
                pass
            else:
                GraphNormal(self.sv_m['dump'],self.link_collection)

            if len(self.form_exists) == 0:
                self.form_exists = {
                    "status":False,
                    "reason":"The website doesn't have form submission features."
                }


        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if len(self.form_exists) == 0:
            self.form_exists = {
                "status":False,
                "reason":"The website didn't allow to track the functionality of form submission or can be protected by firewalls"
            }
        return self.form_exists
