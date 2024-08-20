
#########################################################

    ADG Online Solution Pvt Ltd
##########################################################
            WebAlytics NIC Collector

Author: Adgonline(Anujsayal)
Dated: 10-01-2024
Last-Updated: 16-Feb-2024
Description: We are not responsible for any damange to system caused by this application. without prior use of owner is prohibited

##########################################################

    How to Run NIC Data Collector/consilation

Run the Following Commands and follow instructions:

1. sudo apt-get update && sudo apt-get upgrade	[CMD]
2. Install Python3 in system(Ubantu/linux/windows)
3. Run "pip3 install -r requirements.txt"
4. Type "python3 main.py -h" for command line options
5. Follow the instructions run as per requirements

   EXAMPLE Usage:
6. python3 main.py --queue Yes --function_name PROCESS_NEXT_IN_QUEUE -> (For Setting the crone job/Ubantu/crone)
7. python3 main.py --group [GROUP_NAME] --website [WEBSITE_NAME] -> (For Collection of specific Group)
8. python3 main.py --host 0.0.0.0 --port [PORT_NUMBER] -> (For Running API SERVER)
9. python3 main.py --queue NO --function_name EXECUTOR --website [WEBSITE_NAME] -> (For IGNORE CRONE/QUEUE JOB And RUN to get output)
10. python3 main.py --update_id [QUEUE_ID] --group [GROUP_NAME] --group_key [MAIN_COLLECTION_KEY] --keyname [KEY_YOU_WANT_TO_UPDATE] ->(Only used by developer team)

##########################################################

    How to change DATABASE

python3 main.py --db "dbname:collection_name"

###########################################################
