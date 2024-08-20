def GetURL(**kwargs):
    url = ""
    if kwargs['type'] == "normal":
        url = "https://content-pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url={}".format(kwargs['url'])
    elif kwargs['type'] == "access":
        url = "https://content-pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?category=ACCESSIBILITY&url={}&strategy=DESKTOP".format(kwargs['url'])
    elif kwargs['type']== "save_img":
        url = "https://api.websiteranking.ai/api/docsave"
    
    elif kwargs['type'] == "sugmya_post":
        url = "https://sugamyaweb.gov.in/api/external-benchmarking/run-test"
    elif kwargs['type'] == "sugmya_get":
        url = "https://sugamyaweb.gov.in/api/external-benchmarking/test-runs/{}".format(kwargs['web_id'])

    elif kwargs['type'] == "page_speed_screenshot":
        url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?key=AIzaSyCmVx0XGLUlMA3N1WKz6t4xcO_iVgmCwBI&url={}".format(kwargs['url'])

    elif kwargs['type'] == 'google_maps':
        placeid = kwargs.get('place_id')
        api_key = kwargs.get('api_key')
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={placeid}&key={api_key}&fields=name,formatted_address,formatted_phone_number,website,reviews"

    elif kwargs['type'] == "mobile":
        url= "https://content-pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?category=PERFORMANCE&url={}&strategy=MOBILE".format(kwargs['url'])

    elif kwargs['type'] == "comptability":
        url = "https://content-pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?category=PERFORMANCE&url={}&strategy=DESKTOP".format(kwargs['url'])


    return url
    
