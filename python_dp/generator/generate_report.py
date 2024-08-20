from db.connection import *
import datetime,bson,json,sys
from bson import ObjectId
from python_dc.helpers.requester.requester import SugamyaHttpRequestHandler
from python_dc.helpers.urls.urls import GetURL

class GenerateReport:
    def __init__(self,**kwargs):
        self.sitename = kwargs['sitename']
        self.site = kwargs['site']
    
    async def GenerateSiteReport(self):
        store_data = {}
        psi_data = {}
        print(self.site['_id'])
        try:
            grammer = list(group_grammer.find({"id":str(self.site['_id'])}))[-1]
        except:
            grammer =[]
        try:
            psi = list(group_psi.find({"id":str(self.site['_id'])}))[-1]
        except:
            psi=[]
    
        try:
            psi_2 = list(group_psi_2.find({"id":str(self.site['_id'])}))[-1]
        except:
            psi_2=[]
    

        #########################3 Abhishek ###############################
        
        try:
            print("google m")
            googlemap_details_ = list(googlemaps_details.find({"id": str(self.site['_id'])}))[-1]
        except Exception as e:
            print("google_maps error",e)
            googlemap_details_ = []

        ######################### end #######################################



        ################################ ONLY FOR SEO ############################
        try:
            seo_group_data = list(group_seo.find({"id":str(self.site['_id'])}))[-1]
        except:
            seo_group_data=[]
        

        try:
            seo_top_10 = list(seo_nic.find({"id":str(self.site['_id'])}))[-1]
        except:
            seo_top_10=[]


        try:
            seo_dumps = list(seo_dump.find({"id":str(self.site['_id'])}))[-1]
        except:
            seo_dumps=[]
        
        ############################## END SEO ################################
        try:
            img_stat = list(group_img.find({"id":str(self.site['_id'])}))[-1]
        except:
            img_stat=[]
        
        try:
            text_stats = list(group_textstat.find({"id":str(self.site['_id'])}))[-1]
        except:
            text_stats=[]

        try:
            whois_stat = list(group_whois.find({"id":str(self.site['_id'])}))[-1]
        except:
            whois_stat=[]

        try:
            ssl_stat = list(group_ssl.find({"id":str(self.site['_id'])}))[-1]
        except:
            ssl_stat = []
        


        try:
            beautiful_stat = list(group_beautiful.find({"id":str(self.site['_id'])}))[-1]
        except:
            beautiful_stat =[]

        try:
            beautiful_stat_2 = list(group_beautiful_2.find({"id":str(self.site['_id'])}))[-1]            
        except:
            beautiful_stat_2 =[]

        try:
            automation_stat = list(group_automation.find({"id":str(self.site['_id'])}))[-1]
        except:
            automation_stat = []
        
        try:
            automation_stat_2 = list(group_automation_2.find({"id":str(self.site['_id'])}))[-1]
        except:
            automation_stat_2 = []

        #################### ABhishek #################
        try:
            access_keyword = list(group_accessibility.find({"id": str(self.site['_id'])}))[-1]
        except:
            access_keyword = []


        try:
            vul = list(group_vulerability.find({"id": str(self.site['_id'])}))[-1]
        except:
            vul = []

        try:
            advance_security = list(advance_security_response.find({"siteId": bson.ObjectId(str(self.site['site_id']))}))[-1]
        except:
            advance_security = []


        try:
            g_p_s = list(google_page_speed.find({"id": str(self.site['_id'])}))[-1]
        except:
            g_p_s = []


        ################### end #########################
        

        store_data['site_url']= self.site['url'] if "https" in self.site['url'] else "https://"+self.site['url']
        #store_data['sitename'] = self.sitename
        try:
            store_data["grammer_info"]=grammer['is_grammer_error']
        except Exception as error:
            store_data["grammer_info"]="Missing"

        store_data['queue_id'] = str(self.site['_id'])
        try:
            store_data['font_logo']=beautiful_stat['font_logo']
        except:
            store_data['font_logo'] = "Missing"
        try:
            store_data['multi_lang'] = beautiful_stat['multi_lang']
        except:
             store_data['multi_lang'] = "Missing"

        try:
            store_data['end_permit'] = beautiful_stat['end_permit']
        except:
            store_data['end_permit'] = "Missing"

        try:
            store_data['grievance'] = beautiful_stat['grievance']
        except:
            store_data['grievance'] = "Missing"

        try:
            store_data['social_media'] = beautiful_stat['social_media']
        except:
            store_data['social_media'] = "Missing"

        try:
            store_data['form_stat'] = beautiful_stat['form_stat']
        except:
            store_data['form_stat'] = "Missing"

        try:
            store_data['copyright'] = beautiful_stat['copyright']
        except:
            store_data['copyright'] = "Missing"

        try:
            store_data['correct_title'] = beautiful_stat['correct_title_']
        except:
            try:
                store_data['title'] = psi['title'] if psi.get("title") else "Missing"
            except:
                store_data['title'] = "Incorrect web"

        try:
            store_data['link_dist'] = beautiful_stat['link_dist']
        except:
            store_data['link_dist'] = "Missing"

        try:
            store_data['webhash'] = beautiful_stat['webhash']
        except:
            store_data['webhash'] = "Missing"

        try:
            store_data['site_logo'] = beautiful_stat['site_logo']
        except:
            try:
                store_data['site_logo'] = psi['site_logo'] if psi.get("site_logo") else "Missing"
            except:
                store_data['site_logo'] = "Incorrect web"

        try:
            store_data['meta_description'] = beautiful_stat['meta_description']
        except:
            try:
                store_data['meta_description'] = psi["meta_description"] if psi.get("meta_description") else "Missing"
            except:
                store_data['meta_description'] = "Incorrect web"

        try:
            store_data['change_detected'] = beautiful_stat['change_detected']
        except:
            store_data['change_detected'] = "Missing"

        try:
            store_data['cdns'] = beautiful_stat['cdns']
        except:
            store_data['cdns'] = "Missing"

        try:
            store_data['category'] = beautiful_stat['category']
        except:
            store_data['category'] = "Missing"

        try:
            store_data['download_excel_pdf']=beautiful_stat['download_excel_pdf']
        except:
            store_data['download_excel_pdf']= "Missing"

        try:
            store_data['click_depth']=beautiful_stat['click_depth']
        except:
            store_data['click_depth']= "Missing"

        try:
            store_data['online_trans'] = beautiful_stat['online_trans']
        except:
            store_data['online_trans'] = "Missing"

        try:
            store_data['is_opportunity'] = beautiful_stat['is_opportunity']
        except:
            store_data['is_opportunity'] = "Missing"

        try:
            store_data['pool_consult'] = beautiful_stat['pool_consult']
        except:
            store_data['pool_consult'] = "Missing"

        try:
            store_data['viewport_meta'] = beautiful_stat['viewport_meta']
        except:
            store_data['viewport_meta'] =  "Missing"

        try:
            store_data['gov_services'] = False
        except:
            store_data['gov_services'] = "Missing"

        try:
            store_data['is_400_500_error'] = beautiful_stat['is_400_500_error']
        except:
            store_data['is_400_500_error'] = "Missing"

        try:
            store_data['is_faq'] = beautiful_stat['is_faq']
        except:
            store_data['is_faq'] = "Missing"

        try:
            store_data['is_bread_crumb'] = beautiful_stat['is_bread_crumb']['status']
        except:
            store_data['is_bread_crumb'] =  "Missing"

        try:
            store_data['nav_across_site'] = beautiful_stat_2['nav_across_site']
        except:
            store_data['nav_across_site'] =  "Missing"

        try:
            store_data['site_map'] = beautiful_stat_2['site_map']
        except:
             store_data['site_map'] = "Missing"

        try:
            store_data['home_linked'] = beautiful_stat['home_linked']['status']
        except:
            store_data['home_linked'] = "Missing"

        try:
            store_data['static_assets'] = beautiful_stat_2['static_assets']
        except:
            store_data['static_assets'] = "Missing"

        try:
            store_data['backlink'] = beautiful_stat_2['backlink']
        except:
            store_data['backlink'] = "Missing"


        try:
            store_data['gov_respective'] = beautiful_stat_2['gov_respective']
        except:
            store_data['gov_respective'] = "Missing"

        try:
            store_data['is_descriptive'] = beautiful_stat_2['is_descriptive']
        except:
            store_data['is_descriptive'] = "Missing"

        try:
            store_data['broken_link'] = beautiful_stat_2['broken_link']
        except:
            store_data['broken_link'] =  "Missing"

        try:
            store_data['category'] = beautiful_stat_2['category']
        except:
             store_data['category'] ="Missing"

        try:
            store_data['about_page']= beautiful_stat_2['about_page']
        except:
            store_data['about_page']= "Missing"

        try:
            store_data['contact_page'] = beautiful_stat_2['contact_page']
        except:
            store_data['contact_page'] = "Missing"

        try:
            store_data['flagship'] = beautiful_stat_2['flagship']['status']
        except:
            store_data['flagship'] = "Missing"


        try:
            store_data['user_generated_content'] = beautiful_stat_2['user_generated_content']
        except:
            store_data['user_generated_content'] = "Missing"

        try:
            store_data['memorable_logo'] = beautiful_stat_2['memorable_logo']
        except:
            store_data['memorable_logo'] = "Missing"

        try:
            store_data['cdn_performace'] = beautiful_stat_2['cdn_performace']
        except:
            store_data['cdn_performace'] = "Missing"


        cross_browser = {}
        
        try:
            cross_browser['browser'] = automation_stat_2['cross_browser_testing']
        except:
            cross_browser['browser'] = "Missing"

        try:
            store_data['cross_browser_testing'] = cross_browser
        except:
            store_data['cross_browser_testing'] = "Missing"


        try:
            store_data['smooth_adjust'] = automation_stat_2['smooth_adjust']
        except:
            store_data['smooth_adjust'] = "Missing"

        try:
            store_data['easy_signup'] = automation_stat['easy_signup']
        except:
            store_data['easy_signup'] = "Missing"


        try:
            store_data['real_time_chatbot'] = automation_stat['real_time_chatbot']
        except:
             store_data['real_time_chatbot'] = "Missing"

        try:
            store_data['media_query'] = automation_stat['media_query']
        except:
             store_data['media_query'] = "Missing"


        try:
            store_data['different_sizes'] = automation_stat_2['different_sizes']['status']
        except:
            store_data['different_sizes'] =  "Missing"


        try:
            store_data['sort_filter'] = automation_stat_2['sort_filter']
        except:
            store_data['sort_filter'] = "Missing"


        try:
            store_data['form_input_responsive'] = automation_stat_2['form_input_responsive']
        except:
            store_data['form_input_responsive'] = "Missing"

        try:
            store_data['is_44_by_44'] = automation_stat_2['is_44_by_44']['status']
        except:
            store_data['is_44_by_44'] =  "Missing"

        try:
            store_data['ssl'] = ssl_stat['ssl_info']
        except Exception as error:
            print(error)
            store_data['ssl'] = "Missing"
        
        try:
            store_data['vulnerability'] = vul['vulnerability']
        except Exception as error:
            store_data['vulnerability'] = "Missing"

        try:
            store_data['mobile_compatability'] = automation_stat_2['mobile_compatability']
        except Exception as error:
            print(error)
            store_data['mobile_compatability'] = "Missing"



        try:
            dummy_dump = {}
            dummy_dump['cache'] = psi_2['cache']
            dummy_dump['error_rate'] = psi_2['error_rate']
            dummy_dump['third_party_scripts'] = psi_2['third_party_scripts']
            dummy_dump['network_latency'] = psi_2['network_latency']
            dummy_dump['responsive_image'] = beautiful_stat_2['responsive_image']
            dummy_dump['comment_share_media']=beautiful_stat_2['comment_share_media']
            dummy_dump['form_exits'] = beautiful_stat['form_exists']
            store_data['additional_questions'] = dummy_dump
        except:
            store_data['additional_questions']="Missing"

        try:
            dummy = {}
            dummy['strong_encryption']=ssl_stat['strong_encryption']
            dummy['security_headers']=ssl_stat['security_headers']
            dummy['cookie']=ssl_stat['cookie']
            dummy['captcha']=ssl_stat['captch']         
            store_data['secure_development_practice'] = ssl_stat['secure_development_practice']
            store_data['access_auth']=ssl_stat['access_auth']
            store_data['ssl_additional_questions']=dummy
        except Exception as error:
            print("ERRO SI",error)
            store_data['ssl_additional_questions']="Missing"


        try:
            store_data['performance_indicate'] = psi['performance_indicate']
        except:
            store_data['performance_indicate'] = "Missing"
        
        try:
            store_data['loading_exp'] = psi['loading_exp']
            store_data['origin_loading_exp'] = psi['origin_loading_exp']
            store_data['pg_shot'] = psi['pg_shot']
        except:
            pass

        try:
            store_data['request_total'] = psi['request_total']
        except:
            store_data['request_total'] =  "Missing"

        try:
            store_data['result_2s'] = automation_stat_2['result_2s']
        except:
            store_data['result_2s'] = "Missing"

        try:
            store_data['load_time'] = psi['load_time']
        except:
            store_data['load_time'] = "Missing"

        try:
            store_data['page_speed'] = automation_stat_2['page_speed']
        except:
            store_data['page_speed'] = "Missing"

        try:
            store_data['code_count'] = psi['code_count']
        except:
            store_data['code_count'] = "Missing"
        try:
            store_data['treemap'] = psi['treemap']
        except:
            store_data['treemap'] = "Missing"

        try:
            store_data['size_page'] = psi['size_page']
        except:
            store_data['size_page'] =  "Missing"

        try:
            store_data['metrics'] = psi_2['metrics']
        except:
            store_data['metrics'] = "Missing"

        try:
            store_data['cache_compress'] = psi_2['cache_compress']
        except:
            store_data['cache_compress'] = "Missing"

        try:
            store_data['mobile_friendly'] = psi['mobile_friendly']
        except:
            store_data['mobile_friendly'] = "Missing"

        try:
            store_data['user_experience'] = automation_stat_2['user_experience']
        except:
            store_data['user_experience'] = "Missing"
        
        try:
            stat_data = {
                "readablity":text_stats['clear_info']['readablity'],
                "score":text_stats['clear_info']['score']
            }
            store_data['clear_info'] = stat_data
        except:
            store_data['clear_info'] = "Missing"

        try:
            store_data['ownership_info'] = whois_stat['ownership_info']
        except:
            store_data['ownership_info'] = "Missing"

        try:
            store_data['effective_content'] = img_stat['effective_content']
        except Exception as error:
            store_data['effective_content'] = "Missing"

        try:
            store_data['imagery'] = img_stat['imagery']
        except Exception as error:
            store_data['imagery'] = "Missing"


        try:
            store_data['seo'] = seo_group_data['seo_slu_']
        except Exception as error:
            print(error)
            store_data['seo'] = "Missing"
        
        try:
            store_data['seo'] = seo_group_data['seo_slu_']
        except Exception as error:
            print(error)
            store_data['seo'] = "Missing"
        

        try:
            store_data['color_consistancy'] = automation_stat_2['color_consistancy']
        except Exception as error:
            print(error)
            store_data['color_consistancy'] = "Missing"
        
        try:
            store_data['over_optimization'] = seo_group_data['over_optimize']
        except Exception as error:
            print(error)
            store_data['over_optimization'] = "Missing"
        

        try:
            store_data['heading_optimize'] = seo_group_data['heading_optimize']
        except Exception as error:
            print(error)
            store_data['heading_optimize'] = "Missing"

        try:
            store_data['seo_top_links'] = seo_top_10['top_links']
        except Exception as error:
            print(error)
            store_data['seo_top_links'] = "Missing"
            

        try:
            store_data['seo_urls'] = seo_top_10['seo_urls']
        except Exception as error:
            print(error)
            store_data['seo_urls'] = "Missing"
        


        try:
            store_data['time_to_first_byte'] = psi['time_to_first_byte']
        except Exception as e:
            store_data['time_to_first_byte'] = "Incorrect TIME_TO_FIRST_BYTE"

        try:
            store_data['quicker_loading_page'] = psi['quicker_loading_page']
        except Exception as e:
            store_data['quicker_loading_page'] = "Incorrect quicker_loading_page"

        try:
            store_data['page_size_load'] = psi['page_size_load']
        except Exception as e:
            store_data['page_size_load'] = "Incorrect quicker_loading_page"

        try:
            store_data['minimize_numbers_requests'] = psi['minimize_numbers_requests']
        except Exception as e:
            store_data['minimize_numbers_requests'] = "Incorrect minimize_numbers_requests"
        try:
            store_data['access_keyword'] = access_keyword['keyword_access']
        except Exception as e:
            store_data['access_keyword'] = "Incorrect access_keyword"

        try:
            store_data['add_text'] = access_keyword['add_text']
        except Exception as e:
            store_data['add_text'] = "Incorrect add_text"

        try:
            store_data['googlemap_details'] = googlemap_details_['googlemap_details']
        except Exception as e:
            store_data['googlemap_details'] = "Incorrect googlemap_details"

        try:
            store_data['render_time'] = psi['render_time']
        except Exception as e:
            store_data['minimize_numbers_requests'] = "Missing"

        try:
            store_data['green_metrics'] = psi['green_metrics']
        except Exception as e:
            store_data['green_metrics'] = "Missing"



        try:
            store_data['green_metrics'] = psi['green_metrics']
        except Exception as e:
            store_data['green_metrics'] = "Missing"


        try:
            store_data['web_hash'] = psi['web_hash']
        except Exception as e:
            store_data['web_hash'] = "Missing"

        ############################# Advance security #################################
        try:
            store_data['advance_security_classification'] = json.dumps(advance_security['classifications'])
        except Exception as e:
            print(e)
            
            store_data['advance_security_classification'] = "Missing"

        try:
            store_data['advance_security_vulnerabilities'] = json.dumps(advance_security['vulnerabilities'])
        except Exception as e:
            print(e)
            store_data['advance_security_vulnerabilities'] = "Missing"

        ############################## Google page speed ###################################
        try:
            store_data['g_p_s'] = g_p_s['data']
        except Exception as e:
            store_data['g_p_s'] = "Missing"


        try:
            check_result = access_keyword['accessibility']
            if check_result['status'] == True:
                vio_data = check_result['reason'][-1]['violations']
                passes_data=check_result['reason'][-1]['passes']   
                for h in vio_data:
                    h['status']=False
                    h['reason']=h['nodes'] 
                    h['name']=h['description']
                    del h['nodes']
                    del h['description']

                for s in passes_data:
                    s['status']=True
                    s['reason']=s['nodes']
                    s['name']=s['description']
                    del s['nodes']
                    del s['description']
                store_data['accessibility'] = vio_data+passes_data
            else:
                store_data['accessibility'] = []
        except Exception as error:
            print("Error soun",error)
            this_function_name = sys._getframe(  ).f_code.co_name                     
            Error(error,self.__class__.__name__,this_function_name)

        store_data['type']=self.site['type']
        store_data['site_id'] = self.site['site_id']
        store_data['created_at'] = str(datetime.datetime.now())

        print(store_data)
        process_collection.insert_one(store_data)
        queue_collection.update_one({"_id":ObjectId(str(self.site['_id']))},{"$set":{"processed":1}})        
        group_accessibility.update_one({"_id":str(self.site['_id'])},{"$set":{"processed":1}})        
        group_grammer.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_beautiful.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_beautiful_2.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_psi.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_psi_2.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_img.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_whois.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_textstat.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_ssl.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_automation.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_automation_2.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        group_vulerability.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})

        sugamya_data.update_one({"id":str(self.site['_id'])},{"$set":{"processed":1}})
        googlemaps_details.update_one({"id": str(self.site['_id'])}, {"$set": {"processed": 1}})
        queue_collection.find_one_and_update({"_id":ObjectId(self.site['_id'])},{"$set":{"status":"done","end_at":str(datetime.datetime.now())}})
