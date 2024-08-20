from data_helper.collect import *
from groups import *
from helpers.requester.requester import SugamyaHttpRequestHandler
from helpers.urls.urls import GetURL
import sys,bson,datetime,uuid,bson
from db.connection import *
from logger.json_logger import LogEvent
import pdb


class ExecutorHandler:
    def __init__(self,sites):
        self.sites = sites
        self.queue_id = str(self.sites['_id'])
        self.site_id = str(self.sites['site_id'])
        self.site_name = str(self.sites['name'])
        self.site_url = str(self.sites['url']) if "https" in self.sites['url'] else "https://"+self.sites['url']
        self.random_id = str(uuid.uuid4())


        self.sites['url']=self.site_url
        self.site = self.sites
    async def Executor(self):
        queue_item = None
        try:
            if "https" in self.site_url or  "http" in self.site_url:
                queue_collection.find_one_and_update({"_id":self.site['_id']},{"$set":{"status":"working","processed":0,"start_at":str(datetime.datetime.now())}})
                queue_item = queue_collection.find_one({"_id":self.site['_id']})
                # Process Initiated Log
                LogEvent(queue_item, "process initiated", LogEvent.INFO)
                site_host = self.site_url.split("://")[1].replace("/","")
                collected_data = await NIC_TransporterDataCollectionHandler(site_url=self.site_url,site_host=site_host,site_id=self.site_id,random_id=self.random_id,queue_id=self.queue_id,site_name=self.site_name, queue_item=queue_item).Transport()
                google_page_speed.insert_one({"site_id":bson.ObjectId(self.site_id),"id":str(self.queue_id),"data":collected_data['page_speed']['insights'],"created_at":str(datetime.datetime.now()),"url":self.site_url,"name":self.site_name}) if "Unable to process request" not in str(collected_data['page_speed']['insights']) else False
                LogEvent(queue_item, "Fetching Google Maps info", LogEvent.INFO)
                await Google_maps_details(site_url=self.site_url, site_host=site_host, site_id=self.site_id,
                                        random_id=self.random_id, queue_id=self.queue_id,
                                        site_name=self.site_name, queue_item=queue_item).get_place_details()

                LogEvent(queue_item, "Serp Collection Handler", LogEvent.INFO)
                SerpCollectionHandler(site_url=self.site_url,site_host=site_host,site_id=self.site_id,random_id=self.random_id,queue_id=self.queue_id,site_name=self.site_name).InitializeSerp()

                if len(collected_data) > 0:
                    main_reco = list(sites_collection.find({'queue_id':"%s" % self.queue_id,'processed':{'$exists':False}}))
                    LogEvent(queue_item, "Group_Beautiful Initiating", LogEvent.INFO)
                    await Group_Beautiful(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group_Beautiful_2 Initiating", LogEvent.INFO)
                    await Group_Beautiful_2(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group PSI started", LogEvent.INFO)
                    await Group_Psi(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()

                    LogEvent(queue_item, "Group PSI 2 started", LogEvent.INFO)
                    await Group_Psi_2(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()

                    LogEvent(queue_item, "Group Grammer Started", LogEvent.INFO)
                    await Group_Grammer(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group Tex Stat Started", LogEvent.INFO)
                    await Group_Texstat(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group SSL Started", LogEvent.INFO)
                    await Group_SSL(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group WHOIS Started", LogEvent.INFO)
                    await Group_Whois(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group Automation Started", LogEvent.INFO)
                    await Group_Automation(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group Automation 2 Started", LogEvent.INFO)
                    await Group_Automation_2(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group IMG Started", LogEvent.INFO)
                    await Group_Img(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group SEO Started", LogEvent.INFO)
                    await Group_SEO(site=self.site,uid=self.random_id,collected=collected_data, queue_item=queue_item).GroupCaller()
                    
                    print("Wfwfwfwf")
                    LogEvent(queue_item, "Group Group_Accessibility Started", LogEvent.INFO)
                    await Group_Accessibility(site=self.site, uid=self.random_id, collected=collected_data,queue_id=self.queue_id, queue_item=queue_item).GroupCaller()
                    
                    LogEvent(queue_item, "Group Group_Vulnerability Started", LogEvent.INFO)
                    await Group_Vulnerability(site=self.site, uid=self.random_id, collected=collected_data,queue_id=self.queue_id, queue_item=queue_item).GroupCaller()



                    

                    LogEvent(queue_item, "Updating Report", LogEvent.INFO)
                    queue_collection.find_one_and_update({"_id":self.site['_id']},{"$set":{"status":"done","end_at":str(datetime.datetime.now()),"sms_status":False,"email_status":False}})
                    
                    LogEvent(queue_item, "Updating Report line 2", LogEvent.INFO)
                    queue_collection.insert_one({"name":self.site_name,"site_id":bson.ObjectId(self.site_id),"url":self.site_url,"created_at":datetime.datetime.now(),"updated_at":datetime.datetime.now(),"status":"pending","type":"full","processed":0,"first_report":False,"sms_status":False,"email_status":False,"execution_date":str(datetime.datetime.now().strftime('%d/%m/%Y'))})
                    LogEvent(queue_item, "Updating Report markign done", LogEvent.INFO)
                    print("fucked")
                    return str(self.site["_id"])    
                LogEvent(queue_item, "Updating Report markign done", LogEvent.INFO)
                queue_collection.find_one_and_update({"_id":self.site['_id']},{"$set":{"status":"done","end_at":str(datetime.datetime.now())}})            
                print("caleeeee")


        except Exception as error:
            if queue_item:
                LogEvent(queue_item, "Error in main executor", LogEvent.ERROR)
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        
class GroupCallHandler:
    def __init__(self):
        self.random_id = str(uuid.uuid4())

    async def GroupHandler(self,sitename,group_name,**kwargs):
        if kwargs.get("web"):
            site = kwargs['web']
        else:
            site = list(queue_collection.find({"name":sitename,"status":"pending","type":"full"}).limit(1))
        if len(site) > 0:
            site=site[-1]
            queue_collection.find_one_and_update({"_id":site['_id']},{"$set":{"status":"working","start_at":str(datetime.datetime.now())}})
            site_url = site['url']
            site_host = site_url.split("://")[1].replace("/","")
            queue_id = str(site['_id'])
            site_id = str(site['site_id'])             
            data = await NIC_TransporterDataCollectionHandler(site_url=site_url,site_host=site_host,site_id=site_id,random_id=self.random_id,queue_id=queue_id,site_name=site['name']).Transport()
            await getattr(sys.modules[__name__],group_name)(site=site,uid=self.random_id,collected=data).GroupCaller()
            queue_collection.find_one_and_update({"_id":site['_id']},{"$set":{"status":"done","end_at":str(datetime.datetime.now())}})
            getattr(sys.modules[__name__],group_name.lower()).find_one_and_update({"id":queue_id},{"$set":{"processed":0,"status":"done"}})


class SugamyaHandler:
    def __init__(self,sites):
        self.site = sites
        self.queue_id = str(self.site['_id'])
        self.site_id = str(self.site['site_id'])
        self.site_name = str(self.site['name'])
        self.site_url = str(self.site['url'])
        self.random_id = str(uuid.uuid4())
    
    async def SugamyaExecutor(self):
        if "https" in self.site_url or  "http" in self.site_url:
            get_sugmy_response = SugamyaHttpRequestHandler(type="POST",url=GetURL(type="sugmya_post"),name=self.site_name,site_url=self.site_url,mode="single_page")
            queue_sugamya.find_one_and_update({"_id":self.queue_id},{"$set":{"status":"in_progress","sugamya_request_id":get_sugmy_response['id'],"sugamya_status":get_sugmy_response['status']}})

            queue_sugamya.insert_one({"name":self.site['name'],"site_id":bson.ObjectId(self.site_id),"url":self.site['url'],"created_at":datetime.datetime.now(),"updated_at":datetime.datetime.now(),"status":"pending","processed":0})


            all_inprogress = list(queue_sugamya.find({"status":"in_progress"}).limit(10))

            if len(all_inprogress) > 0:
                for in_progrss_entry in all_inprogress:
                    result = SugamyaHttpRequestHandler(type="GET",url=GetURL(type="sugmya_get",web_id=in_progrss_entry["sugamya_request_id"]))

                    if result['testRun']['status'] == "COMPLETE" or result['testRun']['status'] == "FAILURE":
                        sugamya_data.insert_one({"site_id":in_progrss_entry['site_id'],"id":str(in_progrss_entry["_id"]),"name":in_progrss_entry["name"],"data":result})
                        queue_sugamya.find_one_and_update({"_id":str(in_progrss_entry['_id'])},{"$set":{"status":"done" if result['testRun']['status'] == "COMPLETE" else "failed","sugamya_status":result['testRun']['status']}})


class UpdateGroup:
    def __init__(self):
        self.random_id = str(uuid.uuid4())


    async def UpdateGroupHandler(self,**kwargs):
        for result_set in kwargs['update_id'].split(","):
            
            print(result_set)
            site = list(queue_collection.find({"_id":bson.ObjectId(result_set)}))
            print(site)
            if len(site) > 0:
                site=site[-1]
                site_url = site['url']
                site_host = site_url.split("://")[1].replace("/","")
                queue_id = str(site['_id'])
                site_id = str(site['site_id'])   
                
                data = await NIC_TransporterDataCollectionHandler(site_url=site_url,site_host=site_host,site_id=site_id,random_id=self.random_id,queue_id=queue_id,site_name=site['name']).Transport()
                update_data = list(process_collection.find({"queue_id":"{}".format(queue_id)}))
                if len(update_data) > 0:
                    result_data = await getattr(sys.modules[__name__],kwargs['group_name'])(site=site,uid=self.random_id,collected=data).GroupCaller()
                    import pdb;pdb.set_trace()
                    getattr(sys.modules[__name__],kwargs['group_name'].lower()).delete_many({"id":"{}".format(queue_id)})
                    getattr(sys.modules[__name__],kwargs['group_name'].lower()).insert_one(result_data[-1])
                
                    if kwargs['keyname'] in list(update_data[-1].keys()):
                        process_collection.find_one_and_update({"queue_id":"{}".format(queue_id)},{"$set":{"{}".format(kwargs['keyname']):result_data[-1]['{}'.format(kwargs['group_key'])]}})
                        print("Called and procssed")
                    else:
                        print("Invalid Key Supplied")
                else:
                    print("Queue ID NOT FOUND")
                #getattr(sys.modules[__name__],kwargs['group_name'].lower()).find_one_and_update({"id":queue_id},{"$set":{"processed":0,"status":"done"}})
