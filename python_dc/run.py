import os
import uvicorn

def Executor(host,port):
    PATH=str(os.path.dirname(os.getcwd()))+"/python_dp/log_config.ini"
    uvicorn.run("server:app", host=str(host), port=int(port))