import json

# 消息类型  发送方  内容
def save_message(type, role, content):
    # 读取现有的JSON文件内容
    try:
        with open('message_log.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        # 如果文件不存在，则初始化为一个空数组
        existing_data = []

    # 新对象
    new_object = {"type": type, "role": role, "content": content}

    # 添加新对象到数组中
    existing_data.append(new_object)

    # 将更新后的数组写回JSON文件
    with open('message_log.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

# save_message('11', '22', 'content')