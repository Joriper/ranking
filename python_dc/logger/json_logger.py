import logging
import json
from datetime import datetime
import os,ast
from bson import ObjectId
import re
from settings import JSON_LOGS_PATH

class JsonFormatter(logging.Formatter):
    def format(self, record):
        get_msg = ast.literal_eval(record.getMessage())
        log_data = {
            'timestamp': self.formatTime(record),
            'sitename': get_msg['name'],
            'queue_id': get_msg['_id'],
            'level': record.levelname,
            'message': get_msg['message'],
            # 'logger_name': record.name,
            # 'process': record.process,
            # 'thread': record.thread,
            'module': record.module,
            'func_name': record.funcName,
            'line_no': record.lineno,
            'exception': str(record.exc_info),
            'stack_trace': self.formatException(record.exc_info) if record.exc_info else None
        }
        return json.dumps(log_data) + ','



class JsonLogger:
    DIR_NAME = JSON_LOGS_PATH
    logger_pool = dict()
    
    def _get_logger_file_name(self, _datetime, _queueid, _website_name):

        return f"{_datetime}-{_queueid}-{_website_name}.json"
    
    def _check_logger_dir(self, file_name):
        if not os.path.exists(file_name):
            return False
        else:
            return True
            # os.makedirs(os.path.dirname(file_name))
    
    def _get_file_logger(self, filename):
        logger = logging.getLogger(filename)
        file_handler = logging.FileHandler(f"{self.DIR_NAME}/{filename}")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)
        return logger        

    def get_logger(self, _datetime, _queueid, _website_name):
        filename = self._get_logger_file_name(_datetime, _queueid, _website_name.replace(".","_"))
        if self.logger_pool.get(filename):
            return self.logger_pool.get(filename)

        self.logger_pool[filename] = self._get_file_logger(filename)
        return self.logger_pool.get(filename)


class LogEvent:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    
    def clean_url(self, url):
        pattern = r"https?://(?:www\.)?([^/]+)"
        match = re.match(pattern, url)
        if match:
            return match.group(1)
        else:
            return url


    def __init__(self, queue_item:dict, message:str, level:int=DEBUG, *args, **kwargs):
        """_summary_

        Args:
            queue_item (_type_): {"created_at": x, "_id": y, "url": z}
            message (_type_): message to log
            level (_type_): error level, default 0
        """
        logger = JsonLogger()
        logger = logger.get_logger(
            str(queue_item.get('created_at')), 
            str(queue_item.get('_id')), 
            self.clean_url(str(queue_item.get('url')))
        )
        logger.setLevel(logging.DEBUG)
        if not args:
            args = []
        kwargs['exc_info'] = True
        logger._log(level, {"name":queue_item['name'],"_id":str(queue_item['_id']),"message":message}, args, **kwargs)

if __name__ == "__main__":
    sample_item = {"created_at": datetime.now(), "_id": ObjectId(), "url": "https://testurl.com/"}

    try:
        a = dict()
        LogEvent(sample_item, "Logger Testing one", LogEvent.INFO,)    
        a['d']
    except Exception as e:
        LogEvent(sample_item, "Logger Testing", LogEvent.ERROR)    
