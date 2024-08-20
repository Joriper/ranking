import os
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JSON_LOGS_PATH = os.path.join(root_path, 'JSON_LOGS')

if not os.path.exists(JSON_LOGS_PATH):
    os.makedirs(JSON_LOGS_PATH)