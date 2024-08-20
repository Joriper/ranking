import requests,warnings,os,json

def  HttpRequestHandler(url):
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',        
    }
    print(url)
    request = requests.get(url,verify=False,headers=headers,timeout=120)
    
    #print("{}".format(request.url))
    # sys.stdout.write("\r / {}".format(request.url))
    # sys.stdout.flush()
    return request
    

def HttpPostRequestHandler(**kwargs):
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data = {
        "file":str(kwargs['data'])

    }
    request = requests.post(kwargs['url'],verify=False,data=data,headers=headers)
    print(request)
    return request.json()

def SugamyaHttpRequestHandler(**kwargs):
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        "Content-Type":"application/x-www-form-urlencoded",
        "sugamyaweb-service-name": "{}".format(os.environ['SUGAMYA_WEB_SERVICE_NAME']),
        "sugamyaweb-service-key": "{}".format(os.environ['SUGAMYA_WEB_SERVICE_TOKEN']),
        "Authorization": "Bearer {}".format(os.environ['SUGAMYA_WEB_API_TOKEN']),
        "Content-Type":"application/json"
    }

    if kwargs["type"] == "POST":
        body = {
            "name":kwargs['name'],
            "url":kwargs['site_url'],
            "testMode":kwargs['mode']
        }
        return requests.post(kwargs['url'],verify=False,data=json.dumps(body),headers=headers).json()
    elif kwargs["type"] == "GET":
        headers.pop("Content-Type")
        data = requests.get(kwargs['url'],headers=headers)
        return data.json()
    return
