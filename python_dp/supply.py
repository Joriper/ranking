import argparse,dotenv,sys,asyncio,os
root_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
sys.path.append(root_path)
from Queues.queue import ProcessNextProcessing

parser = argparse.ArgumentParser(prog='NIC Server',description='!Only for private purpose by ADG Online Solution')
parser.add_argument("--db",help="Set Database for Execution and table Example: Python3 main.py --db 'webalytics:process_insight'")
parser.add_argument("--type",help="Set Type of database [single or multiple] Example: python3 main.py --db 'DB_NAME:DB_COLL' --type 'single' ")
parser.add_argument("--process",dest="process",action="store_const",const="process",help="Process")
parser.add_argument("--group",help="Individual Group Process with group name")
parser.add_argument('--queue',help="Run NIC Tool as Job (Yes/NO)?")
parser.add_argument("--queue_sugamay",help="Process as Infinite for SUGMYA JOB. default[Yes]")
parser.add_argument("--website",help="NIC Tool version")

handle_arg=parser.parse_args()

if handle_arg.db != None and handle_arg.type !=None: 
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

elif handle_arg.queue == "Yes" and handle_arg.process == "process" and handle_arg.group ==None:
    asyncio.run(ProcessNextProcessing(request_type="Yes"))

elif handle_arg.queue == "GROUP" and handle_arg.process != None and handle_arg.group != None and handle_arg.website !=None:
    asyncio.run(ProcessNextProcessing(request_type="NO",name=handle_arg.website,group=handle_arg.group))

elif handle_arg.process != None and handle_arg.group == None and handle_arg.website != None:
    asyncio.run(ProcessNextProcessing(request_type="NO",website_name=handle_arg.website))

elif handle_arg.queue_sugamay == "Yes":
    asyncio.run(ProcessNextProcessing(request_type="queue_sugamay",is_sugamya=True))

else:
    raise ValueError("Invalid Argument supplied")

