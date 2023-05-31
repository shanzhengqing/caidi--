# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:36:02 2023

@author: shanz
"""

import openai
import tiktoken
import re

openai.api_key = '#'
openai.organization = '#'

ENCODER = tiktoken.get_encoding("cl100k_base")
# ENCODER = tiktoken.get_encoding("gpt2")

def get_max_tokens(prompt: str) -> int:
    """
    Get the max tokens for a prompt
    """
    return 4096 - len(ENCODER.encode(prompt, allowed_special={'<|endoftext|>',}))

def text_gpt_35(system_p, content):
    try:
        completion = openai.ChatCompletion.create(
                                              model="gpt-3.5-turbo",
                                              messages=[
                                                {"role": "system", "content": system_p},
                                                {"role": "user", "content": content},
                                              ]
                                            )
        response = completion.choices[0].message.content
        return response.strip()
    except openai.error.RateLimitError as e:
        print(e)
        return '服务端卡顿'
    except openai.error.ServiceUnavailableError as e:
        print(e)
        return '服务端卡顿'
    except openai.error.APIError as e:
        print(str(e))
        return '服务端卡顿'
    except Exception as e:
        print(str(e))
        return '服务端卡顿'
    
def save_codes(response, savename, route):
    cmap = {'python':'py', 'javascript':'js', 'shell':'sh'}
    pattern = re.compile(r"```(.*?)```", re.DOTALL)
    r_all = re.findall(pattern, response)
    if not r_all:
        return ['代码生成失败，请将要求具体化']
    pattern1 = re.compile(r'^(.+?)\n')
    ctype = re.findall(pattern1, r_all[0])
    if ctype:
        ctypel = ctype[0].lower()  
    
    response = response.replace('```', '')
    for code in r_all:
        response = response.replace(code, '')
    descs = response.strip().splitlines()
    descs = [x for x in descs if x != '']
    if not ctype:
        ctype = re.findall(r'[a-zA-Z]+', descs[0])
        if ctype:
            ctypel = ctype[0].lower()
        else:
            return ['代码生成失败，请将要求具体化']
    else:
        r_all[0] = r_all[0].replace(ctype[0], '').strip()
    
    endn = cmap.get(ctypel, ctypel)
    nlist = []
    for i, code in enumerate(r_all):
        with open('{}/{}{}.{}'.format(route, savename, i, endn), 'w') as f:
            f.write(code)
            nlist.append('{}/{}{}.{}'.format(route, savename, i, endn))
    if len(descs) > 1:
        desc = '\n\n'.join(descs[1:])
        with open('{}/代码说明_{}.txt'.format(route, savename), 'w') as f:
            f.write(desc)
            nlist.append('{}/代码说明_{}.txt'.format(route, savename))
        # for i, desc in enumerate(descs[1:]):
        #     with open('{}/代码说明_{}{}.txt'.format(route, savename, i), 'w') as f:
        #         f.write(desc)
        #         nlist.append('{}/代码说明_{}{}.txt'.format(route, savename, i))
    return nlist

def main_code_logic(require, ):
    import sys
    fmt = '<代码>\n<代码的语言>\n<代码的逻辑>'
    system_p = '你是一个程序员，能根据给到的要求编写程序，你的代码中有规范的注释。输出的内容只有代码，不要解释，不需要介绍环境的配置过程，不要输出程序运行的结果，但要说明代码的逻辑。请严格按照下面格式给到结果：{}'.format(fmt)
    response = text_gpt_35(system_p, require)
    print('{},rsuccess'.format(require))
    sys.stdout.flush()
    
    fmt = '<缩写的内容>'
    system_p = '你是一个中国程序员，请将收到的代码需求缩写为不超过10个字，不要任何标点符号，不要打招呼，也不要解释。请严格按照下面格式给到结果：{}'.format(fmt)
    shortname = text_gpt_35(system_p, require)
    print('{},shsuccess'.format(require))
    sys.stdout.flush()
    
    nlist = save_codes(response, shortname, '/home/ubuntu/codes')
    return nlist

    
if __name__ == '__main__':
    pass
    # fmt = '<代码>\n<代码的语言>\n<代码的逻辑>'
    # system_p = '你是一个程序员，能根据给到的要求编写程序，你的代码中有规范的注释。输出的内容只有代码，不要解释，不需要介绍环境的配置过程，不要输出程序运行的结果，但要说明代码的逻辑。请严格按照下面格式给到结果：{}'.format(fmt)
    # test = text_gpt_35(system_p, 'java简单的后端框架')
    # with open('test.py', 'w') as f:
    #     f.write(test)
    
    with open('test.txt', 'r') as f:
        text = f.read()
    desc = save_codes(text, 'test', '.')
    
    