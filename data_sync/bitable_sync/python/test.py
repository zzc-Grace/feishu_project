import json

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *

def main():
    # 创建client
    # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token
    client = lark.Client.builder() \
        .app_id("cli_a7f57dda3238d00d") \
        .app_secret("J14nc2yi1nVq01Ad2LA5icOrlC6CnNSW") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: ListAppTableRequest = ListAppTableRequest.builder() \
        .app_token("SS7sbqYZ7a2KvXsUvFdcZbyonId") \
        .page_size(20) \
        .build()

    # 发起请求
    response: ListAppTableResponse = client.bitable.v1.app_table.list(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return


    # 处理业务结果
    # lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    print(json.loads(response.data.items))


if __name__ == "__main__":
    data = main()

    '''for item in data["data"]["items"]:
        if item["name"] == "测试表1":
            table_id = item["table_id"]
    print(table_id)'''