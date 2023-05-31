# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 15:30:35 2023

@author: shanz
"""

from flask import Blueprint
# from controllers.func_key import hzqh_test
# from controllers.func_key import chatgpt_c
from controllers.func_key import chatgpt_general
from controllers.func_key import chatgpt_code
from controllers.func_key import gpt4_fin_server, gpt4_caidi_server, gpt35_hint_server
from controllers.func_key import douban_724, douban_jc, douban_ths_QnA, chatgpt_img, chatgpt_c35, fingpt_server, search_fin_server
from controllers.func_web import logged_in, login, get_uid, index, search_n_list, contact
from controllers.func_line import line_gpt
from controllers.test import test_webgpt

keyword = Blueprint('keyword', __name__)
# keyword.route('/hzqh', methods=['GET', 'POST'])(hzqh_test)
keyword.route('/724', methods=['GET', 'POST'])(douban_724)
keyword.route('/jc', methods=['GET', 'POST'])(douban_jc)
keyword.route('/QnA', methods=['GET', 'POST'])(douban_ths_QnA)
# keyword.route('/chatgpt', methods=['GET', 'POST'])(chatgpt_c)
keyword.route('/chatgpt35', methods=['GET', 'POST'])(chatgpt_c35)
keyword.route('/chatimg', methods=['GET', 'POST'])(chatgpt_img)
keyword.route('/chatcode', methods=['GET', 'POST'])(chatgpt_code)
keyword.route('/gpt_general/<string:key_type>', methods=['GET', 'POST'])(chatgpt_general)
keyword.route('/fingpt', methods=['GET', 'POST'])(fingpt_server)
keyword.route('/gpt4_fin', methods=['GET', 'POSt'])(gpt4_fin_server)
keyword.route('/gpt4_caidi', methods=['GET', 'POSt'])(gpt4_caidi_server)
keyword.route('/search_fin', methods=['GET', 'POSt'])(search_fin_server)
keyword.route('/gpt35_hint', methods=['GET', 'POSt'])(gpt35_hint_server)

webs = Blueprint('webs', __name__)
webs.route('/login', methods=['GET'])(login)
webs.route("/vip", methods=["GET"])(get_uid)
webs.route("/index/<string:uid>", methods=['GET'])(logged_in)
webs.route('/', methods=['GET'])(index)
webs.route('/index', methods=['GET'])(index)
webs.route('/sl/<string:method>/<string:indicator>', methods=['GET', 'POST'])(search_n_list)
webs.route('/contact', methods=['GET'])(contact)

line = Blueprint('line', __name__)
line.route('/line/<string:types>', methods=['GET', 'POST'])(line_gpt)

test = Blueprint('test', __name__)
# test.route('/test', methods=['POST'])(test_webgpt)