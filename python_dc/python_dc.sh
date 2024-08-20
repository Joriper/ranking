#!/bin/bash

# Run DC for python script

cd /home/adg-admin/apps/Engine/python_dc/

nohup /home/adg-admin/apps/Engine/env/bin/python3 /home/adg-admin/apps/Engine/python_dc/main.py --queue Yes --function_name PROCESS_NEXT_IN_QUEUE >>  /home/adg-admin/apps/Engine/python_dc/job.log &


