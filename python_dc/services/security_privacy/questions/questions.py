from cryptography.hazmat.backends import default_backend
from error.error import Error
from helpers.requester.requester import HttpRequestHandler
from helpers.parser.parser import Parser
from cryptography import x509
import subprocess
from concurrent.futures import ThreadPoolExecutor
import ssl,socket,sys,re,os,requests

class SecurityPrivacy:
    def __init__(self,**kwargs):
        self.ssl_info={}
        self.site_host=kwargs['site_host']
        self.site_url = kwargs['site_url']
        self.ssl_tls=False
        self.sv_m = kwargs['data']['dump_helper']
        self.links = kwargs['data']['link_data']
        self.security_headers = {}
        self.cookie_policy={}
        self.check_update = {}
        self.access_auth = {}
        self.captcha = {}
        self.vulnerability = {}
        self.secure_practice = {}
        self.ssl = False

    async def IsSSL(self):
        def verify_ssl_certificate(hostname):
            port = 443
            try:
                dumb = []
                try:
                    def Trustedornot(hostname):
                        context = ssl.create_default_context()
                        try:
                            with socket.create_connection((hostname, port)) as sock:
                                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                                    ssock.do_handshake()
                                    return "OK"
                        except Exception as e:
                            return "Failed"                
                    trusted = Trustedornot(hostname)
                    cert = ssl.get_server_certificate((hostname, port),5)
                    certDecoded = x509.load_pem_x509_certificate(str.encode(cert),default_backend())
                    get_encryption_algorithm = certDecoded.signature_algorithm_oid
                    issuer = certDecoded.issuer
                    subject = certDecoded.subject
                    serial = certDecoded.serial_number
                    expire_date = certDecoded.not_valid_after
                    valid_from = certDecoded.not_valid_before


                    return [subject,issuer,serial,trusted,str(cert),expire_date,valid_from,get_encryption_algorithm,"ssl"]
                except Exception as error:
                    with requests.get(self.site_url,stream=True) as response:
                        certificate_info_raw = response.raw.connection.sock.getpeercert(True)
                        cert = ssl.DER_cert_to_PEM_cert(certificate_info_raw)
                        certificate_info = response.raw.connection.sock.getpeercert()
                        issuer = certificate_info['issuer']
                        subject = certificate_info['subject']
                        serial = certificate_info['serialNumber']
                        expire_date = certificate_info['notAfter']
                        get_encryption_algorithm = False
                        valid_from = certificate_info['notBefore']
                        this_function_name = sys._getframe(  ).f_code.co_name
                    return [subject,issuer,serial,'Unknown',str(cert),expire_date,valid_from,get_encryption_algorithm,"requests"]
            except Exception as error:
                return [False]
  
        resp = verify_ssl_certificate(self.site_host)
        if resp != [False]:
            try:
                if resp[-1] == "ssl":
                    subject = resp[0].rfc4514_string().split("=")[1]
                else:
                    subject = resp[0][-1][-1][-1]
            except:
                subject = ""
            try:
                if resp[-1] == "ssl":
                    issuer_country = list(resp[1])[0].rfc4514_string().split("=")[1]
                else:
                    issuer_country = resp[1][0][0][-1]
            except:
                issuer_country = ""

            try:
                if resp[-1] == "ssl":
                    issuer_organization = list(resp[1])[1].rfc4514_string().split("=")[1]
                else:
                    issuer_organization  = resp[1][1][-1][-1]
            except:
                issuer_organization = ""

            try:
                if resp[-1] == "ssl":
                    common_name = list(resp[1])[2].rfc4514_string().split("=")[1]
                else:
                    common_name = resp[1][-1][-1][-1]
            except:
                common_name = ""

            try:
                tmp = str(resp[-2]).split(" ")[-1]                
                get_type = int(''.join(filter(str.isdigit, str(tmp))))
                if get_type >=256 and len(re.findall("rsa",str(tmp),re.IGNORECASE)) > 0:
                    strong_encryption = {
                        "status":True,
                        "reason":{"name":str(tmp).split("=")[-1].replace(")>","")},
                        "data":{
                            "SHA":True,
                            "RSA":True,
                            "256>=":True
                        }                        
                    }
                else:
                    strong_encryption = {
                        "status":False,
                        "reason":{"name":str(tmp).split("=")[-1].replace(")>","")},
                        "data":{
                            "SHA":False,
                            "RSA":False,
                            "256>=":False
                        }
                    }
            except Exception as error:
                print("ERRORS",error)
                strong_encryption = {
                    "status":False,
                    "reason":{"name":str(resp[-2])},
                    "data":{
                        "SHA":False,
                        "RSA":False,
                        "256>=":False
                    }                    
                }

            print(resp)
            try:
                serial = str(resp[2])
            except:
                serial = ""
            self.ssl_info["Subject"]=subject
            self.ssl_info["Issuer"]=str(resp[1])
            self.ssl_info["expire_date"]=resp[5]
            self.ssl_info["issue_date"]=resp[6]
            self.ssl_info["Verify"]="Verified"
            self.ssl_info["organization"]=issuer_organization
            self.ssl_info["Serial"]=serial
            self.ssl_info['Certificate']=resp[4]
            self.ssl_info["common_name"]=common_name
            self.ssl_info["issuer_country"]=issuer_country
            self.ssl_info["Trusted"]=resp[3]
            self.ssl_info['strong_encryption']=strong_encryption
            self.ssl_tls=True
        else:
            self.ssl_info["Subject"]="The Website did'nt allow to get Subject"
            self.ssl_info["Issuer"]="The Website did'nt allow to get Issuer name"
            self.ssl_info["expire_date"]="The Website did'nt allow to get Expire Date"
            self.ssl_info["issue_date"]="The Website did'nt allow to get Issue Date"
            self.ssl_info["Verify"]="The Website did'nt allow to check SSL is Verfied"
            self.ssl_info["organization"]="The Website did'nt allow to get organization"
            self.ssl_info["Serial"]="The Website did'nt allow to get Serial Number of Certificate",
            self.ssl_info['Certificate']="The Website did'nt allow to get CA Certificate"
            self.ssl_info["common_name"]="The Website did'nt allow to get Common name"
            self.ssl_info["issuer_country"]="The Website did'nt allow to get Issuer Country"
            self.ssl_info["Trusted"]="The Website did'nt allow to check SSL is Trusted"
            self.ssl_info['strong_encryption']={
                "status":False,
                "reason":"The website does'nt have any strong encryption",
                "data":{
                    "SHA":False,
                    "RSA":False,
                    "256>=":False
                }
            }
            self.ssl_tls="The Website does'nt have SSL or TLS Security Layers",


        self.ssl = {
            "ssl_info":self.ssl_info,
            "ssl_tls":self.ssl_tls
        }
    
        return self.ssl


    async def secure_authentication(self):
        return False

    async def privacy_policy(self):
        return False

    async def data_protection(self):
        return False

    async def security_audit_certification(self):
        return False

    async def retemtion_policy(self):
        return False

    async def monitoring_system(self):
        return False

    async def vulnerability_issue(self):
        return False


    ################################################### ADDITIONAL QUESTIONS ######################################################
    async def Security_Headers(self):
        try:
            header = {
                "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
                "Accept":"*/*",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en-US,en;q=0.5",
                "Alt-Used":self.site_host,
                "Connection":"keep-alive",
            }
            check_headers = requests.get(self.site_url,headers=header).headers
            if len(re.findall("X-XSS-Protection|content-security-policy",str(check_headers),re.IGNORECASE)) > 0:
                self.security_headers={
                    "status":True,
                    "data":{
                        "X-XSS-Protection":check_headers['x-xss-protection'] if check_headers.get("x-xss-protection") else False,
                        "Content-Security-Policy":check_headers['Content-Security-Policy'] if check_headers.get("Content-Security-Policy") else False,
                    },
                    "reason":"The website have security headers."
                }
            else:
                self.security_headers={
                    "status":False,
                    "data":{
                        "X-XSS-Protection":check_headers['x-xss-protection'] if check_headers.get("x-xss-protection") else False,
                        "Content-Security-Policy":check_headers['Content-Security-Policy'] if check_headers.get("Content-Security-Policy") else False,
                    },
                    "reason":"The website have security headers"
                }
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)

        if len(self.security_headers) == 0:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            self.security_headers = {
                "status":False,
                "reason":"The website have security headers.",
                "data":{
                    "X-XSS-Protection":False,
                    "Content-Security-Policy":False
                }
            }
        return self.security_headers
    

    async def Cookie_Policy(self,run_type):
        try:
            def GraphNormal(data):
                if isinstance(data,dict):
                    result = data['data']
                else:
                    result = data
                base_model = re.findall("Accept Cookie|Our Cookie policy|Accept all cookies|Cookie policy|Cookie-policy",Parser(result).text,re.IGNORECASE)

                if len(base_model) > 0:
                    self.cookie_policy = {
                        "status":True,
                        "reason": str(result)
                    }
                else:
                    self.cookie_policy = {
                        "status":False,
                        "reason": "The website does'nt have any Cookie Policy"
                    }
            
            if run_type == "GRAPH":
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(GraphNormal, self.cookie_policy)
            else:
                GraphNormal(self.sv_m['dump'])
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name
            Error(error,self.__class__.__name__,this_function_name)
        return self.cookie_policy
    
    async def CaptchDetect(self):
        check_captcha = Parser(str(self.sv_m))
        print(re.findall("recaptcha",str(check_captcha),re.IGNORECASE))
        if len(re.findall("recaptcha",str(check_captcha),re.IGNORECASE)) > 0:
            self.captcha={
                "status":True,
                "reason":str(re.findall("recaptcha",str(check_captcha),re.IGNORECASE))
            }
        else:
            self.captcha = {
                "status":False,
                "reason":"The website does'nt have any Captcha protection"
            }
        return self.captcha
    

    ################################# Additional Question ##################
    async def AccessAuthorization(self):
        try:
            check_authorization = HttpRequestHandler(self.site_url).headers
            if check_authorization.get("Access-Control-Allow-Origin")==True and self.site_url in check_authorization.get("Access-Control-Allow-Origin") and check_authorization.get("access-control-allow-credentials") == True:
                self.access_auth = {
                    "status":True,
                    "reason":check_authorization
                }
            else:
                self.access_auth = {
                    "status":False,
                    "reason":check_authorization
                }

        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        return self.access_auth
    
    async def SecureDevelopmentPractice(self):
        try:
            check_security_header = HttpRequestHandler(self.site_url).headers
            if check_security_header.get("X-Frame-OPTIONS") and check_security_header.get("X-RateLimit") and check_security_header.get("Access-Control-Allow-Credentials") and check_security_header.get("Access-Control-Allow-Methods") and check_security_header.get("CF_ID"):
                self.secure_practice = {
                    "status":True,
                    "reason":check_security_header
                }
            else:
                self.secure_practice = {
                    "status":True,
                    "reason":check_security_header
                }
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if len(self.secure_practice) == 0:
            self.secure_practice = {
                "status":False,
                "reason":{}
            }
        return self.secure_practice
    

    async def Vulnerability(self):
        try:
            crawl_vul,blind_vul,url_vul = [],[],[]
            for_crawl = os.popen("%s %s -u %s --crawl"  % (os.path.dirname(os.getcwd())+"/env/bin/python3",os.getcwd()+"/XSStrike/xsstrike.py",self.site_url)).read()
            for_blind_xss = os.popen("%s %s -u %s --crawl --blind"  % (os.path.dirname(os.getcwd())+"/env/bin/python3",os.getcwd()+"/XSStrike/xsstrike.py",self.site_url)).read()
            for_url = os.popen("%s %s -u %s"  % (os.path.dirname(os.getcwd())+"/env/bin/python3",os.getcwd()+"/XSStrike/xsstrike.py",self.site_url)).read()

            data = re.findall("Potentially vulnerable objects found.*",str(for_crawl))
            data1 = re.findall("Potentially vulnerable objects found.*",str(for_blind_xss))
            data2 = re.findall("Potentially vulnerable objects found [+]",str(for_url))

            spliter_crawl = for_crawl.split(data[0]) if len(data) > 0 else []
            spliter_blinder = for_blind_xss.split(data[0]) if len(data1) > 0 else []
            spliter_url = for_url.split(data[0]) if len(data2) > 0 else []
 
            if len(spliter_crawl) > 0:
                vul_list_crawl = spliter_crawl[1].split("\n")
                for test in vul_list_crawl[2:4]:
                    crawl_vul.append(test.replace(" ",""))
            
            if len(spliter_blinder) > 0:
                vul_list_blind = spliter_blinder[1].split("\n")
                for test in vul_list_blind[2:4]:
                    blind_vul.append(test.replace(" ",""))
            
            if len(spliter_url) > 0:
                vul_list_vul = spliter_url[1].split("\n")
                for test in vul_list_vul[2:4]:
                    url_vul.append(test.replace(" ",""))

            self.vulnerability = {
                "status":True,
                "reason":[
                    {
                        "crawler":"The Crawler detection of vulnerability",
                        "data":crawl_vul
                    },
                    {
                        "blind_xss":"Blind XSS Vulnerability which reflect on frontend",
                        "data":blind_vul
                    },
                    {
                        "url_based":"Vulnerablity testing for url",
                        "data":url_vul
                    }
                ]
            }
        except Exception as error:
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)
        if len(self.vulnerability) == 0:
            self.vulnerability = {
                "status":True,
                "reason":[
                    {
                        "crawler":"The Website did'nt perform crawl scan",
                        "data":[]
                    },
                    {
                        "blind_xss":"The Website did'nt perform blind scan",
                        "data":[]
                    },
                    {
                        "url_based":"The Website did'nt perform url scan",
                        "data":[]
                    }
                ]
            }
        return self.vulnerability
