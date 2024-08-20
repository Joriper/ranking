from helpers.requester.requester import HttpRequestHandler
from concurrent.futures import ThreadPoolExecutor
from colorthief import ColorThief
import numpy as np
import datetime,re,json
from db.connection import *
from helpers.parser.parser import Parser
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from error.error import Error
from selenium.webdriver.common.by import By
from services.seo.questions import Seo
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from logger.json_logger import LogEvent



class Group_SEO:
    def __init__(self,**kwargs):
        self.site = kwargs['site']
        self.is_ssl = False
        self.data = kwargs['collected']
        self.sitename =self.site['name']   
        self.uid = kwargs['uid']
        self.queue_item = kwargs['queue_item']

    async def GroupCaller(self):
        siteurl = str(self.site['url'])
        try:
            if "https" in siteurl or  "http" in siteurl:
                site_host = siteurl.split("://")[1].split("/")[0]
                seo = Seo(collected=self.data,site=self.site, queue_item=self.queue_item)
                seo_questions = await seo.SeoQuestions()
                heading_optimize = await seo.HeadingOptimization()
                over_optimize = await seo.Over_optimization()

                seo_questions['heading_optimize'] = heading_optimize
                seo_questions['over_optimize'] = over_optimize
                group_seo.insert_one(seo_questions)
        except Exception as e:
            LogEvent(self.queue_item, "STEP ERROR", LogEvent.ERROR)
            
            







