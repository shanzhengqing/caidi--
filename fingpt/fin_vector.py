import openai
import pandas as pd

import pinecone
pinecone.init(api_key="#", environment="asia-northeast1-gcp")


openai.api_key = '#' #zq53
openai.organization = '#' #zq53

class content_embedding_upload():
    def __init__(self, tablename):
        self.tablename = tablename

    def download_content(self, time='none'):
        from sqlalchemy import create_engine
        engine_msg = create_engine('#')
        try:
            if time == 'none':
                df = pd.read_sql('select * from {};'.format(self.tablename), engine_msg)
            else:
                df = pd.read_sql("select * from {} where time<'{}';".format(self.tablename, time), engine_msg)
            # df.to_csv('cailianred.csv', index=False, encoding='utf-8-sig')
        except Exception as e:
            print(e)
        finally:
            engine_msg.dispose()
        return df
    
    @classmethod
    def history_batch_upload(cls, df_all, tablename:str):
        cols_info = {
            'gogoal1':['time', 'title', 'summary'], 'gogoal_aw':['time', 'title', 'summary'], 
            'gogoal_bbhc':['time', 'title', 'summary'], 'gogoal_gxe':['time', 'title', 'summary'], 
            'gogoal_pe':['time', 'title', 'summary'], 'gogoal_sds':['time', 'title', 'summary'], 
            'gogoal_sdys':['time', 'title', 'summary'], 'eastmoneyred':['time', 'title', 'digest'],
            'yicai':['time', 'title', 'content'], 'cailianred':['time', 'content'], 
            'caixin':['time', 'title', 'brief'], 'reuters':['time', 'title', 'brief'], 
            'reuters_cn':['time', 'title', 'brief'], 'wsj_cn':['time', 'title', 'brief'], 
            'ths_qna':['reply_time', 'code', 'name', 'Q', 'A'], 'bloomberg':['time', 'title'], 
            'ths_gn':['time', 'code', 'name', 'gnname', 'gncontent'], 'aisixiang':['time', 'title', 'summary'], 
            'sansheng1':['time', 'title', 'retweet_title'], 'fpanda':['time', 'title', 'retweet_title'], 
        }
        table_type = {
            'gogoal1':'rumours', 'gogoal_aw':'rumours', 'gogoal_bbhc':'rumours', 'gogoal_gxe':'rumours', 
            'gogoal_pe':'rumours', 'gogoal_sds':'rumours', 'gogoal_sdys':'rumours', 'eastmoneyred':'news_cn',
            'yicai':'news_cn', 'cailianred':'news_cn', 'caixin':'news_cn', 'reuters':'news_en', 
            'reuters_cn':'news_en', 'wsj_cn':'news_en', 'ths_qna':'ths_qna', 'bloomberg':'news_en', 
            'ths_gn':'ths_gn', 'aisixiang':'others', 'sansheng1':'rumours', 'fpanda':'rumours', 
            'report_num':'report_num', 'report_news':'report_news', 'myfxtrader':'rumours'
        }
        cols = cols_info.get(tablename, ['time', 'title'])
        df_all['content'] = df_all[cols].apply(lambda x: '\n'.join(x.astype(str)).strip(), axis=1)
        df_all.dropna(inplace=True, subset=['content'])
        df_all['ids'] = df_all['content'].apply(lambda x: uuid(x))

        batch = 100
        from tqdm import tqdm
        import warnings
        warnings.filterwarnings('ignore')
        for i in tqdm(range(0, len(df_all), batch)):
            i_end = min(len(df_all), i+batch)
            df = df_all.iloc[i:i_end]
            if 'embedding' not in df.columns:
                df['embedding'] = None
            for i in df.index.tolist():
                df.at[i, 'embedding'] = convert_to_embeddings(df.loc[i, 'content'])
            if 'reply_time' in cols:
                df = df[['reply_time', 'content', 'embedding', 'ids']]
            else:
                df = df[['time', 'content', 'embedding', 'ids']]
            df.columns = ['time', 'content', 'vectors', 'ids']
            try:
                df['year'], df['month'], df['day'] = df['time'].dt.year,df['time'].dt.month, df['time'].dt.day
            except:
                def lambda_time(t):
                    from datetime import datetime
                    t1 = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                    return t1
                df['time'] = df['time'].apply(lambda x: lambda_time(x))
                df['year'], df['month'], df['day'] = df['time'].dt.year,df['time'].dt.month, df['time'].dt.day
            df['types'] = table_type.get(tablename, 'rumours')
            vectors = df['vectors'].tolist()
            ids = df['ids'].tolist()
            metadata = pd.DataFrame(df[['content', 'types', 'year', 'month', 'day']]).to_dict(orient='records')
            to_upsert = list(zip(ids, vectors, metadata))
            # return to_upsert
            # upsert to Pinecone
            index_name = 'financial-vector'
            if index_name not in pinecone.list_indexes():
                # if does not exist, create index
                pinecone.create_index(
                    index_name,
                    dimension=1536,
                    metric='cosine',
                    # metadata_config={'indexed': ['content']}
                )
            index = pinecone.Index(index_name)
            index.upsert(vectors=to_upsert)
        return True

    @classmethod
    def create_content(cls, df, cols:list):
        if ('content' in cols) and (len(cols) == 1):
            pass
        else:
            df['content'] = df[cols].apply(lambda x: '\n'.join(x.astype(str)).strip(), axis=1)
        df.dropna(inplace=True, subset=['content'])
        df['ids'] = df['content'].apply(lambda x: uuid(x))
        # df['embedding'] = df['content'].apply(lambda x: convert_to_embeddings(x))
        # from tqdm import tqdm
        if 'embedding' not in df.columns:
            df['embedding'] = None
        # for i in tqdm(df.index.tolist()):
        for i in df.index.tolist():
            df.at[i, 'embedding'] = convert_to_embeddings(df.loc[i, 'content'])
        if 'reply_time' in cols:
            df = df[['reply_time', 'content', 'embedding', 'ids']]
        else:
            df = df[['time', 'content', 'embedding', 'ids']]
        df.columns = ['time', 'content', 'embedding', 'ids']
        try:
            df['year'], df['month'], df['day'] = df['time'].dt.year,df['time'].dt.month, df['time'].dt.day
        except:
            def lambda_time(t):
                from datetime import datetime
                t1 = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                return t1
            df['time'] = df['time'].apply(lambda x: lambda_time(x))
            df['year'], df['month'], df['day'] = df['time'].dt.year,df['time'].dt.month, df['time'].dt.day
        return df[['content', 'embedding', 'ids', 'year', 'month', 'day']]
    
    @classmethod 
    def upload_embedding_pinecone(cls, df_all:pd.DataFrame, index_name:str, tablename:str):
        # index_name = 'financial-vector'
        if index_name not in pinecone.list_indexes():
            # if does not exist, create index
            pinecone.create_index(
                index_name,
                dimension=1536,
                metric='cosine',
                # metadata_config={'indexed': ['content']}
            )
        index = pinecone.Index(index_name)
        # print(index.describe_index_stats())

        table_type = {
            'gogoal1':'rumours', 'gogoal_aw':'rumours', 'gogoal_bbhc':'rumours', 'gogoal_gxe':'rumours', 
            'gogoal_pe':'rumours', 'gogoal_sds':'rumours', 'gogoal_sdys':'rumours', 'eastmoneyred':'news_cn',
            'yicai':'news_cn', 'cailianred':'news_cn', 'caixin':'news_cn', 'reuters':'news_en', 
            'reuters_cn':'news_en', 'wsj_cn':'news_en', 'ths_qna':'ths_qna', 'bloomberg':'news_en', 
            'ths_gn':'ths_gn', 'aisixiang':'others', 'sansheng1':'rumours', 'fpanda':'rumours', 
            'report_num':'report_num', 'report_news':'report_news', 'myfxtrader':'rumours'
        }
        
        df_all.columns = ['content', 'vectors', 'ids', 'year', 'month', 'day']
        batch = 100
        # from tqdm import tqdm
        # for i in tqdm(range(0, len(df_all), batch)):
        for i in range(0, len(df_all), batch):
            i_end = min(len(df_all), i+batch)
            df = df_all.iloc[i:i_end]
            vectors = df['vectors'].tolist()
            ids = df['ids'].tolist()
            df['types'] = table_type.get(tablename, 'rumours')
            metadata = pd.DataFrame(df[['content', 'types', 'year', 'month', 'day']]).to_dict(orient='records')
            to_upsert = list(zip(ids, vectors, metadata))
            # upsert to Pinecone
            index.upsert(vectors=to_upsert)
        return True

    @classmethod
    def upload_embedding_qdrant(cls, df_all):
        from qdrant_client import QdrantClient
        from qdrant_client.http.models import Distance, VectorParams
        from qdrant_client.http.models import Batch
        df_all.columns = ['content', 'vectors', 'ids']
        start = 0
        while True:
            df = df_all.iloc[start : start+1000]
            dict_df = pd.DataFrame(df['content']).to_dict(orient='records')
            # vectors = df['vectors'].apply(lambda x: ast.literal_eval(x)).tolist()
            vectors = df['vectors'].tolist()
            ids = df['ids'].tolist()
        
            qdrant_client = QdrantClient(
                url="https://1e7256b5-ce74-4c84-a897-aeee30dcf0d5.us-east-1-0.aws.cloud.qdrant.io:6333",
                api_key="FnZLq3wuA5hJ7Kis9D2m-pMib_zjeXV3CncrAQs3FqJEM4Z6BXE0eA",
                )
            qdrant_client.recreate_collection(
                collection_name='financial-vector',
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
            qdrant_client.upsert(
                collection_name='financial_vector',
                wait=True,
                points=Batch(ids=ids, payloads=dict_df, vectors=vectors),
                    )
            start += 1000
            if start >= df_all.shape[0]:
                break
        return True
    
    @classmethod
    def search_pinecone(cls, embed, top_k, index_name:str, filters=None):
        # import pinecone
        # pinecone.init(api_key="86b9b7f7-321b-459b-8701-90c29fb41c5a", environment="asia-northeast1-gcp")
        # index_name = 'financial-vector'
        index = pinecone.Index(index_name)
        if not filters:
            res = index.query(embed, top_k=top_k, include_metadata=True)
        else:
            res = index.query(embed, filter=filters, top_k=top_k, include_metadata=True)
        return res

def todaysdate():
    from datetime import datetime
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

def search_pinecone(text:str, top_k:int, dbname:str, filters=None):
    if not text:
        return ''
    text = text.strip()
    if not filters:
        filters = {}
    contexts = search_report_num(text, filters)
    # return contexts
    if not contexts:
        top_k += 10
    def loop_search(top_k, filters):
        info = {'rumours':int(top_k/5), 'other':1, 'news':top_k-int(top_k/5)}
        c = []
        for types, n in info.items():
            if filters:
                f = filters
            else:
                f = {}
            if types != 'news':
                f['types'] = types
            else:
                f['types'] = {'$nin':['rumours', 'report_num', 'report_news', 'ths_gn', 'ths_qna']}
            res = content_embedding_upload.search_pinecone(embed, n, 'financial-vector', f)
            contexts1 = [
                x['metadata']['content'] for x in res['matches']
            ]
            contexts1 = [str(i) for i in contexts1]
            c.extend(contexts1)
        return c
    embed = convert_to_embeddings(text)
    res = loop_search(top_k, filters)
    contexts.extend(res)
    contexts = [
        '{}、{}'.format(i+1, x) for i, x in enumerate(contexts)
    ]
    contexts = '\n\n'.join(contexts)
    return contexts

def construct_text(text:str, role_msg:str):
    query = [
        # {"role": "system", "content": "You are a helpful assistant."},
        # {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
        {"role": "system", "content": role_msg},
        {"role": "user", "content": text},
        ]
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=query,
        temperature=0
        )
        res_content = response.choices[0].message.content
    except:
        # print(0)
        from time import sleep
        i = 0
        while i < 5:
            sleep(1)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=query,
                temperature=0
                )
            res_content = response.choices[0].message.content
            i += 1
        res_content = ''
    return res_content

def summary(texts:list, role_msg:str, max_length:int):
    # max_length = 800
    length = 0
    temp_text = []
    res = []
    # for text in texts:
    #     res.append(construct_text(text, role_msg))
    for text in texts:
        length += len(text)
        if length > max_length:
            length = 0 
            if not temp_text:
                query = '<金融资讯>：{}。请总结以上的资讯，保留关键的金融或公司信息，保留关键数据。如果消息包含时间信息，你会保留每条消息的时间信息。'.format(text)
                res.append(construct_text(query, role_msg))
                # print(res)
            else:
                query = '<金融资讯>：{}。请总结以上的资讯，保留关键的金融或公司信息，保留关键数据。如果消息包含时间信息，你会保留每条消息的时间信息。'.format('\n<金融资讯>：'.join(temp_text))
                res.append(construct_text(query, role_msg))
                # print(temp_text)
                # print(res)
                temp_text = []
        else:
            temp_text.append(text)
    if temp_text:
        query = '<金融资讯>：{}。请总结以上的资讯，保留关键的金融或公司信息，保留关键数据。如果消息包含时间信息，你会保留每条消息的时间信息。'.format('\n<金融资讯>：'.join(temp_text))
        res.append(construct_text(query, role_msg))
        # print(temp_text)
        # print(res)
    return '<info>\n'.join(res)

def set_time_filter():
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    ts = [datetime.now()-relativedelta(months=i) for i in range(4)]
    ts = [{'year':{'$eq':t.year}, 'month':{'$eq':t.month}} for t in ts]
    return {'$or':ts}

def search_report_num(query, filters, types='fingpt'):
    format_name, format_codename = '这是股票名称：<股票名称>', '这是股票代码和股票名称：<股票代码><股票名称>。'
    role_msg = '你拥有丰富的金融和财经知识。'
    text = '<输入的信息>：{}\
    请根据输入的信息判断。如果输入的信息不包含股票名称，请回答：没有。如果输入的信息包含股票名称但不包含股票代码，请严格按如下格式回答：{}。如果输入的信息包含股票名称也包含股票代码，请严格按如下的格式回答：{}。'.format(query, format_name, format_codename)
    judge = construct_text(text, role_msg)
    # return judge
    if '没有' in judge:
        return []
    type_info = {
        'fingpt':3, 'gpt4_fin':3
    }
    # judge = '{}-{} 现金流,营业收入,利润同比'.format(judge, todaysdate())
    c = []
    embed = convert_to_embeddings(judge)
    num = type_info.get(types, 3)
    def filter_search(embed, num, filters):
        res = content_embedding_upload.search_pinecone(embed, num, 'financial-vector', filters)
        contexts = [
            x['metadata']['content'] for x in res['matches']
        ]
        contexts = [str(i) for i in contexts]
        return contexts
    filters['types'] = 'report_num'
    c.extend(filter_search(embed, num, filters))
    if '概念' in query:
        c.extend(filter_search(embed, 5, {'types':'ths_gn'}))
        filters['types'] = 'ths_qna'
        c.extend(filter_search(embed, 5, filters))
    else:
        c.extend(filter_search(embed, 3, {'types':'ths_gn'}))
        filters['types'] = 'ths_qna'
        c.extend(filter_search(embed, 4, filters))
    # filters['types'] = {'$in':['ths_gn', 'ths_qna']}
    return c


def embed_n_search(text, top_k, types='fingpt'):
    # 近5个月的消息
    filters = set_time_filter()
    # filters = {}
    contexts = search_report_num(text, filters, types)
    # return contexts
    # embed = convert_to_embeddings('{}-{}'.format(todaysdate(), text))
    embed = convert_to_embeddings('{}'.format(text))
    if not contexts:
        type_info = {
            'fingpt':10, 'gpt4_fin':10
        }
        num = type_info.get(types, 10)
        top_k += num
    def loop_search(top_k, filters):
        info = {'rumours':int(top_k/5), 'other':1, 'news':top_k-int(top_k/5)}
        c = []
        for types, n in info.items():
            f = filters
            if types != 'news':
                f['types'] = types
            else:
                f['types'] = {'$nin':['rumours', 'report_num', 'report_news', 'ths_gn', 'ths_qna']}
            res = content_embedding_upload.search_pinecone(embed, n, 'financial-vector', f)
            contexts1 = [
                x['metadata']['content'] for x in res['matches']
            ]
            contexts1 = [str(i) for i in contexts1]
            c.extend(contexts1)
        return c
    if isinstance(top_k, int):
        # res = content_embedding_upload.search_pinecone(embed, top_k, 'financial-vector')
        res = loop_search(top_k, filters)
    else:
        # res = content_embedding_upload.search_pinecone(embed, 20, 'financial-vector')
        res = loop_search(20, filters)
    # contexts1 = [
        # x['metadata']['content'] for x in res['matches']
    # ]
    # contexts1 = [str(i) for i in contexts1]
    # contexts.extend(contexts1)
    contexts.extend(res)
    texts = '<info>\n'.join(contexts)
    # return contexts
    text_num_info = {
        'fingpt':[1200, 800], 
        'gpt4_fin':[3200, 1500],
        # 'gpt4_fin':[1200, 800],
    }
    max_len0, max_len1 = text_num_info.get(types, [1200, 800])[0], text_num_info.get(types, [1200,800])[1]
    if len(texts) > max_len0:
        role_msg = '你拥有丰富的金融和财经知识。今天的日期是{}'.format(todaysdate())
        res_content = summary(contexts, role_msg, max_len1)
        # print(res_content)
        # import sys
        # sys.stdout.flush()
        return res_content
    else:
        return texts

def upload_function(tablename:str, df:pd.DataFrame):
    cols_info = {
        'gogoal1':['time', 'title', 'summary'], 'gogoal_aw':['time', 'title', 'summary'], 
        'gogoal_bbhc':['time', 'title', 'summary'], 'gogoal_gxe':['time', 'title', 'summary'], 
        'gogoal_pe':['time', 'title', 'summary'], 'gogoal_sds':['time', 'title', 'summary'], 
        'gogoal_sdys':['time', 'title', 'summary'], 'eastmoneyred':['time', 'title', 'digest'],
        'yicai':['time', 'title', 'content'], 'cailianred':['time', 'content'], 
        'caixin':['time', 'title', 'brief'], 'reuters':['time', 'title', 'brief'], 
        'reuters_cn':['time', 'title', 'brief'], 'wsj_cn':['time', 'title', 'brief'], 
        'ths_qna':['reply_time', 'code', 'name', 'Q', 'A'], 'bloomberg':['time', 'title'], 
        'ths_gn':['time', 'code', 'name', 'gnname', 'gncontent'], 'aisixiang':['time', 'title', 'summary'], 
        'sansheng1':['time', 'title', 'retweet_title'], 'fpanda':['time', 'title', 'retweet_title'], 
                 }
    cols = cols_info.get(tablename, ['time', 'title'])
    df = content_embedding_upload.create_content(df, cols)
    res = content_embedding_upload.upload_embedding_pinecone(df, 'financial-vector', tablename)
    return res
        
def uuid(text:str):
        import uuid
        namespace = uuid.NAMESPACE_DNS
        uuid_obj = uuid.uuid5(namespace, text)
        result = str(uuid_obj)
        return result

def convert_to_embeddings(texts:str):
    embed_model = 'text-embedding-ada-002'
    try:
        res = openai.Embedding.create(input=texts, engine=embed_model)
    except:
        done = False
        while not done:
            from time import sleep
            sleep(2)
            try:
                res = openai.Embedding.create(input=texts, engine=embed_model)
                done = True
            except:
                pass
    return res.data[0]["embedding"]

if __name__ == "__main__":
    # # 补充历史数据到向量库
    # cols_info = {
    #     'gogoal1':['time', 'title', 'summary'], 'gogoal_aw':['time', 'title', 'summary'], 
    #     'gogoal_bbhc':['time', 'title', 'summary'], 'gogoal_gxe':['time', 'title', 'summary'], 
    #     'gogoal_pe':['time', 'title', 'summary'], 'gogoal_sds':['time', 'title', 'summary'], 
    #     'gogoal_sdys':['time', 'title', 'summary'], 'eastmoneyred':['time', 'title', 'digest'],
    #     'yicai':['time', 'title', 'content'], 'cailianred':['time', 'content'], 
    #     'caixin':['time', 'title', 'brief'], 'reuters':['time', 'title', 'brief'], 
    #     'reuters_cn':['time', 'title', 'brief'], 'wsj_cn':['time', 'title', 'brief'], 
    #     'ths_qna':['reply_time', 'code', 'name', 'Q', 'A'], 'bloomberg':['time', 'title'], 
    #     'ths_gn':['time', 'code', 'name', 'gnname', 'gncontent'], 'aisixiang':['time', 'title', 'summary'], 
    #     'sansheng1':['time', 'title', 'retweet_title'], 'fpanda':['time', 'title', 'retweet_title'], 
    #              }
    # tablenames = list(cols_info.keys())
    # tablenames.extend(['jefflijun', 'macrostrategist', 'xxtian', 'caolei'])
    # from tqdm import tqdm 
    # for tablename in tqdm(tablenames):
    #     if tablename == 'gogoal1':
    #         continue
    #     limit = '2023-05-06 19:11'
    #     history_df = content_embedding_upload(tablename).download_content(limit)
    #     history_df = content_embedding_upload.history_batch_upload(history_df, tablename)
    # from get_report_num import report_num_hist_script
    # report_num_hist_script('2022-12-31')
    # report_num_hist_script('2023-03-31')

    # # 测试embed search
    # # text = '请分析000977浪潮信息的财务数据，用券商的风格写一篇分析报告，字数1000字左右'
    # text = '根据光迅科技002281发布的2022年年报和2023年一季报，用券商的风格写一篇年报点评，要分条分段，第一段写业绩数字，后面三段结合业绩公司的发展趋势，最好有具体数据支持，结论维持买入评级，字数不要超过500字'
    # res1 = embed_n_search(text, 10, 'fingpt')

    # 测试搜索模块
    # text = '请分析000977浪潮信息的财务数据，用券商的风格写一篇分析报告，字数1000字左右'
    # text = '根据光迅科技002281发布的2022年年报和2023年一季报，用券商的风格写一篇年报点评，要分条分段，第一段写业绩数字，后面三段结合业绩公司的发展趋势，最好有具体数据支持，结论维持买入评级，字数不要超过500字'
    text = 'cta基金的表现'
    res2 = search_pinecone(text, 10, 'financial-vector')

    # history_df = content_embedding_upload(tablename).download_content()
    # history_df = content_embedding_upload.history_batch_upload(history_df, tablename)
    # res = content_embedding_upload.create_content(history_df, ['time', 'title', 'retweet_title'])
    
    # pinecone.delete_index("financial-vector")
    
    # path = 'C:/Users/shanz/Documents/证券投资数据积累/邯郸路菜地营业部/实时消息应用'
    # import ast
    # history_df = pd.read_csv('{}/{}.csv'.format(path, tablename))
    # history_df['embedding'] = history_df['embedding'].apply(lambda x: ast.literal_eval(x)).tolist()
    # history_df = history_df[['content', 'embedding', 'uuid']]
    
    # # 直接用content算embedding
    # df.dropna(inplace=True, subset=['content'])
    # from tqdm import tqdm
    # for i in tqdm(df.index.tolist()):
    #     df.at[i, 'embedding'] = convert_to_embeddings(df.loc[i, 'content'])
    # # df['embedding'] = df['content'].apply(lambda x: convert_to_embeddings(x))
    # df.to_csv('cailianred.csv', index=False, encoding='utf-8-sig')

    # history_df = content_embedding_upload(tablename).download_content()
    # content_embedding_upload.history_batch_upload(history_df, cols=['title', 'summary'])
    # history_df = history_content_embedding_upload.create_content(history_df, ['content'])
    # history_content_embedding_upload.upload_embedding(history_df)
    
    # cols = ['time', 'title', 'summary']
    # history_df['content'] = history_df[cols].apply(lambda x: '\n'.join(x.astype(str)).strip(), axis=1)
    
    # history_content_embedding_upload.upload_embedding_pinecone(history_df)
    # text = '量化cta有哪些因子'
    # embed = convert_to_embeddings(text)
    # res = content_embedding_upload.search_pinecone(embed, 10)
    # contexts = [
    #     x['metadata']['content'] for x in res['matches']
    # ]

    # for tablename in ['gogoal1', 'gogoal_aw', 'gogoal_bbhc', 'gogoal_gxe', 'gogoal_pe', 'gogoal_sds', 'gogoal_sdys']:
    #     history_df = content_embedding_upload(tablename).download_content()
    #     content_embedding_upload.history_batch_upload(history_df, cols=['title', 'summary'])
    
    # text = '根据000858五粮液年报，用卖方分析师的风格写一篇年报点评报告，要分条分段，第一段写公司的业绩数字，后面三段结合业绩表现和年报内容写三条公司2022年的业务发展情况以及未来发展趋势，最好有具体数据支持，请一步一步思考'
    # text = '300750宁德时代 上周有资金流入嘛？'
    # res1 = search_report_num(text, 'gpt4_fin')
    # res1 = embed_n_search(text, 15, types='gpt4_fin')
    # print(res1)

    # role_msg = '你拥有丰富的金融和财经知识你会总结用户输入的需求，并保留数据,股票代码,股票名称,基金名称等关键信息。如果消息包含时间信息，你会保留每条消息的时间信息。今天的日期是{}'.format(todaysdate())
    # texts = [text]
    # res2 = summary(texts, role_msg, 1200)
    # print(res2)

    # text = '上周有资金流入嘛？'
    # format_name, format_codename = '这是股票名称：<股票名称>', '这是股票代码和股票名称：<股票代码><股票名称>。'
    # role_msg = '你拥有丰富的金融和财经知识。你会判断输入的信息是否包含股票名称。如果否，请回答：没有。\
    #     如果是，你会进一步判断输入的信息是否包含股票代码，如果是，请严格按照如下格式回答：```{}```。\
    #         如果否，即输入的信息只包含股票名称，请严格按照如下回答：```{}```。回答时不要有任何额外解释和其他信息。'.format(format_name, format_codename)
    # res2 = construct_text(text, role_msg)

    # text = '这是股票名称：五粮液。-分配、净利润、营收'
    # res2 = embed_n_search(text, 15, types='gpt4_fin')
    

