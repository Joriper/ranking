#########################################################

    ADG Online Solution Pvt Ltd
##########################################################
            NIC Project

Author: Adgonline
Dated: 30-09-2023
Description: We are not responsible for any damange to system caused by this application.

##########################################################

    How to Run NIC Project

1. sudo docker pull selenium/standalone-chrome
2. docker run -d -p 4444:4444 -p 7900:7900  selenium/standalone-chrome:latest
3. sudo docker run -it solutions/nic_repo bash
4. sudo apt-get update
5. In env file change only IP "NIC_DOCKER_URI_CHROME" to http://{YOUR SERVER IP}:4444/wd/hub
6. Install Python3 in system(Ubantu/linux/windows)
7. Run "pip3 install -r requirements.txt"
8. Type "python3 main.py -h" for command line options
9. Follow the instructions run as per requirements

##########################################################

    How to change DATABASE

python3 main.py --db "dbname:collection_name"

###########################################################
