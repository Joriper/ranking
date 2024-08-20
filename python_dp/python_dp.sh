#!/bin/bash

# Run DP for python script


cd /home/adg-admin/apps/Engine/python_dp/

nohup /home/adg-admin/apps/Engine/env/bin/python3 /home/adg-admin/apps/Engine/python_dp/main.py  --process --queue Yes >>  /home/adg-admin/apps/Engine/python_dp/job.log &


