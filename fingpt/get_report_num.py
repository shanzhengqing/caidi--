import requests
import pandas as pd

def get_report_news_hist(page:int):
    from fin_vector import uuid, convert_to_embeddings, content_embedding_upload
    url = 'http://data.eastmoney.com/dataapi/search/article?keyword=%E8%B4%A2%E6%8A%A5&page={}&pagesize=50&keywordPhase=true&excludeChannels%5B%5D=1'.format(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'data.eastmoney.com',
        'Referer': 'http://data.eastmoney.com/bbsj/',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        res = r.json()
    except:
        return pd.DataFrame()
    if res['msg'] == 'OK':
        df = pd.DataFrame(res['result']['cmsArticleWeb'])
        cols = ['date', 'title', 'content', 'mediaName']
        df['content'] = df[cols].apply(lambda x: '\n'.join(x.astype(str)).strip(), axis=1)
        df.dropna(inplace=True, subset=['content'])
        df['ids'] = df['content'].apply(lambda x: uuid(x))
        df['embeddings'] = df['content'].apply(lambda x: convert_to_embeddings(x))
        df = df[['content', 'embeddings', 'ids']]
        content_embedding_upload.upload_embedding_pinecone(df, 'financial-vector')
        return df
    else:
        return pd.DataFrame()

def get_report_num_hist(page:int, report_period:str):
    from fin_vector import uuid, convert_to_embeddings, content_embedding_upload
    url = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Host': 'datacenter-web.eastmoney.com',
        'Referer': 'https://data.eastmoney.com/',
        'Accept': '*/*',
    }
    params = {
        'callback': 'jQuery112300021129960147092675_1682518669257',
        'sortColumns': 'UPDATE_DATE,SECURITY_CODE',
        'sortTypes': '-1,-1',
        'pageSize': '50',
        'pageNumber': str(page),
        'reportName': 'RPT_LICO_FN_CPD', 
        'columns': 'ALL',
        # "filter": "(REPORTDATE='2022-12-31')",
        'filter': "(REPORTDATE='{}')".format(report_period)
    }
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.encoding = r.apparent_encoding
        # return r.text
        res = r.text.replace('jQuery112300021129960147092675_1682518669257(', '').rstrip(');')
        import json 
        res = json.loads(res)
        # return res
    except:
        return pd.DataFrame()
    if res['message'] == 'ok':
        df = pd.DataFrame(res['result']['data'])
        col_namespace = {
            'ASSIGNDSCRPT':'利润分配', 'BASIC_EPS':'每股收益（元）', 'BPS':'每股净资产（元）',
            'DATATYPE':'报告类型', 'DEDUCT_BASIC_EPS':'扣非每股收益（元）', 'MGJYXJJE':'每股经营性现金流（元）',
            'SJLHZ':'净利润环比增长（%）', 'SJLTZ':'净利润同比增长（%）', 'TOTAL_OPERATE_INCOME':'营业总收入（元）',
            'WEIGHTAVG_ROE':'净资产收益率（%）', 'XSMLL':'销售毛利率（%）', 'YSHZ':'营收环比增长（%）', 
            'YSTZ':'营收同比增长（%）', 'PARENT_NETPROFIT':'净利润（元）', 
        }
        df.rename(columns=col_namespace, inplace=True)
        selected_cols = [
            'SECURITY_CODE', 'SECURITY_NAME_ABBR', 'EITIME'
        ]
        selected_cols.extend(col_namespace.keys())
        def apply_content(x):
            ca = []
            for col in selected_cols:
                n = col_namespace.get(col, '')
                if n:
                    c = '{}:{}'.format(n, x[n])
                else:
                    c = '{}'.format(x[col])
                ca.append(c)
            return ''.join(ca)
        df['content'] = df.apply(lambda x: apply_content(x), axis=1)
        df['ids'] = df['content'].apply(lambda x: uuid(x))
        try:
            df['year'], df['month'], df['day'] = df['EITIME'].dt.year,df['EITIME'].dt.month, df['EITIME'].dt.day
        except:
            def lambda_time(t):
                from datetime import datetime
                t1 = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                return t1
            df['EITIME'] = df['EITIME'].apply(lambda x: lambda_time(x))
            df['year'], df['month'], df['day'] = df['EITIME'].dt.year,df['EITIME'].dt.month, df['EITIME'].dt.day
        df.dropna(inplace=True, subset=['content'])
        # return df
        df['embeddings'] = df['content'].apply(lambda x: convert_to_embeddings(x))
        df = df[['content', 'embeddings', 'ids', 'year', 'month', 'day']]
        # return df
        content_embedding_upload.upload_embedding_pinecone(df, 'financial-vector', 'report_num')
        return df
    else:
        return pd.DataFrame()

def get_report_num_hist_page_all(report_period:str):
    url = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Host': 'datacenter-web.eastmoney.com',
        'Referer': 'https://data.eastmoney.com/',
        'Accept': '*/*',
    }
    params = {
        'callback': 'jQuery112300021129960147092675_1682518669257',
        'sortColumns': 'UPDATE_DATE,SECURITY_CODE',
        'sortTypes': '-1,-1',
        'pageSize': '50',
        'pageNumber': '1',
        'reportName': 'RPT_LICO_FN_CPD', 
        'columns': 'ALL',
        # "filter": "(REPORTDATE='2022-12-31')",
        'filter': "(REPORTDATE='{}')".format(report_period)
    }
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.encoding = r.apparent_encoding
        # return r.text
        res = r.text.replace('jQuery112300021129960147092675_1682518669257(', '').rstrip(');')
        import json 
        res = json.loads(res)
        # return res
    except:
        return -1
    if res['message'] == 'ok':
        return res['result']['pages']
    else:
        return -1

def report_num_hist_script(report_period:str):
    while True:
        pages = get_report_num_hist_page_all(report_period)
        if pages != -1:
            break
        else:
            import time
            time.sleep(1)
    from tqdm import tqdm
    for i in tqdm(range(1, pages+1)):
        res = get_report_num_hist(i, report_period)
    return True

if __name__ == '__main__':
    # from tqdm import tqdm
    # for i in tqdm(range(1, 21)):
    #     report_num = get_report_news_hist(i)
    # print(report_num)
    # res = get_report_num_hist(2)
    # from tqdm import tqdm
    # for i in tqdm(range(2, 176)):
    #     res = get_report_num_hist(i)
    res = get_report_num_hist(page=1, report_period='2023-06-30')