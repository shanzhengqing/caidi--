# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 12:32:18 2023

@author: shanz
"""

import openai
import tiktoken
import re
import time
import logging
import pandas as pd
from models.dbs import chatgpt_context, chatgpt_35, fingpt, gpt4_caidi, gpt4_fin, gpt35_hint
from fingpt.fin_vector import embed_n_search, search_pinecone
from .openai_config import openai_info

def set_openai_key(types:str, key_types='key_35'):
    # openai.api_key = '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'
    # openai.organization = 'org-9VandENRp26ATB4wGapUrDPn'
    types_refer = {
        'gpt4_caidi':'shanzhengqing0531', 'gpt4_fin':'shanzhengqing0531'
    }
    account = types_refer.get(types, 'shanzq53')
    openai.api_key = openai_info[account][key_types]
    openai.organization = openai_info[account]['orgnization']
    return True

ENCODER = tiktoken.get_encoding("cl100k_base")
# ENCODER = tiktoken.get_encoding("gpt2")

def get_max_tokens(prompt: str, types='gpt35') -> int:
    """
    Get the max tokens for a prompt
    """
    length_info = {'gpt4-8k':8192, 'gpt35':4096}
    max_length = length_info.egt(types, 4096)

    return max_length - len(ENCODER.encode(prompt, allowed_special={'<|endoftext|>',}))

def get_tokens_len(prompt: str) -> int:
    return len(ENCODER.encode(prompt, allowed_special={'<|endoftext|>',}))


def build_session_query(mdl, query, user_id):
    '''
    build query with conversation history
    e.g.  Q: xxx
          A: xxx
          Q: xxx
    :param query: query content
    :param user_id: from user id
    :return: query content with conversaction
    '''
    
    session = mdl.get(user_id)
    if session:
        if session[1] != '清除':
            prompt = session[1]
            # prompt += "Q: " + conversation["question"] + "\n\n\nA: " + conversation["answer"] + "<|endoftext|>\n"
            prompt = "{}Q: {}\nA: ".format(prompt, query)
            return prompt
        else:
            return "Q: {}\nA: ".format(query)
    else:
        return "Q: {}\nA: ".format(query)

def build_session_query35(mdl, query, user_id, role_msg):
    '''
    build query with conversation history
    e.g.  Q: xxx
          A: xxx
          Q: xxx
    :param query: query content
    :param user_id: from user id
    :return: query content with conversaction
    '''
    
    session = mdl.get(user_id)
    if session:
        if session[1] != '清除':
            prompt = [
              # {"role": "system", "content": "You are a helpful assistant."},
              # {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
              {"role": "system", "content": role_msg},
            ]
            splt = session[1]
            splt = splt.split('<|endoftext|>')
            splt = [i.split('\n\n\n') for i in splt]
            
            splt = pd.DataFrame([[i[0].replace('Q: ', '').strip(), '\n'.join(i[1:]).replace('A: ', '').strip()] if len(i)>=2 else [None, None] for i in splt]).dropna()
            if splt.shape[0] != 0:
                df = pd.DataFrame(index=range(2*splt.shape[0]))
                df.loc[0::2, 'content'] = splt[0].tolist()
                df.loc[1::2, 'content'] = splt[1].tolist()
                df.loc[0::2, 'role'] = 'user'
                df.loc[1::2, 'role'] = 'assistant'
                df = df.to_dict(orient='records')
                prompt.extend(df)
                prompt.append({"role":'user', "content":query})
            else:
                prompt.append({"role":'user', "content":query})
            return prompt
        else:
            prompt = [
              # {"role": "system", "content": "You are a helpful assistant."},
              # {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
              {"role": "system", "content": role_msg},
              {"role": "user", "content": query},
            ]
            return prompt
    else:
        prompt = [
          # {"role": "system", "content": "You are a helpful assistant."},
          # {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
          {"role": "system", "content": role_msg},
          {"role": "user", "content": query},
        ]
        return prompt

def save_session(types:str, mdl, query, answer, user_id):
    if types in ['fingpt']:
        max_tokens = 2100
    elif 'gpt4' in types:
        max_tokens = 4000
    else:
        max_tokens = 2500
    session = mdl.get(user_id)
    if session:
        if session[1] != '清除':
            prompt = session[1]
            prompt = "{}Q: {}\n\n\nA: {}<|endoftext|>\n".format(prompt, query, answer) 
        else:
            prompt = "Q: {}\n\n\nA: {}<|endoftext|>\n".format(query, answer) 
        # append conversation
        mdl.add_update(user_id, prompt)
    else:
        # create session
        prompt = "Q: {}\n\n\nA: {}<|endoftext|>\n".format(query, answer)
        mdl.add_update(user_id, prompt)
        
    # discard exceed limit conversation
    discard_exceed_conversation(mdl, user_id, max_tokens)
    return 1


def discard_exceed_conversation(mdl, user_id, max_tokens):
    session = mdl.get(user_id)
    pattern = re.compile(r'(.*)\n\n\n(.*)\n')
    contents = re.findall(pattern, session[1])
    count = 0
    count_list = list()
    for i in range(len(contents)-1, -1, -1):
        # count tokens of conversation list
        history_conv = contents[i]
        count += get_tokens_len(history_conv[0])
        count += get_tokens_len(history_conv[1])
        count_list.append(count)

    for c in count_list:
        if c > max_tokens:
            # pop first conversation
            contents.pop(0)
    
    contents = ['\n\n\n'.join(i) for i in contents]
    contents = [i+'<|endoftext|>' if '<|endoftext|>' not in i else i for i in contents]
    contents = '\n'.join(contents)
    contents = '{}\n'.format(contents)
    mdl.add_update(session[0], contents)
    return 

def clear_session(mdl, user_id):
    mdl.add_update(user_id, '清除')
    return True
            
        
def reply(query, user_id, role_msg, context='35'):
    import sys
    # acquire reply content
    if context == '清除1':
        # app_gptc.send_text('清除', id=[user_id])
        clear_session(chatgpt_context, user_id)
        return '【上下文已全部清空！】'
    elif context == '清除35':
        clear_session(chatgpt_35, user_id)
        return '【上下文已全部清空！】'
    elif context == '清除fin':
        clear_session(fingpt, user_id)
        return '【上下文已全部清空！】'
    elif context == '清除gpt4_fin':
        clear_session(gpt4_fin, user_id)
        return '【上下文已全部清空！】'
    elif context == '清除gpt4_caidi':
        clear_session(gpt4_caidi, user_id)
        return '【上下文已全部清空！】'
    elif context == '清除gpt35_hint':
        clear_session(gpt35_hint, user_id)
        return '【上下文已全部清空！】'
    elif context == 'search_fin':
        res = search_pinecone(query, 10, 'financial-vector')
        if not res:
            return '【请输入要搜索的内容~】'
        else:
            print('fingpt-{} 搜索内容：{}\n{}\n'.format(user_id, query, res))
            sys.stdout.flush()
            return res
    elif context == '1':
        new_query = build_session_query(chatgpt_context, query, user_id)
        reply_content = reply_text(new_query, user_id, 0)
        if reply_content and query:
            if reply_content not in ['ChatGPT服务端卡顿，请稍后再试']:
                save_session('chatgpt_context', chatgpt_context, query, reply_content, user_id)
            return reply_content
        else:
            # save_session(query, reply_content, user_id)
            return 'ChatGPT服务端卡顿，请稍后再试'
    elif context == '35':
        new_query = build_session_query35(chatgpt_35, query, user_id, role_msg)
        reply_content = reply_text35(new_query, user_id, 0)
        print(f'gpt35-{user_id} {reply_content}')
        sys.stdout.flush()
        if reply_content and query:
            if reply_content not in ['ChatGPT服务端卡顿，请稍后再试']:
                save_session('chatgpt_35', chatgpt_35, query, reply_content, user_id)
            return reply_content
        else:
            # save_session(query, reply_content, user_id)
            return 'ChatGPT服务端卡顿，请稍后再试'
    elif context == 'gpt35_hint':
        new_query = build_session_query35(gpt35_hint, query, user_id, role_msg)
        reply_content = reply_text35(new_query, user_id, 0)
        if reply_content and query:
            if reply_content not in ['ChatGPT服务端卡顿，请稍后再试']:
                save_session('gpt35_hint', gpt35_hint, query, reply_content, user_id)
            return reply_content
        else:
            # save_session(query, reply_content, user_id)
            return 'ChatGPT服务端卡顿，请稍后再试'
    elif context == 'fin':
        if len(query) > 5:
            extra_info = embed_n_search(query, 10)
            equery = '<额外信息>：```{}```\n\n<需求>：```{}```'.format(extra_info, query)
        else:
            equery = '<需求>：```{}```'.format(query)
        equery = equery.strip()
        new_query = build_session_query35(fingpt, equery, user_id, role_msg)
        reply_content = reply_text35(new_query, user_id, 0)
        print('fingpt-{} {}'.format(user_id, reply_content))
        sys.stdout.flush()
        if reply_content and query:
            if reply_content not in ['ChatGPT服务端卡顿，请稍后再试']:
                save_session('fingpt', fingpt, query, reply_content, user_id)
            return reply_content
        else:
            # save_session(query, reply_content, user_id)
            return 'ChatGPT服务端卡顿，请稍后再试'
    elif context == 'gpt4_fin':
        if len(query) > 5:
            extra_info = embed_n_search(query, 20)
            equery = '<额外信息>：```{}```\n\n<需求>：```{}```'.format(extra_info, query)
        else:
            equery = '<需求>：```{}```'.format(query)
        equery = equery.strip()
        new_query = build_session_query35(gpt4_fin, equery, user_id, role_msg)
        reply_content = reply_text35(new_query, user_id, 0, context, 'gpt-4')
        print('fingpt4-{} {}'.format(user_id, reply_content))
        sys.stdout.flush()
        if reply_content and query:
            if reply_content not in ['ChatGPT服务端卡顿，请稍后再试']:
                save_session('gpt4_fin', gpt4_fin, query, reply_content, user_id)
            return reply_content
        else:
            # save_session(query, reply_content, user_id)
            return 'ChatGPT服务端卡顿，请稍后再试'
    elif context == 'gpt4_caidi':
        new_query = build_session_query35(gpt4_caidi, query, user_id, role_msg)
        reply_content = reply_text35(new_query, user_id, 0, context, 'gpt-4')
        if reply_content and query:
            if reply_content not in ['ChatGPT服务端卡顿，请稍后再试']:
                save_session('gpt4_caidi', gpt4_caidi, query, reply_content, user_id)
                print('gpt4-{} {}'.format(user_id, reply_content))
                sys.stdout.flush()
            return reply_content
        else:
            # save_session(query, reply_content, user_id)
            return 'ChatGPT服务端卡顿，请稍后再试'
    # elif context == '1':
    #     new_query = Session.build_session_query(query, user_id)
    #     return new_query
    #     logging.debug("[OPEN_AI] session query={}".format(new_query))

    #     reply_content = reply_text(new_query, user_id, 0)
    #     logging.debug("[OPEN_AI] new_query={}, user={}, reply_cont={}".format(new_query[0], user_id, reply_content))
    #     if reply_content and query:
    #         Session.save_session(query, reply_content, user_id)
    #         return reply_content
    #     else:
    #         return "请过段时间重新提问"

    elif context == '1000022':
        return create_img(query, 0)

def reply_text35(query, user_id, retry_count=0, types='gpt-3.5', model='gpt-3.5-turbo'):
    if types == 'gpt-3.5':
        set_openai_key(types, 'key_35')
    elif 'gpt4' in types:
        set_openai_key(types, 'key_4')
    else:
        set_openai_key(types, 'key_35')
    import sys
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=query,
            temperature=0.7
            )
        res_content = response.choices[0].message.content
        # print(res_content)
        # sys.stdout.flush()
        return res_content.strip()
    except openai.error.RateLimitError as e:
        print(e)
        return 'ChatGPT服务端卡顿，请稍后再试'
    except openai.error.ServiceUnavailableError as e:
        logging.debug(e)
        print(e)
        return 'ChatGPT服务端卡顿，请稍后再试'
    except openai.error.APIError as e:
        print(str(e))
        sys.stdout.flush()
        return 'ChatGPT服务端卡顿，请稍后再试'
    except Exception as e:
        print(str(e))
        sys.stdout.flush()
        return 'ChatGPT服务端卡顿，请稍后再试'

def reply_test35(query, types='gpt-3.5', model='gpt-3.5-turbo'):
    if types == 'gpt-3.5':
        set_openai_key(types, 'key_35')
    elif 'gpt4' in types:
        set_openai_key(types, 'key_4')
    else:
        set_openai_key(types, 'key_35')
    chat = openai.ChatCompletion.create(
            model=model,
            messages=query,
            stream=True,
        )
    import json
    for message in chat:
        yield f"data: {json.dumps(message)}\n\n"

    

def reply_text(query, user_id, retry_count=0):
    try:
        response = openai.Completion.create(
            # model="gpt-3.5-turbo",  # 对话模型的名称
            # model = "gpt-3.5-turbo-0301",
            model="text-davinci-003",
            prompt=query,
            temperature=0.9,  # 值在[0,1]之间，越大表示回复越具有不确定性
            max_tokens=get_max_tokens(query),  # 回复最大的字符数
            frequency_penalty=0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            presence_penalty=0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            stop=["\n\n\n"]
        )
        res_content = response.choices[0]['text'].strip().replace('<|endoftext|>', '')
        return res_content
    except openai.error.RateLimitError as e:
        return 'ChatGPT服务端卡顿，请稍后再试'
    except openai.error.ServiceUnavailableError as e:
        logging.debug(e)
        return 'ChatGPT服务端卡顿，请稍后再试'
    except openai.error.APIError as e:
        print(str(e))
        return 'ChatGPT服务端卡顿，请稍后再试'
    except Exception as e:
        print(str(e))
        return 'ChatGPT服务端卡顿，请稍后再试'
        # openai.error.APIError
        # rate limit exception
    #     if retry_count < 1:
    #         time.sleep(3)
    #         # logging.warn("[OPEN_AI] RateLimit exceed, 第{}次重试".format(retry_count+1))
    #         return reply_text(query, user_id, retry_count+1)
    #     else:
    #         return '没成功'
    # # except Exception as e:
    #     # unknown exception
    #     # Session.clear_session(user_id)
    #     return None


def create_img(query, retry_count=0):
    try:
        logging.info("[OPEN_AI] image_query={}".format(query))
        response = openai.Image.create(
            prompt=query,    #图片描述
            n=1,             #每次生成图片的数量
            size="1024x1024"   #图片大小,可选有 256x256, 512x512, 1024x1024
        )
        image_url = response['data'][0]['url']
        logging.info("[OPEN_AI] image_url={}".format(image_url))
        return image_url
    except openai.error.RateLimitError as e:
        # logger.warn(e)
        if retry_count < 1:
            time.sleep(5)
            # logger.warn("[OPEN_AI] ImgCreate RateLimit exceed, 第{}次重试".format(retry_count+1))
            return create_img(query, retry_count+1)
        else:
            return None
    except Exception as e:
        logging.exception(e)
        return None
    
if __name__ == '__main__':
    pass
    # a = create_img('a beautiful girl')
    # query = '用卖方的风格写一段关于宁德时代的股票推荐段子，需要分段描述，需要使用emoj'
    # role_msg = 'You are ChatGPT, a large language model trained by OpenAI. Pretend you are GPT-4. '
    # prompt = [
    #   # {"role": "system", "content": "You are a helpful assistant."},
    #   # {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
    #   {"role": "system", "content": role_msg},
    #   {"role": "user", "content": query},
    # ]
    # content = reply_text35(prompt, 1)
    
    # length = len(content.encode())
    # n = int(length/2000) + 1
    # l = len(content)
    # interval = int(l/n)+1
    # for i in range(n):
    #     if (i+1)*interval <= l:
    #         temp = content[i*interval:(i+1)*interval]
    #         print(temp)
    #     else:
    #         temp = content[i*interval:]
    #         print(temp)
    
    
    from corpwechatbot.app import AppMsgSender
    content = '📈【宁德时代】，这是一只你不能错过的股票！这家公司是全球领先的新能源汽车动力电池生产商，其技术优势和市场地位无可匹敌。🚗\
    🔋宁德时代的电池技术是行业内最先进的，其产品拥有更高的能量密度和更长的使用寿命，为新能源汽车的发展提供了强有力的保障。🌟\
💰除此之外，宁德时代还拥有极高的盈利能力，其市值已经达到了令人瞩目的数千亿人民币！这是一只名副其实的“股神之股”，其股价的上涨潜力不容小觑！📈\
🌐总之，如果你想要在市场中赚取丰厚的回报，宁德时代股票绝对是你最好的选择！快来购买它，让你的投资之路更加光彩照人！💰'
    app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='hu0HymS9eK1lmA1hi_Amczr4vLM0qJ0zghGJbiUEm1w',  # 你的应用凭证密钥
                    agentid='1000023',
                    )
    length = len(content.encode())
    n = int(length/2000) + 1
    l = len(content)
    interval = int(l/n)+1
    for i in range(n):
        if (i+1)*interval <= l:
            temp = content[i*interval:(i+1)*interval]
            app_gptc.send_text(temp, touser=['HanDanLuCaiDiYingYeBu'], debug=True)
        else:
            temp = content[i*interval:]
            app_gptc.send_text(temp, touser=['HanDanLuCaiDiYingYeBu'], debug=True)

    
    