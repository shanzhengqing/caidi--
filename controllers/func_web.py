# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 14:46:50 2023

@author: shanz
"""

from corpwechatbot.app import AppMsgSender
from models.dbs import msg_rcn, msg_rglb, msg_caixin, msg_wsj_cn, \
    msg_yicai, msg_eastmoneyred, msg_jcdata, \
        msg_ths_qna, msg_caolei, msg_ths_gn, \
            msg_cailianred, msg_aisixiang, msg_cfake, msg_lilaoshi, \
                msg_junmahe, msg_macrostrategist, msg_mao, \
                    msg_ttbot, msg_wm, msg_gogoal, msg_sansheng1, msg_blood
from flask import request, redirect, render_template, session, jsonify, make_response, url_for, flash
from flask_paginate import Pagination
from sqlalchemy import or_
from urllib import parse
import requests
import json
import re

# @app.route('/login', methods=['GET']) #构造qr_code
def login():
    """
    获取微信授权码
    :param code:前端或app拉取的到临时授权码
    :param flag:web端或app端
    :return:None 或 微信授权数据
    """
    # 先通过session判断登陆状态
    uid = session.get('uid', '')
    if uid:
        flash('登陆成功')
        return redirect('/index/{}'.format(uid))
    # 构造登陆链接
    # appid, rurl = 'wwacaf3117a9b4c6ad', 'http://www.handanrdcaidi.xyz/vip'
    appid, rurl = 'wwacaf3117a9b4c6ad', 'http://www.handanrdcaidi.com/vip'
    # 把查询条件转成url中形式
    fields = parse.urlencode(
        {"appid": appid, "redirect_uri": rurl,
        "response_type": 'code', "scope": "snsapi_base", #静默授权
        'agentid':'1000015'}, 
    )
    # fields = parse.urlencode(
    #     {"appid": appid, "redirect_uri": rurl,
    #     "response_type": 'code', "scope": "snsapi_privateinfo", #手动授权
    #     'agentid':'1000015', 'state':'qrcode'}, 
    # )
    # # 判断是不是微信客户端，构造不同的登陆链接
    ua = request.headers.get('user-agent', '')
    ua_wp = request.headers.get('wxuserAgent', '')
    if ('MicroMessenger' in ua or 'MicroMessenger' in ua_wp):
        # 拼接请求链接
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?{}{}'.format(fields, '#wechat_redirect') 
        return redirect(url)
    else:
        # 拼接请求链接
        url = 'https://open.work.weixin.qq.com/wwopen/sso/qrConnect?{}{}'.format(fields, '#wechat_redirect') 
        return redirect(url)

# @app.route("/vip", methods=["GET"])
def get_uid():
    """
    测试微信登陆注册
    :return:
    """
    url = 'https://qyapi.weixin.qq.com/cgi-bin/auth/getuserinfo'
    
    
    code = request.args.get('code', '')
    if not code:
        return redirect('/login')
    # return code
    app = AppMsgSender(corpid='wwacaf3117a9b4c6ad',  # 你的企业id
                       corpsecret='BmQG_ShdpWpZMWb8a4FNFA9iPKkCRmJ3rl-ju1nfPDs',  # 你的应用凭证密钥
                       agentid='1000015',
                       ) 
    atoken = app.get_assess_token()
    # url_detail = 'https://qyapi.weixin.qq.com/cgi-bin/user/get' #用user_id
    url_detail = 'https://qyapi.weixin.qq.com/cgi-bin/auth/getuserdetail?access_token={}'.format(atoken) #用user_ticket
    
    params = {
        'access_token': atoken,
        'code': code
        }
    req = requests.get(url, params=params)
    info = json.loads(req.text)
    uid = info.get('userid', '')
    session.permanent = True
    session['uid'] = uid
    flash('登陆成功')
    return redirect('/index/{}'.format(uid))
    # return '用户名是{}'.format(uid)
    # user_ticket = info.get('user_ticket', '')
    # form = json.dumps({'user_ticket':user_ticket})
    # req_detail = requests.post(url=url_detail, data=form)
    # info = json.loads(req_detail.text)
    # return json.loads(req_detail.text)
    # return render_template('test.html', info=info)

# @app.route("/index/<string:uid>")
def logged_in(uid):
    # # 注意这个uid不可靠
    # uid_from_session = session.get('uid', '')
    # if not uid_from_session:
    #     # 可以考虑加一个中间页面
    #     return redirect('/login')
    if 'uid' not in session:
        return redirect('/login')
    else:
        # uid = uid_from_session
        # 路透中文
        rcns = msg_rcn.query.order_by(msg_rcn.published_time.desc()).distinct().limit(3).all()
        # 路透国际
        rglbs = msg_rglb.query.order_by(msg_rglb.time.desc()).distinct().limit(3).all()
        # 财新
        caixins = msg_caixin.query.order_by(msg_caixin.time.desc()).distinct().limit(5).all()
        # 华尔街日报
        wsj_cns = msg_wsj_cn.query.order_by(msg_wsj_cn.time.desc()).distinct().limit(3).all()
        # 一财
        yicai = msg_yicai.query.order_by(msg_yicai.time.desc()).distinct().limit(5).all()        
        # 东财
        eastmoneyred = msg_eastmoneyred.query.order_by(msg_eastmoneyred.time.desc()).distinct().limit(5).all()
        # 给网页设置utf-8
        response = set_header(render_template('index.html', rcns=rcns, 
                                             rglbs=rglbs,
                                             caixins=caixins,
                                             wsj_cns=wsj_cns,
                                             yicai=yicai,
                                             eastmoneyred=eastmoneyred))
        return response
    # return '用户{}，你好！欢迎来到菜地营业部'.format(uid)

def index():
    # 路透中文
    rcns = msg_rcn.query.order_by(msg_rcn.published_time.desc()).distinct().limit(3).all()
    # 路透国际
    rglbs = msg_rglb.query.order_by(msg_rglb.time.desc()).distinct().limit(3).all()
    # 财新
    caixins = msg_caixin.query.order_by(msg_caixin.time.desc()).distinct().limit(5).all()
    # 华尔街日报
    wsj_cns = msg_wsj_cn.query.order_by(msg_wsj_cn.time.desc()).distinct().limit(3).all()
    # 一财
    yicai = msg_yicai.query.order_by(msg_yicai.time.desc()).distinct().limit(5).all()        
    # 东财
    eastmoneyred = msg_eastmoneyred.query.order_by(msg_eastmoneyred.time.desc()).distinct().limit(5).all()
    # 给网页设置utf-8
    response = set_header(render_template('index.html', rcns=rcns, 
                                         rglbs=rglbs,
                                         caixins=caixins,
                                         wsj_cns=wsj_cns,
                                         yicai=yicai,
                                         eastmoneyred=eastmoneyred))
    return response

def contact():
    return set_header(render_template('lianxi.html'))

def set_header(rtemplate):
    response = make_response(rtemplate)
    response.headers['Content-Type'] = "text/html; charset=utf-8"
    return response

def lists(temp_db, pagenum, perpage):
    """

    Parameters
    ----------
    temp_db : model
        查询的数据库.
    pagenum : int
        查询的页码.
    perpage : int
        每页的内容数.

    Returns
    -------
    pagedata : 分页数据.
    pageination : object, 分页器

    """
    paginate = temp_db.query.order_by(temp_db.time.desc()).distinct().paginate(page=pagenum, per_page=perpage, error_out=False)
    pagedata = paginate.items  # 当前页数的记录列表
    total = paginate.total
    pagination = Pagination(page=pagenum, total=total, per_page=perpage)
    return pagedata, pagination

def searches(temp_db, rule, pagenum, perpage):
    """

    Parameters
    ----------
    temp_db : model
        查询的数据库.
    rule : list
        列表化的查询条件
    pagenum : int
        查询的页码.
    perpage : int
        每页的内容数.

    Returns
    -------
    pagedata : 分页数据.
    pageination : object, 分页器

    """
    paginate = temp_db.query.filter(or_(*rule)).order_by(temp_db.time.desc()).distinct().paginate(page=pagenum, per_page=perpage, error_out=False)
    pagedata = paginate.items  # 当前页数的记录列表
    total = paginate.total
    pagination = Pagination(page=pagenum, total=total, per_page=perpage)
    return pagedata, pagination

def search_n_list(method, indicator):
    # 名字字典
    map_name = {'aisixiang':'爱思想', 'cailianred':'财联社标红内容', 
                'caixin':'财新', 'caolei':'曹三石', 'jcdata':'韭菜公社', 
                'reuters':'路透国际', 'reuters_cn':'路透中国', 'ths_gn':'同花顺概念',
                'ths_qna':'董秘问答', 'wsj_cn':'华尔街中国', 'yicai':'第一财经', 
                'blood':'生物制品批签发'}
    name = map_name.get(indicator, '新闻内容')
    # 每页内容数字典
    map_perpage = {'cailianred':5, 'caixin':5, 'eastmoneyred':5, 
                   'jcdata':5, 'ths_qna':5, 'yicai':5, 'blood':15}
    perpage = map_perpage.get(indicator, 3)
    # 模板对应字典 还缺aisixiang和strat
    map_template = {'cailianred':'notitile', 'caixin':'newspage', 
                    'eastmoneyred':'newspage', 'gogoal':'notitile', 
                    'jcdata':'jcdata', 'reuters':'newspage',
                    'reuters_cn':'newspage', 'sansheng1':'notitile',
                    'ths_gn':'ths_gn', 'ths_qna':'ths_qna',
                    'wsj_cn':'newspage', 'yicai':'newspage', 'blood':'blood'}
    template_name = map_template.get(indicator, 'tweet')
    # 禁止非会员看的内容
    if template_name == 'tweet':
        prohibit = 1
    elif indicator in ['gogoal', 'sansheng1']:
        prohibit = 1
    else:
        prohibit = 0
    # 数据库名字典
    map_db = {'reuters':'rglb', 'reuters_cn':'rcn'}
    dbname = 'msg_{}'.format(map_db.get(indicator, indicator))
    temp_db = globals().get(dbname, None)
    pagenum = request.args.get('page', 1, type=int)
    # 查uid看看登录没
    # uid_from_session = session.get('uid', '')
    # 先判断是搜索还是查列表
    if method == 'list':
        pagedata, pagination = lists(temp_db, pagenum, perpage)
        # if uid_from_session:
        if 'uid' in session:
            if pagedata:
                return set_header(render_template('{}.html'.format(template_name), 
                                       pagination=pagination, 
                                       pagedata=pagedata,
                                       name=name))
            else:
                return set_header(render_template('404.html', name=name))
        elif prohibit == 1:
            return set_header(render_template('no_access.html', name=name))
        elif pagenum > 1:
            return set_header(render_template('no_access.html', name=name))
        else:
            return set_header(render_template('{}.html'.format(template_name), 
                                   pagination=pagination, 
                                   pagedata=pagedata, 
                                   name=name))
        
    elif method == 'search':
        # if uid_from_session:
        if 'uid' in session:
            if indicator == 'set_db':
                set_db = request.form.get('search_roll', '')
                if not set_db:
                    return set_header(render_template('404.html', name=name))
                keywords = request.form.get('keywords', '')
                return redirect(url_for('webs.search_n_list', method='search',
                                                              indicator=set_db,
                                                              keywords=keywords))
            elif temp_db:
                keywords = request.args.get('keywords', '')
                if not keywords:
                    return redirect(url_for('webs.search_n_list', method='list',
                                                                  indicator=indicator,))
                keywords = re.split('[,，\s]+', keywords)
                keywords = ['%{}%'.format(i) for i in keywords]
                # 设置规则
                rule = []
                if template_name == 'jcdata':
                    rule.extend([temp_db.title.like(k) for k in keywords])
                    rule.extend([temp_db.nickname.like(k) for k in keywords])
                    rule.extend([temp_db.stock.like(k) for k in keywords])
                elif template_name == 'newspage':
                    if indicator not in ['yicai', 'eastmoneyred']:
                        rule.extend([temp_db.title.like(k) for k in keywords])
                        rule.extend([temp_db.brief.like(k) for k in keywords])
                    elif indicator == 'yicai':
                        rule.extend([temp_db.title.like(k) for k in keywords])
                        rule.extend([temp_db.content.like(k) for k in keywords])
                    elif indicator == 'eastmoneyred':
                        rule.extend([temp_db.title.like(k) for k in keywords])
                        rule.extend([temp_db.digest.like(k) for k in keywords])
                elif template_name == 'notitile':
                    if indicator == 'cailianred':
                        rule.extend([temp_db.content.like(k) for k in keywords])
                    elif indicator == 'gogoal':
                        rule.extend([temp_db.title.like(k) for k in keywords])
                        rule.extend([temp_db.summary.like(k) for k in keywords])
                    elif indicator == 'sansheng1':
                        rule.extend([temp_db.title.like(k) for k in keywords])
                elif template_name == 'ths_gn':
                    rule.extend([temp_db.code.like(k) for k in keywords])
                    rule.extend([temp_db.name.like(k) for k in keywords])
                    rule.extend([temp_db.gnname.like(k) for k in keywords])
                    rule.extend([temp_db.gncontent.like(k) for k in keywords])
                elif template_name == 'ths_qna':
                    rule.extend([temp_db.code.like(k) for k in keywords])
                    rule.extend([temp_db.name.like(k) for k in keywords])
                    rule.extend([temp_db.Q.like(k) for k in keywords])
                    rule.extend([temp_db.A.like(k) for k in keywords])
                else:
                    rule.extend([temp_db.title.like(k) for k in keywords])
                # 分页
                pagedata, pagination = searches(temp_db, rule, pagenum, perpage)
                if pagedata:
                    return set_header(render_template('{}.html'.format(template_name), 
                                           pagination=pagination, 
                                           pagedata=pagedata,
                                           name=name))
                else:
                    return set_header(render_template('404.html', name=name))
        else:
            return set_header(render_template('no_access.html', name=name))