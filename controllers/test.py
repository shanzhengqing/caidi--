from chatgpt.chatgpt_official import reply_test35
from flask import request, Response

role_info = {
    'test':'You are ChatGPT, a large language model trained by OpenAI.',
    }


def test_webgpt(types='test'):
    if request.method == 'POST':
        # echo_str = line_chat_post(request, types)
        return line_chat_post(request, types)

def wait_for_reply35(id0, textrvd, role_msg):
    if not textrvd:
        content = '请输入信息。'
    elif not id0:
        query = [
            {'role':'system', 'content':role_msg},
            {'role':'user', 'content':textrvd}
            ]
        content = reply_test35(query)
        return content
    # return content
    

# 开启消息接受模式时验证接口连通性
def line_chat_post(request, types): 
    
    try:
        textrvd = request.get_json()['query']
    except Exception as e:
        textrvd = None
    
    role_msg = role_info[types]
    query = [
            {'role':'system', 'content':role_msg},
            {'role':'user', 'content':textrvd}
            ]
    
    # data = {'response':wait_for_reply35(None, textrvd, role_msg)}
    return Response(reply_test35(query), mimetype='text/event-stream')