from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class ChromeHandler:
    def __init__(self, *args, **kwargs):
        pass
    
    def get_driver(self, options:list):
        chrome_options = webdriver.ChromeOptions()
        for i in options:
            chrome_options.add_argument(i)
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
    def kill_driver(self):
        pass
    
    def scrap_url(self, url): 
        pass
    
    

def get_driver(options:list):
    options = webdriver.ChromeOptions()
    for i in options:
        options.add_argument(i)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def get_firefox_driver(options:list):
    options = webdriver.FirefoxOptions()
    for i in options:
        options.add_argument(i)
    return webdriver.Firefox(options=options)

"""


options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
driver = get_firefox_driver(options=options)




options = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
driver = get_driver(options=options)


"""
