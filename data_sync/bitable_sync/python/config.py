# -*- coding: UTF-8 -*-
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# load from env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
LARK_HOST = os.getenv("LARK_HOST")
APP_TOKEN=os.getenv("APP_TOKEN")
# localization
TABLE_NAME = '测试表1'
KEY_TYPE='消息类型'
KEY_ROLE='发送方'
KEY_CONTENT='消息内容'




