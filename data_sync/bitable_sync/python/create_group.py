import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from config import *


def create_group(name, description):
    # 创建client
    client = lark.Client.builder() \
        .app_id(APP_ID) \
        .app_secret(APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateChatRequest = CreateChatRequest.builder() \
        .user_id_type("open_id") \
        .set_bot_manager(False) \
        .request_body(CreateChatRequestBody.builder()
            .avatar("default-avatar_44ae0ca3-e140-494b-956f-78091e348435")
            .name(name)
            .description(description)
            .i18n_names(I18nNames.builder()
                .zh_cn(name)
                .en_us("group chat")
                .ja_jp("グループチャット")
                .build())
            .owner_id("ou_bee335adcd97c7ab71230ffe3f4660b7")  # 群主id
            .user_id_list(["ou_bee335adcd97c7ab71230ffe3f4660b7"])  # 成员id
            .bot_id_list(["cli_a7f57dda3238d00d"])
            .group_message_type("chat")
            .chat_mode("group")
            .chat_type("private")
            .join_message_visibility("all_members")
            .leave_message_visibility("all_members")
            .membership_approval("no_approval_required")
            .restricted_mode_setting(RestrictedModeSetting.builder()
                .status(False)
                .screenshot_has_permission_setting("all_members")
                .download_has_permission_setting("all_members")
                .message_has_permission_setting("all_members")
                .build())
            .urgent_setting("all_members")
            .video_conference_setting("all_members")
            .edit_permission("all_members")
            .hide_member_count_setting("all_members")
            .build()) \
        .build()

    # 发起请求
    response: CreateChatResponse = client.im.v1.chat.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    
    chat_id = response.data.chat_id
    return chat_id


