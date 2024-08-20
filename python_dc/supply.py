import argparse,asyncio,dotenv,sys,os
from Queue.queue import ProcessNext,SubamyaQueueNext
from run import Executor

root_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
sys.path.append(root_path)
from python_dp.Queues.queue import ProcessNextProcessing

parser = argparse.ArgumentParser(prog='NIC Tool',description='NIC DATA COLLECTOR')
parser.add_argument('--queue',help="Run NIC Tool as Job (Yes/NO)?")
parser.add_argument("--function_name",help='default:PROCESS_NEXT_IN_QUEUE')
parser.add_argument("--manu",action="store_const" ,const="manu",help="Should not passed with '--queue' for manual execution.[Example: python3 main.py --limit [0-9] --website WEBNAME --manu --function_name FUNNAME,] for multiple functions")
parser.add_argument("--website",help='Pass the website url')
parser.add_argument("--db",help="Set Database for Execution and table Example: Python3 main.py --db 'webalytics:process_insight'")
parser.add_argument("--function_list",dest="function_list",action="store_const",const="function_list",help='Get All function name for execution individual')
parser.add_argument("--type",help="Set Type of database [single or multiple] Example: python3 main.py --db 'DB_NAME:DB_COLL' --type 'single' ")
parser.add_argument("--thread",help="Specifiy thread [min=1,max=10]")
parser.add_argument("--update_id",help="Update specific group with Provided ID")
parser.add_argument("--host",help="Specify host of API Server")
parser.add_argument("--port",help="Specify port of server")
parser.add_argument("--group",help="Execute a group based[Example python nic.py --group NAME --website NAME]")
parser.add_argument("--subamya_queue",help="Run SUMBAMYA AS QUEUE[Default:Yes]")
parser.add_argument("--key",help="Specify Key name to process based on process[NOT IN USE ONLY USED BY DEVELOPER]")
parser.add_argument("--limit",help="Pass the limit [1-10] max")
parser.add_argument("--queue_type",help="Set full or pending")

parser.add_argument("--group_key",help="Specify the group key name")
parser.add_argument("--version",dest="version",action="store_const",const="version",help="NIC Tool version")

handle_arg=parser.parse_args()
if  handle_arg.version:
    print("0.4.2")
elif handle_arg.db != None and handle_arg.type !=None: 
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    db_tab = handle_arg.db.split(":")
    if handle_arg.type == "single":
        dotenv.set_key(dotenv_file,"NIC_DATABASE",db_tab[0])
        dotenv.set_key(dotenv_file,"NIC_SINGLE_EXECUTION",db_tab[1])
    elif type == "multiple":
        dotenv.set_key(dotenv_file,"NIC_DATABASE",db_tab[0])
        dotenv.set_key(dotenv_file,"NIC_DUMP_PROCESS_TABLE",db_tab[1])
    else:
        print("[-] Database Value Error 'single' or 'multiple'")
        sys.exit(1)
    print("[*] Database Set to -> {}".format(handle_arg.db))

elif handle_arg.group != None and handle_arg.website !=None:
    asyncio.run(ProcessNext(request_type="GROUP",group_name=handle_arg.group,website=handle_arg.website))
elif handle_arg.queue == "Yes"  and handle_arg.function_name=="PROCESS_NEXT_IN_QUEUE":
    asyncio.run(ProcessNext(thread=handle_arg.thread,request_type="Yes"))
elif handle_arg.queue == "NO" and handle_arg.function_name=="EXECUTOR" and handle_arg.website:
    asyncio.run(ProcessNext(thread=None,request_type="NO",name=handle_arg.website))
elif handle_arg.host != None and handle_arg.port !=None:
    Executor(handle_arg.host,handle_arg.port)
elif handle_arg.update_id != None and handle_arg.group != None and handle_arg.group_key != None:
    print("Called")
    asyncio.run(ProcessNext(update_id=handle_arg.update_id,group_name=handle_arg.group,keyname=handle_arg.key,request_type="update",group_key=handle_arg.group_key))
elif handle_arg.queue == "NO" and handle_arg.function_name=="PS_CALL" and handle_arg.website != None:
    queue_id= asyncio.run(ProcessNext(request_type="ps_web_collect_group_process",website_name=str(handle_arg.website)))
    asyncio.run(ProcessNextProcessing(request_type="NO",website_name=handle_arg.website,site_queue=queue_id))
elif handle_arg.subamya_queue == "Yes":
    asyncio.run(SubamyaQueueNext(request_type="SUGAMYA_QUEUE"))
else:
    raise ValueError("Invalid Argument supplied")
