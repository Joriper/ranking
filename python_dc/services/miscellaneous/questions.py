import whois,nltk
from helpers.time_percentage.tim_per import timedelta_percentage
from newspaper import Article
from helpers.requester.requester import HttpRequestHandler


class Miscellaneous:
    def __init__(self,**kwargs):
        self.lighthouse=kwargs['lighthouse']
        self.loading_exp=kwargs['loading_exp']
        self.site_url=kwargs['site_url']
        self.site_host=kwargs['site_host']
        self.age_aut_per=0
        self.keyword_per = 0
    
    async def mobile_resp_per(self):
        fcp = self.loading_exp["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"]
        fid = self.loading_exp["metrics"]["FIRST_INPUT_DELAY_MS"]["percentile"]
        lcp = self.loading_exp["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]
        cls = self.loading_exp["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]
        percentage = fcp+fid+lcp+cls
        fcp_per=(fcp/percentage)*100
        fid_per=(fid/percentage)*100
        lcp_per=(lcp/percentage)*100
        cls_per=(cls/percentage)*100
        self.total_percentage = {
            "fcp_per":fcp_per,
            "fid_per":fid_per,
            "lcp_per":lcp_per,
            "cls_per":cls_per
        }
        return self.total_percentage
    
    async def domain_age_url(self):
        TOTAL_DAY_SECS = 86400.0
        exp_date = whois.whois(self.site_url)['expiration_date']
        self.age_aut_per=round(timedelta_percentage(exp_date) * 100 ,2)
        return self.age_aut_per
    
    async def keywords_on_page(self):
        nltk.download('punkt')
        article = Article('')
        parser = HttpRequestHandler(self.site_url)
        article.download(parser.content)
        article.parse()

        if len(article.keywords) > 0:
            self.keyword_per = article[0]/len(article.keywords) * 100
        return self.keyword_per




