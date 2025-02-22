# -*- coding: UTF-8 -*-
import json
import api
import config
import logging
from datetime import datetime
import utils
from mock import schema, name_map

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.ERROR)

import os
logging.info(os.getcwd())



table_id = "tblGgIqQlggNY50s"
def create_table(client, access_token):
    global table_id
    table_id = client.create_table(access_token, config.APP_TOKEN, config.TABLE_NAME)

def write_bitable(client: api.Client, access_token, schema, name_map) -> str:
    '''write project release date info to bitable'''
    # table_id = client.create_table(access_token, config.APP_TOKEN, config.TABLE_NAME)
    global table_id
    if table_id == "":
        create_table(client, access_token)
    resp = client.get_fields_list(access_token, config.APP_TOKEN, table_id)
    current_fields = resp['items']

    for index, (field_name, field_type) in enumerate(schema.items()):
        try:
            if index >= len(current_fields):
                print(client.add_field(access_token, config.APP_TOKEN, table_id, name_map[field_name], field_type))
            else:
                print(client.update_field(
                    access_token, 
                    config.APP_TOKEN, 
                    table_id, 
                    current_fields[index]['field_id'], 
                    name_map[field_name],
                    field_type))
        except utils.LarkException as e:
            if e.code == 1254606: # DataNotChange
                pass
            else:
                raise

    resp = client.get_records_list(access_token, config.APP_TOKEN, table_id)
    current_records = resp['items']
    if current_records is None:
        current_records = []

    updated_records = []
    created_records = []
    with open('message_log.json', 'r', encoding='utf-8') as f:
        data = json.load(f) 
    raw_data = data

    for index, version_info in enumerate(raw_data):
        fields = {}
        for field_name, field_value in version_info.items():
            # 时间换算
            if schema[field_name] == 5: 
                field_value = datetime.strptime(field_value, '%Y-%m-%d').timestamp() * 1000
            fields[name_map[field_name]] = field_value
        if index >= len(current_records): 
            created_records.append({'fields': fields})
        else:
            updated_records.append({'record_id': current_records[index]['record_id'], 'fields': fields})
    if updated_records:
        resp = client.batch_update_records(access_token, config.APP_TOKEN, table_id, updated_records)
    if created_records:
        resp = client.batch_create_records(access_token, config.APP_TOKEN, table_id, created_records)
    return table_id

def update_bitable():
    '''write project release date info to bitable and sync it to calendar'''
    # init api client
    client = api.Client(config.LARK_HOST)

    # get tenant access token        
    access_token = client.get_tenant_access_token(config.APP_ID, config.APP_SECRET)

    # create a new table and push local json-like version iteration data to it
    table_id = write_bitable(client, access_token, schema, name_map)
    print("数据已更新到表格中")


# if __name__=="__main__":
#     update_bitable()
