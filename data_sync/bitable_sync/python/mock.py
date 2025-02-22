import json
from config import KEY_TYPE, KEY_ROLE, KEY_CONTENT
schema = {
    "type": 1,
    "role": 1,
    "content": 1
}

name_map = {
    "type": KEY_TYPE,
    "role": KEY_ROLE,
    "content": KEY_CONTENT
}

'''with open('message_log.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
raw_data = data'''
