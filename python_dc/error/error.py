import os,datetime
def Error(message,classname,funname):
    if os.path.exists(os.getcwd()+"/error/"+"error.log"):
        with open(os.getcwd()+"/error/"+"error.log","a+") as error_:
            error_.writelines("{} {} -> {} -> {}\n".format(str(datetime.datetime.now()),message,classname,funname))
    else:
        with open(os.getcwd()+"/error/"+"error.log","w+") as error:
            error.writeliness("{} {} -> {} -> {}\n".format(str(datetime.datetime.now()),message,classname,funname))

