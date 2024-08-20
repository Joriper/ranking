# UPDATED - WORKING
from collections import Counter, defaultdict
from urllib.parse import urlsplit
from lxml import etree  # Use lxml for XML parsing
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .http import http
from .page import Page
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Website:
    def __init__(
            self, base_url, sitemap, analyze_headings, analyze_extra_tags, follow_links
    ):
        self.base_url = base_url
        self.sitemap = sitemap
        self.analyze_headings = analyze_headings
        self.analyze_extra_tags = analyze_extra_tags
        self.follow_links = follow_links
        self.crawled_pages = []
        self.crawled_urls = set([])
        self.page_queue = []
        self.wordcount = Counter()
        self.bigrams = Counter()
        self.trigrams = Counter()
        self.content_hashes = defaultdict(set)
        self.max_urls_to_crawl = 1

    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def teardown_driver(self):
        self.driver.quit()

    def check_dns(self, url_to_check):
        try:
            o = urlsplit(url_to_check)
            socket.gethostbyname(o.hostname)
            return True
        except:
            pass
        return False

    def get_text_from_xml(self, element):
        """
        Extract text from an lxml element
        """
        return element.text

    def crawl(self):
        self.setup_driver()

        try:
            if self.sitemap:
                page = http.get(self.sitemap)
                if self.sitemap.endswith("xml"):
                    tree = etree.fromstring(page.data.decode("utf-8"))
                    sitemap_urls = tree.xpath("//loc")
                    for url in sitemap_urls:
                        self.page_queue.append(self.get_text_from_xml(url))
                elif self.sitemap.endswith("txt"):
                    sitemap_urls = page.data.decode("utf-8").split("\n")
                    for url in sitemap_urls:
                        self.page_queue.append(url)

            self.page_queue.append(self.base_url)

            while self.page_queue and len(self.crawled_urls) < self.max_urls_to_crawl:
                url = self.page_queue.pop(0)
                if url in self.crawled_urls:
                    continue

                try:
                    self.driver.get(url)
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                    page = Page(
                        url=url,
                        base_domain=self.base_url,
                        analyze_headings=self.analyze_headings,
                        analyze_extra_tags=self.analyze_extra_tags,
                        html_content=self.driver.page_source
                    )

                    if page.parsed_url.netloc != page.base_domain.netloc:
                        continue

                    page.analyze()

                    self.content_hashes[page.content_hash].add(page.url)

                    for w in page.wordcount:
                        self.wordcount[w] += page.wordcount[w]

                    for b in page.bigrams:
                        self.bigrams[b] += page.bigrams[b]

                    for t in page.trigrams:
                        self.trigrams[t] += page.trigrams[t]

                    # Add new links to the queue, but skip URLs already crawled
                    new_links = [link for link in page.links if link not in self.crawled_urls]
                    self.page_queue.extend(new_links)

                    self.crawled_pages.append(page)
                    self.crawled_urls.add(page.url)

                    if not self.follow_links:
                        break

                except Exception as e:
                    print(f"Error processing {url}: {e}")
                    continue

        finally:
            self.teardown_driver()
