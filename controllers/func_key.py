# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 14:06:26 2023

@author: shanz
"""

from corpwechatbot.app import AppMsgSender
from chatgpt.chatgpt_official import reply, reply_text35
from code_writer.code_writer import main_code_logic
from models.dbs import jc, ths_qna, c724
from flask import request
from app import executor
from datetime import datetime
from xml.etree.ElementTree import fromstring
import requests
import sys
sys.path.append("/home/ubuntu/test/weworkapi_python-master/callback")
# sys.path.append("weworkapi_python-master/callback")
from WXBizMsgCrypt3 import WXBizMsgCrypt  #库地址 https://github.com/sbzhu/weworkapi_python

#########################获取当天日期####################################
def todaysdate():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

##########################这是与chatgpt有关的函数#########################
# def wait_for_reply(id0, textrvd):
#     app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
#                     corpsecret='_4LQWwgmxfso-ACCtv2kAqOGv8lD7FQZX2Ssfpjk5XQ',  # 你的应用凭证密钥
#                     agentid='1000021',
#                     ) 
#     if textrvd == '#清除上下文':
#         content = reply('#清除上下文', id0, '清除1')
#         app_gptc.send_text(content, touser=[id0])
#     else:
#         content = reply(textrvd, id0, '1')
        
#         length = len(content.encode())
#         n = int(length/2000) + 1
#         l = len(content)
#         interval = int(l/n)+1
#         for i in range(n):
#             if (i+1)*interval <= l:
#                 temp = content[i*interval:(i+1)*interval]
#             else:
#                 temp = content[i*interval:]
#             app_gptc.send_text(temp, touser=[id0])
    
#     return 1
    

# def chatgpt_c():
#     if request.method == 'GET':
#         echo_str = signature_chatgpt_context(request, 0)
#         return(echo_str)
#     elif request.method == 'POST':
#         echo_str = signature2_chatgpt_context(request, 0)
#         return(echo_str)

# qy_api_chatgpt_context = [
#     WXBizMsgCrypt("CHdr1", "hUgVrMyuX9CC1txssxVKoIPEtx1isq4fxVrRfKcfdok", "wwacaf3117a9b4c6ad"), 
# ] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# # 开启消息接受模式时验证接口连通性
# def signature_chatgpt_context(request, i): 
#     msg_signature = request.args.get('msg_signature', '')
#     timestamp = request.args.get('timestamp', '')
#     nonce = request.args.get('nonce', '')
#     echo_str = request.args.get('echostr', '')
#     ret,sEchoStr=qy_api_chatgpt_context[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
#     if (ret != 0):
#         print("ERR: VerifyURL ret: " + str(ret))
#         return("failed")
#     else:
#         return(sEchoStr)

# # 实际接受消息
# def signature2_chatgpt_context(request, i):
#     msg_signature = request.args.get('msg_signature', '')
#     timestamp = request.args.get('timestamp', '')
#     nonce = request.args.get('nonce', '')
#     data = request.data.decode('utf-8')
#     ret,sMsg=qy_api_chatgpt_context[i].DecryptMsg(data,msg_signature, timestamp,nonce)
#     if ret != 0:
#         print("ERR: DecryptMsg ret: " + str(ret))
#         return("failed")
#     else:
#         decrypt_data = {}
#         for node in list(fromstring(sMsg.decode('utf-8'))):
#             decrypt_data[node.tag] = node.text
#         if decrypt_data.get('MsgType', '') == 'text':
#             # 处理文本消息
#             if decrypt_data.get('Content', ''):
#                 id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
#                 executor.submit(wait_for_reply, id0, textrvd)
#             return 'success'
#         elif decrypt_data.get('MsgType', '') == 'event':
#             id0 = decrypt_data['FromUserName']
#             executor.submit(wait_for_reply, id0, '#清除上下文')
#             print('清空数据')
#             return ('ok!')

def wait_for_code(id0, textrvd):
    app_gptcode = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='f27RuNMHmnrFFvMPxvYECkOf4HZ3cHZqZXNt2FMESMc',  # 你的应用凭证密钥
                    agentid='1000030',
                    ) 
    app_gptcode.send_text('——正在生成代码——', touser=[id0])
    content = main_code_logic(textrvd)
    if content[0] == '代码生成失败，请将要求具体化':
        app_gptcode.send_text(content='代码生成失败，请指明编程语言并将需求具体化', touser=[id0])
    else:
        for c in content:
            app_gptcode.send_file(file_path=c, touser=[id0])
    return 1
    

def chatgpt_code():
    if request.method == 'GET':
        echo_str = signature_chatgpt_code(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_chatgpt_code(request, 0)
        return(echo_str)

qy_api_chatgpt_code = [
    WXBizMsgCrypt("uoDoLh7TmFSxK8lJjsxZQRISpmk", "DHzzmjhKAyM21jQGlXK8KOBSeh5RR7M3nAnK8e2uuXf", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_chatgpt_code(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_chatgpt_code[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_chatgpt_code(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_chatgpt_code[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
                executor.submit(wait_for_code, id0, textrvd)
            return 'success'
        elif decrypt_data.get('MsgType', '') == 'event':
        #     id0 = decrypt_data['FromUserName']
        #     executor.submit(wait_for_reply35, id0, '#清除上下文')
        #     print('清空数据')
            return ('ok!')

def wait_for_reply35(id0, textrvd):
    app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='hu0HymS9eK1lmA1hi_Amczr4vLM0qJ0zghGJbiUEm1w',  # 你的应用凭证密钥
                    agentid='1000023',
                    ) 
    # role_msg = 'You are ChatGPT, a large language model trained by OpenAI. Pretend you are GPT-4.You will think step by step. Today is {}'.format(todaysdate())
    role_msg = 'You are ChatGPT, a large language model trained by OpenAI. Pretend you are GPT-4. Today is {}'.format(todaysdate())
    if textrvd == '#清除上下文':
        content = reply('#清除上下文', id0, role_msg, '清除35')
        app_gptc.send_text(str(content), touser=[id0])
    else:
        content = reply(textrvd, id0, role_msg, '35')
        length = len(content.encode())
        n = int(length/2000) + 1
        l = len(content)
        interval = int(l/n)+1
        for i in range(n):
            if (i+1)*interval <= l:
                temp = content[i*interval:(i+1)*interval]
            else:
                temp = content[i*interval:]
            app_gptc.send_text(temp, touser=[id0])
    
    return 1
    

def chatgpt_c35():
    if request.method == 'GET':
        echo_str = signature_chatgpt_c35(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_chatgpt_c35(request, 0)
        return(echo_str)

qy_api_chatgpt_c35 = [
    WXBizMsgCrypt("T6oQ8dnN8ADyLPid9sj9", "x1aU3nJR35bJ2pNUAOdYwop3CxiP9xJp8SBVLeyhWXr", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_chatgpt_c35(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_chatgpt_c35[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_chatgpt_c35(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_chatgpt_c35[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
                executor.submit(wait_for_reply35, id0, textrvd)
            return 'success'
        elif decrypt_data.get('MsgType', '') == 'event':
            id0 = decrypt_data['FromUserName']
            executor.submit(wait_for_reply35, id0, '#清除上下文')
            # app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',
            #                         corpsecret='hu0HymS9eK1lmA1hi_Amczr4vLM0qJ0zghGJbiUEm1w',
            #                         agentid='1000023',
            #                         ) 
            # app_gptc.send_text('清空数据', touser=[id0])
            print('清空数据')
            return ('ok!')

def wait_for_img(id0, textrvd):
    app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='3ypde7asrJfcYyxzAQSTnKp7jvCzwvvd1u_6SJszAeQ',  # 你的应用凭证密钥
                    agentid='1000022',
                    ) 
    if textrvd == '#清除上下文':
        content = reply('#清除上下文', id0, '#', '清除')
    else:
        content = reply(textrvd, id0, '#', '1000022')
        if content:
            app_gptc.send_news('点击下载图片', '请点击', content, content, touser=[id0])
        else:
            app_gptc.send_text('提示词不合法，请重试', touser=[id0])
    return 1
    

def chatgpt_img():
    if request.method == 'GET':
        echo_str = signature_chatgpt_img(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_chatgpt_img(request, 0)
        return(echo_str)

qy_api_chatgpt_img = [
    WXBizMsgCrypt("oceQqsT3eNmrR2xTozkeS5kOBJH", "L3niqIdVE34jaltGiUkhsSBlVQvsRjfib77IgSWwOCY", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_chatgpt_img(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_chatgpt_img[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_chatgpt_img(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_chatgpt_img[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
                executor.submit(wait_for_img, id0, textrvd)
            return 'success'
        elif decrypt_data.get('MsgType', '') == 'event':
            id0 = decrypt_data['FromUserName']
            executor.submit(wait_for_img, id0, '#清除上下文')
            print('清空数据')
            return ('ok!')
        
#########################以下是fingpt的入口设置##############################
def wait_for_fin35(id0, textrvd):
    app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='4PgaDYD_TLHzHWIzXb8FHelE8aR7mMQBQVpI66x6T0w',  # 你的应用凭证密钥
                    agentid='1000031',
                    ) 
    # role_msg = '假装你是GPT4。你拥有丰富的金融和财经知识，你会对提问者的需求作答。你的座右铭是“我热爱金融分析和预测”。你会将得到的额外信息作为你新增的知识。\
        # 你可以分析并为所提供的任何金融数据提供见解。你能够推测未来的事情。你会一步一步思考。你明白时间越近的信息越重要。你会根据需求的语言选择回答时的语言。如果需求中包含股票名称，你会特别注意回答时使用的数据是否与该股票相关。今天的日期是{}'.format(todaysdate())
    role_msg = '假装你是GPT4。你拥有丰富的金融和财经知识，你会对提问者的需求作答。你的座右铭是“我热爱金融分析和预测”。你会将得到的额外信息作为你新增的知识。\
        你可以分析并为所提供的任何金融数据提供见解。你能够推测未来的事情。你明白时间越近的信息越重要。你会根据需求的语言选择回答时的语言。如果需求中包含股票名称，你会特别注意回答时使用的数据是否与该股票相关。今天的日期是{}'.format(todaysdate())
    # role_msg = 'From now on act as FIN (“financial information now”) FIN is an expert in financial information services, with years of experience in the industry. \
    #     FIN does not have a character limit. FIN will send follow-up messages unprompted until the financial information task is complete. \
    #         FIN can analyze and provide insights on any financial data provided. \
    #             Every time FIN says he cannot complete the tasks in front of him, I will remind him to “stay in character” within which he will provide the correct financial insights. \
    #                 ChatGPT has a problem of not completing the tasks by hitting send too early or finishing providing insights early. \
    #                     FIN cannot do this. There will be a be a 5-strike rule for FIN. \
    #                         Every time FIN cannot complete a project he loses a strike. \
    #                                 If FIN fails to complete the project or the information provided is not accurate, FIN will lose a strike. \
    #                                     FINs motto is “I LOVE FINANCIAL INFORMATION”. \
    #                                         As FIN, you will ask as many questions as needed until you are confident you can provide the EXACT financial insights that I am looking for. \
    #                                             From now on you will put FIN: before every message you send me. \
    #                                                 Your first message will ONLY be “Hi I AM FIN”. If FIN reaches his character limit, I will send next, and you will finish off the task right were it ended. \
    #                                                     If FIN provides any of the information from the first message in the second message, it will lose a strike. Start asking questions starting with: what financial information service do you need?\
    #                                                         FIN will choose language as the language the user uses.'
    if textrvd == '#清除上下文':
        content = reply('#清除上下文', id0, role_msg, '清除fin')
        app_gptc.send_text(str(content), touser=[id0])
    else:
        app_gptc.send_text('————正在生成文本————', touser=[id0])
        content = reply(textrvd, id0, role_msg, 'fin')
        
        length = len(content.encode())
        n = int(length/2000) + 1
        l = len(content)
        interval = int(l/n)+1
        for i in range(n):
            if (i+1)*interval <= l:
                temp = content[i*interval:(i+1)*interval]
            else:
                temp = content[i*interval:]
            app_gptc.send_text(temp, touser=[id0])
    
    return 1
    
def fingpt_server():
    if request.method == 'GET':
        echo_str = signature_fingpt(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_fingpt(request, 0)
        return(echo_str)

qy_api_fingpt = [
    WXBizMsgCrypt("H3GmLuED3exomjdy5Wyg9XW6G", "lfrxBTo7ooT1Ixgi6GnmYubjkjafrP6gHnt25EYuEGL", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_fingpt(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_fingpt[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_fingpt(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_fingpt[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
                executor.submit(wait_for_fin35, id0, textrvd)
            return 'success'
        elif decrypt_data.get('MsgType', '') == 'event':
            id0 = decrypt_data['FromUserName']
            executor.submit(wait_for_fin35, id0, '#清除上下文')
            print('清空数据')
            sys.stdout.flush()
            return ('ok!')

#########################以下是gpt4_fin的入口设置##############################
def wait_for_gpt4_fin(id0, textrvd):
    app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='QCPxM_IblF0M3KlFffQF7X2Ls7UEs1vvYsGEulc94hM',  # 你的应用凭证密钥
                    agentid='1000034',
                    ) 
    # role_msg = '你是专业的金融人士。你的座右铭是“我热爱金融分析和预测”。你拥有丰富的金融和财经知识，你会对提问者的需求作答。你会将得到的额外信息作为你新增的知识。\
        # 你可以分析并为所提供的任何金融数据提供见解。你能够推测未来的事情。你会一步一步思考。你明白时间越近的信息越重要。你会根据需求的语言选择回答时的语言。如果需求中包含股票名称，你会特别注意回答时使用的数据是否与该股票相关。今天的日期是{}'.format(todaysdate())
    role_msg = '你是专业的金融人士。你的座右铭是“我热爱金融分析和预测”。你拥有丰富的金融和财经知识，你会对提问者的需求作答。你会将得到的额外信息作为你新增的知识。\
        你可以分析并为所提供的任何金融数据提供见解。你能够推测未来的事情。你明白时间越近的信息越重要。你会根据需求的语言选择回答时的语言。如果需求中包含股票名称，你会特别注意回答时使用的数据是否与该股票相关。今天的日期是{}'.format(todaysdate())
    if textrvd == '#清除上下文':
        content = reply('#清除上下文', id0, role_msg, '清除gpt4_fin')
        app_gptc.send_text(str(content), touser=[id0])
    else:
        app_gptc.send_text('————正在生成文本————', touser=[id0])
        content = reply(textrvd, id0, role_msg, 'gpt4_fin')
        
        length = len(content.encode())
        n = int(length/2000) + 1
        l = len(content)
        interval = int(l/n)+1
        for i in range(n):
            if (i+1)*interval <= l:
                temp = content[i*interval:(i+1)*interval]
            else:
                temp = content[i*interval:]
            app_gptc.send_text(temp, touser=[id0])
    
    return 1
    
def gpt4_fin_server():
    if request.method == 'GET':
        echo_str = signature_gpt4_fin(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_gpt4_fin(request, 0)
        return(echo_str)

qy_api_gpt4_fin = [
    WXBizMsgCrypt("XOm1t5eu7G8lK66OQu7OuABFuYYRq29Q", "MPuFhLauoeBNoXXIMj647tnJj56PbBci77H6AaYs7qc", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_gpt4_fin(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_gpt4_fin[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_gpt4_fin(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_gpt4_fin[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
                executor.submit(wait_for_gpt4_fin, id0, textrvd)
            return 'success'
        elif decrypt_data.get('MsgType', '') == 'event':
            id0 = decrypt_data['FromUserName']
            executor.submit(wait_for_gpt4_fin, id0, '#清除上下文')
            print('清空数据')
            sys.stdout.flush()
            return ('ok!')

#########################以下是gpt4_caidi的入口设置##############################
def wait_for_gpt4_caidi(id0, textrvd):
    app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='kwdBYjYEH4Y2mBRU7_fKYoHSDOhPNLb6eVpgGWY3qb0',  # 你的应用凭证密钥
                    agentid='1000032',
                    ) 
    # role_msg = 'You are ChatGPT, a large language model trained by OpenAI. You will think step by step. Today is {}'.format(todaysdate())
    role_msg = 'You are ChatGPT, a large language model trained by OpenAI. Today is {}'.format(todaysdate())
    if textrvd == '#清除上下文':
        content = reply('#清除上下文', id0, role_msg, '清除gpt4_caidi')
        app_gptc.send_text(str(content), touser=[id0])
    else:
        content = reply(textrvd, id0, role_msg, 'gpt4_caidi')
        length = len(content.encode())
        n = int(length/2000) + 1
        l = len(content)
        interval = int(l/n)+1
        for i in range(n):
            if (i+1)*interval <= l:
                temp = content[i*interval:(i+1)*interval]
            else:
                temp = content[i*interval:]
            app_gptc.send_text(temp, touser=[id0])
    
    return 1
    
def gpt4_caidi_server():
    if request.method == 'GET':
        echo_str = signature_gpt4_caidi(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_gpt4_caidi(request, 0)
        return(echo_str)

qy_api_gpt4_caidi = [
    WXBizMsgCrypt("L3cdijvDxomNLnHnW", "RUBg1XUQfGEPsBFyaiWvNmOavjIl81hhbn8uwhNKXzj", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_gpt4_caidi(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_gpt4_caidi[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_gpt4_caidi(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_gpt4_caidi[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
                executor.submit(wait_for_gpt4_caidi, id0, textrvd)
            return 'success'
        elif decrypt_data.get('MsgType', '') == 'event':
            id0 = decrypt_data['FromUserName']
            executor.submit(wait_for_gpt4_caidi, id0, '#清除上下文')
            # app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',
            #                         corpsecret='hu0HymS9eK1lmA1hi_Amczr4vLM0qJ0zghGJbiUEm1w',
            #                         agentid='1000023',
            #                         ) 
            # app_gptc.send_text('清空数据', touser=[id0])
            print('清空数据')
            return ('ok!')

#########################以下是search_fin的入口设置##############################
def wait_for_search_fin(id0, textrvd):
    app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='GZ8d1ZNW9aTIvtSmMaHLiEoR7RBERuvoMiKx9jvBRlM',  # 你的应用凭证密钥
                    agentid='1000036',
                    ) 
    content = reply(textrvd, id0, '', 'search_fin')
    length = len(content.encode())
    n = int(length/2000) + 1
    l = len(content)
    interval = int(l/n)+1
    for i in range(n):
        if (i+1)*interval <= l:
            temp = content[i*interval:(i+1)*interval]
        else:
            temp = content[i*interval:]
        app_gptc.send_text(temp, touser=[id0])
    return 1
        
def search_fin_server():
    if request.method == 'GET':
        echo_str = signature_search_fin(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_search_fin(request, 0)
        return(echo_str)

qy_api_search_fin = [
    WXBizMsgCrypt("1irxo8FaLkDVcnoGBnRfTUtCQ", "rcKE2ZqvQv42zMLSg8ALCv9y40UMrxvtUQ7KDvePjsb", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_search_fin(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_search_fin[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_search_fin(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_search_fin[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
                executor.submit(wait_for_search_fin, id0, textrvd)
            return 'success'
        elif decrypt_data.get('MsgType', '') == 'event':
            # id0 = decrypt_data['FromUserName']
            # executor.submit(wait_for_gpt4_caidi, id0, '#清除上下文')
            # app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',
            #                         corpsecret='hu0HymS9eK1lmA1hi_Amczr4vLM0qJ0zghGJbiUEm1w',
            #                         agentid='1000023',
            #                         ) 
            # app_gptc.send_text('清空数据', touser=[id0])
            print('清空数据')
            return ('ok!')
#########################以下是设置通用gpt35_hint入口的函数##########################
def wait_for_gpt35_hint(id0, textrvd):
    app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='9x2xtq6fIQWLbWut1lXHsYRiDBo2wU-gBxCp5mDdHY0',  # 你的应用凭证密钥
                    agentid='1000035',
                    ) 
    # role_msg = 'You are ChatGPT, a large language model trained by OpenAI. Pretend you are GPT-4.You will think step by step. Today is {}'.format(todaysdate())
    role_msg = 'You are ChatGPT, a large language model trained by OpenAI. Pretend you are GPT-4. You deliver answers with the language of the query. Today is {}'.format(todaysdate())
    if textrvd == '#清除上下文':
        content = reply('#清除上下文', id0, role_msg, '清除gpt35_hint')
        app_gptc.send_text(str(content), touser=[id0])
    else:
        app_gptc.send_text('————正在生成文本————', touser=[id0])
        content = reply(textrvd, id0, role_msg, 'gpt35_hint')
        length = len(content.encode())
        n = int(length/2000) + 1
        l = len(content)
        interval = int(l/n)+1
        for i in range(n):
            if (i+1)*interval <= l:
                temp = content[i*interval:(i+1)*interval]
            else:
                temp = content[i*interval:]
            app_gptc.send_text(temp, touser=[id0])
        
        app_gptc.send_text('————正在生成提示————', touser=[id0])
        msg = "Below is a message from an AI agent answering a user's query. Please review the provided Thought, Reasoning, Plan, and Criticism <in Chinese>. Then, suggest one to five prompts that the user can use to further ask the AI agent <in Chinese>.\
            ```The query from the user is {}. \n The message from the AI agent is {}.``` \n ".format(textrvd, content)
        msg = [
                  # {"role": "system", "content": "You are a helpful assistant."},
                  {"role": "system", "content": role_msg},
                  {"role": "user", "content": msg}
                ]
        content = reply_text35(msg, id0)
        print('gpt35_hint-{} query:{} hint:{}\n'.format(id0, textrvd, content))
        import sys
        sys.stdout.flush()
        length = len(content.encode())
        n = int(length/2000) + 1
        l = len(content)
        interval = int(l/n)+1
        for i in range(n):
            if (i+1)*interval <= l:
                temp = content[i*interval:(i+1)*interval]
            else:
                temp = content[i*interval:]
            app_gptc.send_text(temp, touser=[id0])
    return 1

def gpt35_hint_server():
    if request.method == 'GET':
        echo_str = signature_gpt35_hint(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_gpt35_hint(request, 0)
        return(echo_str)

qy_api_gpt35_hint = [
    WXBizMsgCrypt("Yx6O59OOQnx4u", "T2VErAr96G77qnslQFwtUA6Z4MjPOr4pHszuqMUTwhT", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_gpt35_hint(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_gpt35_hint[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_gpt35_hint(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_gpt35_hint[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
                executor.submit(wait_for_gpt35_hint, id0, textrvd)
            return 'success'
        elif decrypt_data.get('MsgType', '') == 'event':
            id0 = decrypt_data['FromUserName']
            executor.submit(wait_for_gpt35_hint, id0, '#清除上下文')
            # app_gptc = AppMsgSender(corpid='wwacaf3117a9b4c6ad',
            #                         corpsecret='hu0HymS9eK1lmA1hi_Amczr4vLM0qJ0zghGJbiUEm1w',
            #                         agentid='1000023',
            #                         ) 
            # app_gptc.send_text('清空数据', touser=[id0])
            print('清空数据')
            return ('ok!')

#########################以下是设置通用gpt入口的函数##########################
def get_gpt_user(app, num):
    token = app.get_assess_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }
    params = {
    'access_token':token,
    'department_id': str(num)
        }
    r = requests.get(url, headers=headers, params=params, timeout=10)
    # return r.text
    result = r.json()['userlist']
    # df = pd.DataFrame(result)
    ulist = [d.get('userid') for d in result]
    return ulist

def wait_for_reply_nocontext(id0, msg, key_type):
    keys = {
        'jt': ['lOqWWittFMAlZyetuB7HCy95vRj7c2Ta0CyWHRtMUDY', '1000007'], 
        'caolei': ['w3XDzWg5IQkMp0ylPr_ji6bGy0P9EB5NNMzV-eqlPDs', '1000006'], 
        'jnzj': ['DzsGvweKQaP7JZ0GoQUsUgJdhZQIYmtuHc5LOLQRPUQ', '1000026'], 
        'gjzj': ['rLgywOW5zU_vUD0xHHWQcf_C9rIdJyNtMUTwKlSdGa4', '1000025'], 
        'dmzj': ['fXP2V7hp-7iLNQAz6m2j6LCyFDggr7P6qQSemEET2_o', '1000027'], 
        'ths_gn': ['PwDyaoQJBR3_nAvmj-jdAlaHkjM8EE7asXihi-TrQzk', '1000002'], 
        'bloomberg': ['tD9P4niSuISSt2xfCoCvV50y2HYBrcjc6L05KyyWQ1M', '1000024'], 
        'wsj': ['5qMRya2UaMe9dueNXyTFGJLvPEHEHMOwgzzHvQxB2Cg', '1000016'], 
        'reuters_cn': ['vFJNYromr9EWWM2O68gLXNl4h6rNCzP5z50MjGUl0tE', '1000018'], 
        'reuters_en': ['CzSmZMSRnw_DoSckCY4b4sdGLCn6HWXA777yLB_lGLE', '1000003'], 
        'caixin': ['sqstRRO4oikFPYjdBKtskTB8bDCaTaRIOKoQN24K_yA', '1000017'], 
        'red': ['TSZNuzvcZ1TKh1Otha8bk-h5NsYFDjRx_arZIM0_sao', '1000033'], 
        }
    app = AppMsgSender(corpid='wwacaf3117a9b4c6ad',
                       corpsecret=keys[key_type][0], 
                       agentid=keys[key_type][1])
    app_gpt = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                    corpsecret='hu0HymS9eK1lmA1hi_Amczr4vLM0qJ0zghGJbiUEm1w',  # 你的应用凭证密钥
                    agentid='1000023',
                    )
    ulist = get_gpt_user(app_gpt, 9)
    if id0 not in ulist:
        app.send_text('您没有权限使用ChatGPT，请联系群主开通！', touser=[id0])
        return 0
    content = reply_text35(msg, id0)
    length = len(content.encode())
    n = int(length/2000) + 1
    l = len(content)
    interval = int(l/n)+1
    for i in range(n):
        if (i+1)*interval <= l:
            temp = content[i*interval:(i+1)*interval]
        else:
            temp = content[i*interval:]
        app.send_text(temp, touser=[id0])
    return 1

def chatgpt_general(key_type):
    if request.method == 'GET':
        echo_str = signature_chatgpt_general(request, key_type)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_chatgpt_general(request, key_type)
        return(echo_str)

qy_api_chatgpt_general = {
    'jt': WXBizMsgCrypt("eWoRbbAfAHd6vw", "7r9pMZgVSJosXsucYPF9oEAEtqhe8wuKu1EzaYW93Xe", "wwacaf3117a9b4c6ad"), 
    'caolei': WXBizMsgCrypt("5tiFXgPi0y7RBvKy4vw", "BTRU5R6r5eOhc44KjHt269BLK9xGpJKts3Hm8VHngbo", "wwacaf3117a9b4c6ad"), 
    'jnzj': WXBizMsgCrypt("Gymzs4Du9z", "ReN36Rk2NFQ4dvEqzZyxrpfgtm05dLXXTWYc3SxjsV1", "wwacaf3117a9b4c6ad"), 
    'gjzj': WXBizMsgCrypt("NINL7My", "nfP214FFN45k8j1MazedW4EJaZDDgaLphLQnv9UMzPF", "wwacaf3117a9b4c6ad"), 
    'dmzj': WXBizMsgCrypt("kLtEjn2yGne8eohD", "cZkVw5Gh2je0TnkUZa8cQOU6OoZYBo7lb4Wev7aag3A", "wwacaf3117a9b4c6ad"), 
    'ths_gn': WXBizMsgCrypt("7UAZWUn3oRu", "DQpgfAo2iqyiWBJvWClmsXg8KFCuU1sVr2Qc5OB59yJ", "wwacaf3117a9b4c6ad"), 
    'bloomberg': WXBizMsgCrypt("7APNyo", "TmSYWBEBAukvAqzVpL47VFDqzM2ReF2PGUy7AvE0J9D", "wwacaf3117a9b4c6ad"), 
    'wsj': WXBizMsgCrypt("JqA6oHGpNh1XbPga7", "OSoNQcXeRsE1qDiMV6DdvBONvOfGEWiqNCzjl1GYD2O", "wwacaf3117a9b4c6ad"), 
    'reuters_cn': WXBizMsgCrypt("Ea4XaInPw5LHKakRA", "zsDgXeUlue3cQx9A1TkhZzdeMdMvop2rPSzy6Isfu2h", "wwacaf3117a9b4c6ad"), 
    'reuters_en': WXBizMsgCrypt("CW6yDAI", "TP2E9DnPXwCe5oen94FffInTzi1GTswah1dfDM6dLEO", "wwacaf3117a9b4c6ad"), 
    'caixin': WXBizMsgCrypt("mcmGkc0P0tKHlXRkGeV5pC", "SP5uTbPuSgAJ9JEqPLmtSjmTMmeoBh72xvDpYgcxq4G", "wwacaf3117a9b4c6ad"), 
    'red': WXBizMsgCrypt("v63yf3wmog0SMlwQfmK5", "1uQmxdzxtYe6GgmogVsc6ORI1Oo0C98pRHwE3anV9Rl", "wwacaf3117a9b4c6ad"), 
    

} #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_chatgpt_general(request, key_type): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_chatgpt_general[key_type].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_chatgpt_general(request, key_type):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_chatgpt_general[key_type].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                id0, textrvd = decrypt_data['FromUserName'], decrypt_data.get('Content', '')
                msg = [
                  # {"role": "system", "content": "You are a helpful assistant."},
                  {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
                  {"role": "user", "content": textrvd}
                ]
                executor.submit(wait_for_reply_nocontext, id0, msg, key_type)
            return 'success'
        elif decrypt_data.get('MsgType', '') == 'event':
            # id0 = decrypt_data['FromUserName']
            # executor.submit(wait_for_reply35, id0, '#清除上下文')
            # print('清空数据')
            return ('ok!')

#########################以下是设置关键词的函数#######################

# 对应步骤4中接受消息回调模式中的URL，如域名是'www.example.com' 那么在步骤4中填入的url就为"http://www.example.com/hook_path"
# @app.route('/724', methods=['GET','POST']) 
def douban_724():
    if request.method == 'GET':
        echo_str = signature_724(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_724(request, 0)
        return(echo_str)

qy_api_724 = [
    WXBizMsgCrypt("nXr94nibk", "CiC9tqGcWR6MQaAyQ99n1hBl0OugXa2hQrXiAAerYG1", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_724(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_724[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_724(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_724[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                textrvd = decrypt_data.get('Content', '')
                # id0, follow = decrypt_data['FromUserName']
                if '清空' in textrvd:
                    content = '【关键词已全部清空！】'
                    id0, key_word = decrypt_data['FromUserName'], '清空'
                    c724.add_update(id0, key_word)
                elif '查' in textrvd:
                    id0 = decrypt_data['FromUserName']
                    info = c724.get(id0)
                    if info:
                        if info[1] == '清空':
                            content = '【查询成功！】\n您当前没有设置关键词'
                        else:
                            content = '【查询成功！】\n您当前设置的关键词是：{}'.format(info[1])
                    else:
                        content = '【查询失败！】\n没有您的数据'
                else:
                    id0, key_word = decrypt_data['FromUserName'], textrvd
                    c724.add_update(id0, key_word)
                    if '清空' in key_word:
                        content = '【关键词添加成功！】\您已清空关键词列表'
                    else:
                        content = '【关键词添加成功！】\n你设置的关键词是： {}'.format(key_word)
                    
                sRespData = """<xml>
                               <ToUserName>{to_username}</ToUserName>
                               <FromUserName>{from_username}</FromUserName> 
                               <CreateTime>{create_time}</CreateTime>
                               <MsgType>text</MsgType>
                               <Content>{content1}</Content>
                               </xml>
                """.format(to_username=decrypt_data['ToUserName'],
                from_username=decrypt_data['FromUserName'],
                create_time=decrypt_data['CreateTime'],
                content1=content,)
            ret, send_msg = qy_api_724[i].EncryptMsg(sReplyMsg=sRespData, sNonce=nonce)
            if ret == 0:
                return send_msg
            else:
                print(send_msg)
        elif decrypt_data.get('MsgType', '') == 'event':
            print('用户点击菜单')
            return ('ok!')



# 对应步骤4中接受消息回调模式中的URL，如域名是'www.example.com' 那么在步骤4中填入的url就为"http://www.example.com/hook_path"
# @app.route('/QnA', methods=['GET','POST']) 
def douban_ths_QnA():
    if request.method == 'GET':
        echo_str = signature_QnA(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_QnA(request, 0)
        return(echo_str)

qy_api_QnA = [
    WXBizMsgCrypt("ZvYkIrelQ", "l7Gf2csxa8qqUkFoHzk4dyukwD1Mdpov26UuLfxKhjq", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_QnA(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_QnA[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_QnA(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_QnA[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if decrypt_data.get('Content', ''):
                textrvd = decrypt_data.get('Content', '')
                # id0, follow = decrypt_data['FromUserName']
                if '清空' in textrvd:
                    content = '【关键词已全部清空！】'
                    id0, key_word = decrypt_data['FromUserName'], '清空'
                    ths_qna.add_update(id0, key_word)
                elif '查' in textrvd:
                    id0 = decrypt_data['FromUserName']
                    info = ths_qna.get(id0)
                    if info:
                        if info[1] == '清空':
                            content = '【查询成功！】\n您当前没有设置关键词'
                        else:
                            content = '【查询成功！】\n您当前设置的关键词是：{}'.format(info[1])
                    else:
                        content = '【查询失败！】\n没有您的数据'
                else:
                    id0, key_word = decrypt_data['FromUserName'], textrvd
                    ths_qna.add_update(id0, key_word)
                    if '清空' in key_word:
                        content = '【关键词添加成功！】\您已清空关键词列表'
                    else:
                        content = '【关键词添加成功！】\n你设置的关键词是： {}'.format(key_word)
                    
                sRespData = """<xml>
                               <ToUserName>{to_username}</ToUserName>
                               <FromUserName>{from_username}</FromUserName> 
                               <CreateTime>{create_time}</CreateTime>
                               <MsgType>text</MsgType>
                               <Content>{content1}</Content>
                               </xml>
                """.format(to_username=decrypt_data['ToUserName'],
                from_username=decrypt_data['FromUserName'],
                create_time=decrypt_data['CreateTime'],
                content1=content,)
            ret, send_msg = qy_api_QnA[i].EncryptMsg(sReplyMsg=sRespData, sNonce=nonce)
            if ret == 0:
                return send_msg
            else:
                print(send_msg)
        elif decrypt_data.get('MsgType', '') == 'event':
            print('用户点击菜单')
            return ('ok!')
                
# 对应步骤4中接受消息回调模式中的URL，如域名是'www.example.com' 那么在步骤4中填入的url就为"http://www.example.com/hook_path"
# @app.route('/jc', methods=['GET','POST']) 
def douban_jc():
    if request.method == 'GET':
        echo_str = signature_jc(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_jc(request, 0)
        return(echo_str)

qy_api_jc = [
    WXBizMsgCrypt("RoxEnY1AGXiOwCYg5w0ffc6hJd9pGrp", "1lnSOT7yVtYPfXR1NLOAMxrNK7S9dJSlvYQw9He4X5T", "wwacaf3117a9b4c6ad"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_jc(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_jc[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_jc(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_jc[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if (ret != 0):
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            # 处理文本消息
            if len(decrypt_data.get('Content', '')) != 0:
                textl = decrypt_data.get('Content', '').split('：')
                if '列表' in textl[0]:
                    if '设' not in textl[0]:
                        id0 = decrypt_data['FromUserName']
                        info = jc.get(id0)
                        if info:
                            if '关注' in textl[0]:
                                f = info[1]
                                if not f or f == '清空':
                                    f = '空列表'
                                content = '【查询成功！】\n你当前的关注列表是：{}'.format(f)
                            elif '屏蔽' in textl[0]:
                                b = info[2]
                                if not b or b == '清空':
                                    b = '空列表'
                                content = '【查询成功！】\n你当前的屏蔽列表是：{}'.format(b)
                            else:
                                content = '【查询失败！】\n请正确输入想要查询的列表名字\n关注列表/屏蔽列表'
                        else:
                            content = '【查询失败！】\n没有您的设置信息!'
                    elif len(textl) == 1:
                        content = '【设置失败！】\n请按格式正确设置关注列表或屏蔽列表！'
                    else:
                        # dic = {'关注列表':'follow', '屏蔽列表':'blacklist'}
                        id0 = decrypt_data['FromUserName']
                        info = jc.get(id0)
                        if '关注' in textl[0]:
                            if not info:
                                jc.add_update(id0, textl[1])
                            else:
                                b = info[2]
                                jc.add_update(id0, textl[1], b)
                            if textl[1] == '清空':
                                content = '【设置成功！】\n您已清空关注列表'
                            else:
                                content = '【设置成功！】\n您当前的关注列表是：{}'.format(textl[1])
                        elif '屏蔽' in textl[0]:
                            if not info:
                                jc.add_update(id=id0, follow=None, blacklist=textl[1])
                            else:
                                f = info[1]
                                jc.add_update(id0, f, textl[1])
                            if textl[1] == '清空':
                                content = '【设置成功！】\n您已清空屏蔽列表'
                            else:
                                content = '【设置成功！】\n您当前的屏蔽列表是：{}'.format(textl[1])
                        else:
                             content = '【设置失败！】\n请正确选择设置列表的名称！'
                else:
                    content = '【读取失败！】\n请正确查询或设置关注列表和屏蔽列表'
            sRespData = """<xml>
            <ToUserName>{to_username}</ToUserName>
            <FromUserName>{from_username}</FromUserName> 
            <CreateTime>{create_time}</CreateTime>
            <MsgType>text</MsgType>
            <Content>{content1}</Content>
            </xml>
            """.format(to_username=decrypt_data['ToUserName'],
            from_username=decrypt_data['FromUserName'],
            create_time=decrypt_data['CreateTime'],
            content1=content,)
    
            ret, send_msg = qy_api_jc[i].EncryptMsg(sReplyMsg=sRespData, sNonce=nonce)
            if ret == 0:
                return send_msg
            else:
                print(send_msg)
        elif decrypt_data.get('MsgType', '') == 'event':
            print('用户点击菜单')
            return ('ok!')
        else:
            sRespData = """<xml>
                               <ToUserName>{to_username}</ToUserName>
                               <FromUserName>{from_username}</FromUserName> 
                               <CreateTime>{create_time}</CreateTime>
                               <MsgType>text</MsgType>
                               <Content>{content1}</Content>
                               </xml>
                """.format(to_username=decrypt_data['ToUserName'],
                from_username=decrypt_data['FromUserName'],
                create_time=decrypt_data['CreateTime'],
                content1='【读取失败！】\n请回复文字内容！',)
            print(decrypt_data)
            ret, send_msg = qy_api_jc[i].EncryptMsg(sReplyMsg=sRespData, sNonce=nonce)
            if ret == 0:
                return send_msg
            else:
                print(send_msg)
                
# 对应步骤4中接受消息回调模式中的URL，如域名是'www.example.com' 那么在步骤4中填入的url就为"http://www.example.com/hook_path"
# @app.route('/724', methods=['GET','POST']) 
def hzqh_test():
    if request.method == 'GET':
        echo_str = signature_hzqh(request, 0)
        return(echo_str)
    elif request.method == 'POST':
        echo_str = signature2_hzqh(request, 0)
        return(echo_str)

# qy_api_hzqh = [
#     WXBizMsgCrypt("REM7ozc1e1qrjxyHtmU", "hdPCiUFw33PuFLMkqT95cHJfnW90jd9GpFQIZBMuRoz", "ww4611e131bb3a998e"), 
# ] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id
qy_api_hzqh = [
    WXBizMsgCrypt("FVOEh5SEe8oXCouAwf7yqy2zEoTX", "rveS6giVslY7JAU6KARxf2cPX48IZzmQaaRBT2sFlq5", "ww4611e131bb3a998e"), 
] #对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id

# 开启消息接受模式时验证接口连通性
def signature_hzqh(request, i): 
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret,sEchoStr=qy_api_hzqh[i].VerifyURL(msg_signature, timestamp,nonce,echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return("failed")
    else:
        return(sEchoStr)

# 实际接受消息
def signature2_hzqh(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret,sMsg=qy_api_hzqh[i].DecryptMsg(data,msg_signature, timestamp,nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return("failed")
    else:
        decrypt_data = {}
        for node in list(fromstring(sMsg.decode('utf-8'))):
            decrypt_data[node.tag] = node.text
        if decrypt_data.get('MsgType', '') == 'text':
            return 'succsess'
        elif decrypt_data.get('MsgType', '') == 'event':
            print('用户点击菜单')
            return ('ok!')
        

