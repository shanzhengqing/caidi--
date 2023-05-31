# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:01:17 2023

@author: shanz
"""

import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#################### client 数据库
class jc(db.Model):
    """韭菜信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "jc"
    # 字段定义
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    id = db.Column(db.String(100), primary_key=True)
    follow = db.Column(db.Text)
    blacklist = db.Column(db.Text)
    
    def __init__(self, id, follow, blacklist):
        self.id = id
        self.follow = follow
        self.blacklist = blacklist

    def __repr__(self):
        return f"{self.id}<用户>\n{self.follow}"
    
    @classmethod
    def add_update(cls, id, follow=None, blacklist=None):
        check = cls.query.get(id)
        if not check:
            jc = cls(id, follow, blacklist)
            db.session.add(jc)
        else:
            cls.query.filter(cls.id == id).update({'follow': follow, 'blacklist':blacklist})
        db.session.commit()
        return 1
    
    @classmethod
    def get(cls, id):
        check = cls.query.get(id)
        if not check:
            return []
        else:
            return [check.id, check.follow, check.blacklist]

class ths_qna(db.Model):
    """董秘信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "ths_qna"
    # 字段定义
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    id = db.Column(db.String(100), primary_key=True)
    key_word = db.Column(db.Text)
    
    def __init__(self, id, key_word,):
        self.id = id
        self.key_word = key_word

    def __repr__(self):
        return f"{self.id}<用户>\n{self.key_word}"
    
    @classmethod
    def add_update(cls, id, key_word=None, ):
        check = cls.query.get(id)
        if not check:
            ths_qna = cls(id, key_word, )
            db.session.add(ths_qna)
        else:
            cls.query.filter(cls.id == id).update({'key_word': key_word})
        db.session.commit()
        return 1
    
    @classmethod
    def get(cls, id):
        check = cls.query.get(id)
        if not check:
            return []
        else:
            return [check.id, check.key_word, ]

class c724(db.Model):
    """724用户信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "c724"
    # 字段定义
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    id = db.Column(db.String(100), primary_key=True)
    key_word = db.Column(db.Text)
    
    def __init__(self, id, key_word,):
        self.id = id
        self.key_word = key_word

    def __repr__(self):
        return f"{self.id}<用户>\n{self.key_word}"
    
    @classmethod
    def add_update(cls, id, key_word=None, ):
        check = cls.query.get(id)
        if not check:
            c724= cls(id, key_word, )
            db.session.add(c724)
        else:
            cls.query.filter(cls.id == id).update({'key_word': key_word})
        db.session.commit()
        return 1
    
    @classmethod
    def get(cls, id):
        check = cls.query.get(id)
        if not check:
            return []
        else:
            return [check.id, check.key_word, ]

class chatgpt_context(db.Model):
    """chatgpt信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "chatgpt_context"
    # 字段定义
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    id = db.Column(db.String(100), primary_key=True)
    context = db.Column(db.Text)
    
    def __init__(self, id, context):
        self.id = id
        self.context = context

    def __repr__(self):
        return f"{self.id}<用户>\n{self.context}"
    
    @classmethod
    def add_update(cls, id, context=None):
        check = cls.query.get(id)
        if not check:
            chat_context = cls(id, context)
            db.session.add(chat_context)
        else:
            cls.query.filter(cls.id == id).update({'context': context, })
        db.session.commit()
        return 1
    
    @classmethod
    def get(cls, id):
        check = cls.query.get(id)
        if not check:
            return []
        else:
            return [check.id, check.context,] 
        
class chatgpt_35(db.Model):
    """chatgpt信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "chatgpt_35"
    # 字段定义
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    id = db.Column(db.String(100), primary_key=True)
    context = db.Column(db.Text)
    
    def __init__(self, id, context):
        self.id = id
        self.context = context

    def __repr__(self):
        return f"{self.id}<用户>\n{self.context}"
    
    @classmethod
    def add_update(cls, id, context=None):
        check = cls.query.get(id)
        if not check:
            chat_context = cls(id, context)
            db.session.add(chat_context)
        else:
            cls.query.filter(cls.id == id).update({'context': context, })
        db.session.commit()
        return 1
    
    @classmethod
    def get(cls, id):
        check = cls.query.get(id)
        if not check:
            return []
        else:
            return [check.id, check.context,] 

class fingpt(db.Model):
    """chatgpt信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "fingpt"
    # 字段定义
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    id = db.Column(db.String(100), primary_key=True)
    context = db.Column(db.Text)
    
    def __init__(self, id, context):
        self.id = id
        self.context = context

    def __repr__(self):
        return f"{self.id}<用户>\n{self.context}"
    
    @classmethod
    def add_update(cls, id, context=None):
        check = cls.query.get(id)
        if not check:
            chat_context = cls(id, context)
            db.session.add(chat_context)
        else:
            cls.query.filter(cls.id == id).update({'context': context, })
        db.session.commit()
        return 1
    
    @classmethod
    def get(cls, id):
        check = cls.query.get(id)
        if not check:
            return []
        else:
            return [check.id, check.context,]

class gpt4_caidi(db.Model):
    """chatgpt信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "gpt4_caidi"
    # 字段定义
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    id = db.Column(db.String(100), primary_key=True)
    context = db.Column(db.Text)
    
    def __init__(self, id, context):
        self.id = id
        self.context = context

    def __repr__(self):
        return f"{self.id}<用户>\n{self.context}"
    
    @classmethod
    def add_update(cls, id, context=None):
        check = cls.query.get(id)
        if not check:
            chat_context = cls(id, context)
            db.session.add(chat_context)
        else:
            cls.query.filter(cls.id == id).update({'context': context, })
        db.session.commit()
        return 1
    
    @classmethod
    def get(cls, id):
        check = cls.query.get(id)
        if not check:
            return []
        else:
            return [check.id, check.context,]

class gpt4_fin(db.Model):
    """chatgpt信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "gpt4_fin"
    # 字段定义
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    id = db.Column(db.String(100), primary_key=True)
    context = db.Column(db.Text)
    
    def __init__(self, id, context):
        self.id = id
        self.context = context

    def __repr__(self):
        return f"{self.id}<用户>\n{self.context}"
    
    @classmethod
    def add_update(cls, id, context=None):
        check = cls.query.get(id)
        if not check:
            chat_context = cls(id, context)
            db.session.add(chat_context)
        else:
            cls.query.filter(cls.id == id).update({'context': context, })
        db.session.commit()
        return 1
    
    @classmethod
    def get(cls, id):
        check = cls.query.get(id)
        if not check:
            return []
        else:
            return [check.id, check.context,]
        
class gpt35_hint(db.Model):
    """chatgpt提示模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "gpt35_hint"
    # 字段定义
    """
    create table db_student(
      id int primary key auto_increment comment="主键",
      name varchar(15) comment="姓名",
    )
    """
    id = db.Column(db.String(100), primary_key=True)
    context = db.Column(db.Text)
    
    def __init__(self, id, context):
        self.id = id
        self.context = context

    def __repr__(self):
        return f"{self.id}<用户>\n{self.context}"
    
    @classmethod
    def add_update(cls, id, context=None):
        check = cls.query.get(id)
        if not check:
            chat_context = cls(id, context)
            db.session.add(chat_context)
        else:
            cls.query.filter(cls.id == id).update({'context': context, })
        db.session.commit()
        return 1
    
    @classmethod
    def get(cls, id):
        check = cls.query.get(id)
        if not check:
            return []
        else:
            return [check.id, check.context,]

########################## 抓取消息的数据库        
class msg_rcn(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'reuters_cn'
    article_id = db.Column(db.String(30), primary_key=True)
    link = db.Column(db.Text)
    title = db.Column(db.String(300))
    brief = db.Column(db.Text)
    updated_time = db.Column(db.DateTime)
    published_time = db.Column(db.DateTime)
    time = db.Column(db.DateTime, primary_key=True)
    display_time = db.Column(db.DateTime)
    author = db.Column(db.Text)
    author_email = db.Column(db.Text)
    pic = db.Column(db.Text)

class msg_rglb(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'reuters'
    time = db.Column(db.DateTime, primary_key=True)
    title = db.Column(db.Text)
    link = db.Column(db.Text)
    brief = db.Column(db.Text)
    article_id = db.Column(db.String(30), primary_key=True)

class msg_caixin(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'caixin'
    time = db.Column(db.DateTime, primary_key=True)
    brief = db.Column(db.Text)
    link = db.Column(db.String(100))
    title = db.Column(db.String(300), primary_key=True)

class msg_wsj_cn(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'wsj_cn'
    article_id = db.Column(db.String(100), primary_key=True)
    link = db.Column(db.Text)
    title = db.Column(db.Text)
    brief = db.Column(db.Text)
    time = db.Column(db.DateTime, primary_key=True)
    author = db.Column(db.Text)
    pic = db.Column(db.Text)

class msg_yicai(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'yicai'
    title = db.Column(db.String(400))
    time = db.Column(db.DateTime)
    content = db.Column(db.Text)
    link = db.Column(db.String(100))
    keyword = db.Column(db.Text)
    check = db.Column(db.BigInteger)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_eastmoneyred(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'eastmoneyred'
    time = db.Column(db.DateTime)
    title = db.Column(db.Text)
    digest = db.Column(db.Text)
    newsid = db.Column(db.String(30))
    link = db.Column(db.Text)
    keyword = db.Column(db.Text)
    check = db.Column(db.BigInteger)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_jcdata(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'jcdata'
    time = db.Column(db.DateTime)
    title = db.Column(db.Text)
    article_id = db.Column(db.String(20))
    link = db.Column(db.Text)
    nickname = db.Column(db.Text)
    stock = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_ths_qna(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'ths_qna'
    name = db.Column(db.String(50))
    code = db.Column(db.String(6))
    reply_time = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    Q = db.Column(db.Text)
    A = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_caolei(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'caolei'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    media_url = db.Column(db.Text)
    id_str = db.Column(db.Text)
    media_route = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_ths_gn(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'ths_gn'
    code = db.Column(db.String(6))
    name = db.Column(db.String(15))
    gncontent = db.Column(db.Text)
    cid = db.Column(db.String(6))
    gnname = db.Column(db.String(20))
    time = db.Column(db.DateTime)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_cailianred(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'cailianred'
    time = db.Column(db.DateTime)
    brief = db.Column(db.Text)
    content = db.Column(db.Text)
    id = db.Column(db.BigInteger)
    keyword = db.Column(db.Text)
    stock = db.Column(db.Text)
    subjects = db.Column(db.Text)
    sid = db.Column(db.BigInteger, primary_key=True)

class msg_aisixiang(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'aisixiang'
    time = db.Column(db.DateTime)
    title = db.Column(db.Text)
    link = db.Column(db.Text)
    summary = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_cfake(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'cfake'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    media_url = db.Column(db.Text)
    id_str = db.Column(db.Text)
    quote_url = db.Column(db.Text)
    video_check = db.Column(db.BigInteger)
    media_route = db.Column(db.Text)
    video_url = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_lilaoshi(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'lilaoshi'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    media_url = db.Column(db.Text)
    id_str = db.Column(db.Text)
    quote_url = db.Column(db.Text)
    video_check = db.Column(db.BigInteger)
    media_route = db.Column(db.Text)
    video_url = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_junmahe(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'junmahe'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    media_url = db.Column(db.Text)
    id_str = db.Column(db.Text)
    quote_url = db.Column(db.Text)
    video_check = db.Column(db.BigInteger)
    media_route = db.Column(db.Text)
    video_url = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_macrostrategist(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'macrostrategist'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    media_url = db.Column(db.Text)
    id_str = db.Column(db.Text)
    quote_url = db.Column(db.Text)
    rumor_check = db.Column(db.BigInteger)
    media_route = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_mao(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'mao'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    media_url = db.Column(db.Text)
    id_str = db.Column(db.Text)
    quote_url = db.Column(db.Text)
    video_check = db.Column(db.BigInteger)
    media_route = db.Column(db.Text)
    video_url = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)
    
class msg_ttbot(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'ttbot'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    media_url = db.Column(db.Text)
    id_str = db.Column(db.Text)
    quote_url = db.Column(db.Text)
    video_check = db.Column(db.BigInteger)
    media_route = db.Column(db.Text)
    video_url = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_wm(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'wm'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    media_url = db.Column(db.Text)
    id_str = db.Column(db.Text)
    quote_url = db.Column(db.Text)
    video_check = db.Column(db.BigInteger)
    media_route = db.Column(db.Text)
    video_url = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_gogoal(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'gogoal1'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    summary = db.Column(db.DECIMAL)
    summary_check = db.Column(db.BigInteger)
    download_url = db.Column(db.Text)
    mroute_check = db.Column(db.Text)
    media_route = db.Column(db.Text)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_sansheng1(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'sansheng1'
    title = db.Column(db.Text)
    time = db.Column(db.DateTime)
    length = db.Column(db.BigInteger)
    media_url = db.Column(db.Text)
    download_url = db.Column(db.Text)
    mroute_check = db.Column(db.BigInteger)
    media_route = db.Column(db.Text)
    retweet_title = db.Column(db.Text)
    retweet_check =db.Column(db.BigInteger)
    id = db.Column(db.BigInteger, primary_key=True)

class msg_blood(db.Model):
    __bind_key__ = 'msg'
    __tablename__ = 'blood'
    product_name = db.Column('产品名称', db.Text)
    batch_num = db.Column('批号', db.Text)
    expire_date = db.Column('有效期至', db.Text)
    certificate_holder = db.Column('上市许可持有人', db.Text)
    certificate_num = db.Column('证书编号', db.Text)
    result = db.Column('签发结论', db.Text)
    regulator = db.Column('批签发机构', db.Text)
    time = db.Column('签发日期', db.DateTime)
    manufacturer = db.Column('生产企业', db.Text)
    specification = db.Column('规格', db.Text)
    volume = db.Column('签发量', db.Text)
    test_num = db.Column('收检编号', db.Text)
    report_num = db.Column('报告编号', db.Text)
    id = db.Column(db.BigInteger, primary_key=True)