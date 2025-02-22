import json
import subprocess
from flask import Flask, request, jsonify, render_template

from create_group import create_group
from message_by_bot import send_message
from save_message import save_message
from update_bitable import update_bitable


app = Flask(__name__)
chat_id = "oc_9f165e4e1fb7cf3eb3687c4d0e941356"  # 默认群组


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_group', methods=['POST'])
def createGroup():
    data = request.get_json()
    group_name = data.get('group_name')
    group_description = data.get('group_description')
    
    # 创建群聊
    global chat_id
    chat_id = create_group(group_name, group_description)
    
    # 返回响应
    response = {
        'message': f'群组 "{group_name}" 已创建，描述为：{group_description[:50]}...'  # 简化描述显示
    }
    return jsonify(response), 200

@app.route('/send_message', methods=['POST'])
def sendMessage():
    data = request.get_json()
    content = data.get('content')
    # 发送消息
    send_message(content, chat_id)

    if content.startswith('#'):
        type = 'instruct'
    else:
         type = 'common'
    # 保存消息
    save_message(type, "robot", content)

    with open('message_log.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    # 更新到表格中
    update_bitable()
    
    return jsonify(data), 200

@app.route('/get_message', methods=['POST'])
def getMessage():
    with open('message_log.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return jsonify(data), 200

if __name__ == '__main__':
    # Python脚本的路径
    script_path = 'get_user_message.py'
    
    # 构造命令，这里使用'start cmd /k'来启动新终端并保持打开状态
    # 注意：脚本路径中的反斜杠需要双写，或者使用原始字符串前缀r
    command = f'start cmd /k python "{script_path}"'
    
    # 使用subprocess.Popen运行命令
    subprocess.Popen(command, shell=True)
    
    app.run(debug=True)
    # socketio.run(app, debug=True)  