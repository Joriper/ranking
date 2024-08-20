from pymongo import MongoClient
from dotenv import load_dotenv
from error.error import Error
import os

try:
    load_dotenv()
    connection = MongoClient(os.environ['MONGO_CONNECTION'])
    database = connection[os.environ['NIC_DATABASE']]
    sites = database[os.environ['NIC_WEBSITES']]
    sites_collection = database[os.environ['NIC_DUMP_TABLE']]
    process_collection = database[os.environ['NIC_DUMP_PROCESS_TABLE']]
    
    queue_collection = database[os.environ['NIC_QUEUE']]

    group_psi = database[os.environ['NIC_GROUP_PSI']]
    group_psi_2 = database[os.environ['NIC_GROUP_PSI_2']]

    group_automation = database[os.environ['NIC_GROUP_AUTOMATION']]
    group_grammer = database[os.environ['NIC_GROUP_GRAMMER']]
    group_ssl = database[os.environ['NIC_GROUP_SSL']]
    group_textstat = database[os.environ['NIC_GROUP_TEXSTAT']]
    group_beautiful = database[os.environ['NIC_GROUP_BEAUTIFUL']]
    group_whois = database[os.environ['NIC_GROUP_WHOIS']]
    group_automation_2 = database[os.environ['NIC_GROUP_AUTOMATION_2']]
    group_beautiful_2 = database[os.environ['NIC_GROUP_BEAUTIFUL_2']]
    group_img = database[os.environ['NIC_GROUP_IMG']]
    free_text = database[os.environ['NIC_FREE_TEXT']]
    queue_sugamya = database[os.environ['SUGAMYA_QUEUE']]
    sugamya_data = database[os.environ['SUGAMYA_DATA']]
    group_accessibility = database[os.environ['NIC_GROUP_ACCESSIBILITY']]
    nic_settings = database[os.environ['NIC_CRON_SETTINGS']]
    seo_nic = database[os.environ['NIC_SEO_ANALYZE']]
    seo_dump = database[os.environ['NIC_SEO_DUMP']]
    group_seo = database[os.environ['NIC_GROUP_SEO']]
    group_vulerability = database[os.environ['NIC_GROUP_VULNERABILITY']]
    googlemaps_details = database[os.environ['GOOGLE_MAPS_DETAILS']]
    google_page_speed = database[os.environ['GOOGLE_PAGE_SPEED']]
    advance_security_response = database[os.environ['ADVANCE_SECURITY_RESPONSE']]

except ConnectionError as error:
    Error(error,"MONGO","MONGO")
    print("Connection Failed")
