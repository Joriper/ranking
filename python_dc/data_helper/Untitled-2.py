
import datetime,sys,re
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
import requests
import textstat
from bs4 import BeautifulSoup
import pandas as pd
from serpapi import GoogleSearch
import json
from statistics import median
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SerpCollectionHandler:
    def __init__(self,**kwargs):
        pass

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
            try:
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
            except:
                pass

        reading_levels_mean = median(reading_levels)
        reading_times_mean = median(reading_times)
        word_counts_median = median(word_counts)

        return reading_levels, reading_times, word_counts, reading_levels_mean, reading_times_mean, word_counts_median, mydomain_reading_level, mydomain_reading_time, mydomain_word_count
    

    def InitializeSerp(self):
        keyword="websiteranking.ai"
        num_results = 10
        mydomain="websiteranking.ai"
        mydomain_url = "https://websiteranking.ai"
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

        set_actual = []
        for url,time,word,ease in zip(links,reading_times,word_counts,reading_levels):
            set_actual.append({"url":url,"reading_time":time,"word_count":word,"reading_ease":ease})

        print(set_actual)
        
x= SerpCollectionHandler()
x.InitializeSerp()