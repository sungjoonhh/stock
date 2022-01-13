import OpenDartReader
import pandas as pd
import time

import sys
sys.path.append('C:\\Users\\sungjoon\\libs')
from postLib import  PostgresDataClass

#%%
def read_data( path) -> dict:
    """

    :rtype: object
    """
    ret_val = {}
    fp = open(path, 'r')
    read_line = fp.readlines()
    for itr in read_line:
        temp = itr.split('=')
        ret_val[temp[0]] = temp[1].replace('\n','')
    return ret_val


#%%
api_dict = read_data('C:\\Users\\sungjoon\\libs\\api_key.txt')
api_key = api_dict['api_key']

dart = OpenDartReader(api_key)
#%%
stock_name = 'SK이노베이션'

df2 = pd.DataFrame(columns=['유동자산_재무상태표', '부채총계_재무상태표', '자본총계_재무상태표', '매출액_손익계산서', '매출총이익_손익계산서', '영업이익_손익계산서', '당기순이익_손익계산서', '영업활동현금흐름_현금흐름표',  '잉여현금흐름_현금흐름표'], index=['1900-01-01'])
reprt_code = ['11013', '11012', '11014', '11011'] # '11013'=1분기보고서, '11012' =반기보고서, '11014'=3분기보고서, '11011'=사업보고서
#%%
for i in range(2018, 2022): # OpenDart는 2015년부터 정보를 제공한다.

    # 더미 리스트 초기화. 1 ~ 4 분기 데이터를 합할 예정이므로 4 크기 만큼의 리스트 선언.
    current_assets = [0, 0, 0, 0] # 유동자산
    liabilities = [0, 0, 0, 0] # 부채총계
    equity = [0, 0, 0, 0] # 자본총계
    revenue = [0, 0, 0, 0] # 매출액 
    grossProfit = [0, 0, 0, 0] # 매출총이익
    income = [0, 0, 0, 0] # 영업이익
    net_income = [0, 0, 0, 0] # 당기순이익
    cfo = [0, 0, 0, 0] # 영업활동현금흐름
    cfi = [0, 0, 0, 0] # 투자활동현금흐름
    fcf = [0, 0, 0, 0] # 잉여현금흐름 : 편의상 영업활동 - 투자활동 현금흐름으로 계산

    for j, k in enumerate(reprt_code):
        df1 = pd.DataFrame() # Raw Data
        if str(type(dart.finstate_all(stock_name, i, reprt_code=k, fs_div='CFS'))) == "<class 'NoneType'>":
            pass
            
        # 타입이 NoneType 이 아니면 읽어온다.    
        else: 
            df1 = df1.append(dart.finstate_all(stock_name, i, reprt_code=k, fs_div='CFS')) 
            # 재무상태표 부분
            condition = (df1.sj_nm == '재무상태표') & (df1.account_nm == '유동자산') # 유동자산
            condition_2 = (df1.sj_nm == '재무상태표') & (df1.account_nm == '부채총계') # 부채총계
            condition_3 = (df1.sj_nm == '재무상태표') & \
                        ((df1.account_nm == '자본총계') | (df1.account_nm == '반기말자본') | (df1.account_nm == '3분기말자본') | (df1.account_nm == '분기말자본') | (df1.account_nm == '1분기말자본'))  #자본총계
                        
            # 손익계산서 부분
            condition_4 = ((df1.sj_nm == '손익계산서') | (df1.sj_nm == '포괄손익계산서')) & ((df1.account_nm == '매출액') | (df1.account_nm == '수익(매출액)')| (df1.account_nm == '매출'))
            condition_5 = ((df1.sj_nm == '손익계산서') | (df1.sj_nm == '포괄손익계산서')) & ((df1.account_nm == '매출총이익')|(df1.account_nm == '매출총이익(손실)')|(df1.account_nm == '매출총이익 (손실)'))
            condition_6 = ((df1.sj_nm == '손익계산서') | (df1.sj_nm == '포괄손익계산서')) & \
                            ((df1.account_nm == '영업이익(손실)') | (df1.account_nm == '영업이익 (손실)') | (df1.account_nm == '영업이익'))
            condition_7 = ((df1.sj_nm == '손익계산서') | (df1.sj_nm == '포괄손익계산서')) & \
                            ((df1.account_nm == '당기순이익(손실)') | (df1.account_nm == '당기순이익') | \
                            (df1.account_nm == '분기순이익') | (df1.account_nm == '분기순이익(손실)') | (df1.account_nm == '반기순이익') | (df1.account_nm == '반기순이익(손실)') | \
                            (df1.account_nm == '분기연결순이익') | (df1.account_nm == '분기연결순이익(손실)') | (df1.account_nm == '분기연결순이익 (손실)') | \
                            (df1.account_nm == '반기연결순이익') | (df1.account_nm == '반기연결순이익(손실)') | (df1.account_nm == '반기연결순이익 (손실)') | \
                            (df1.account_nm == '당기순이익') | (df1.account_nm == '연결당기순이익(손실)') | (df1.account_nm == '연결당기순이익 (손실)')| (df1.account_nm == '연결당기순이익')|\
                            
                            (df1.account_nm == '연결분기순이익') | (df1.account_nm == '연결반기순이익')| (df1.account_nm == '연결당기순이익')|(df1.account_nm == '연결분기(당기)순이익')|(df1.account_nm == '연결반기(당기)순이익')|\
                            (df1.account_nm == '연결분기순이익(손실)') |(df1.account_nm == '분(반)기순이익(손실)')|(df1.account_nm == '분(반)기순이익')|(df1.account_nm == '순이익')|(df1.account_nm == '순이익(손실)'))
            # 현금흐름표 부분
            condition_8 = (df1.sj_nm == '현금흐름표') & ((df1.account_nm == '영업활동으로 인한 현금흐름') | (df1.account_nm == '영업활동 현금흐름') | (df1.account_nm == '영업활동현금흐름') | (df1.account_nm == '영업활동으로 인한 순현금흐름'))
            condition_9 = (df1.sj_nm == '현금흐름표') & ((df1.account_nm == '투자활동으로 인한 현금흐름') | (df1.account_nm == '투자활동 현금흐름')| (df1.account_nm == '투자활동현금흐름')| (df1.account_nm == '투자활동으로 인한 순현금흐름'))
            
            current_assets[j] = int(df1.loc[condition].iloc[0]['thstrm_amount'])
            liabilities[j] = int(df1.loc[condition_2].iloc[0]['thstrm_amount'])
            equity[j] = int(df1.loc[condition_3].iloc[0]['thstrm_amount'])
            revenue[j] = int(df1.loc[condition_4].iloc[0]['thstrm_amount'])
            grossProfit[j] = int(df1.loc[condition_5].iloc[0]['thstrm_amount'])
            income[j] = int(df1.loc[condition_6].iloc[0]['thstrm_amount'])
            net_income[j] = int(df1.loc[condition_7].iloc[0]['thstrm_amount'])
            cfo[j] = int(df1.loc[condition_8].iloc[0]['thstrm_amount'])
            cfi[j] = int(df1.loc[condition_9].iloc[0]['thstrm_amount'])
            fcf[j] = (cfo[j] - cfi[j])
                                  
           
            
            if k == '11013': # 1분기.
                path_string = str(i) + '-03-31'
            elif k == '11012': # 2분기
                path_string = str(i) + '-06-30'
            elif k == '11014': # 3분기
                path_string = str(i) + '-09-30'
            else: # 4분기. 1 ~ 3분기 데이터를 더한다음 사업보고서에서 빼야 함
                path_string = str(i) + '-12-30'
                revenue[j] = revenue[j] - (revenue[0] + revenue[1] + revenue[2])
                grossProfit[j] = grossProfit[j] - (grossProfit[0] + grossProfit[1] + grossProfit[2])
                income[j] = income[j] - (income[0] + income[1] + income[2])
                net_income[j] = net_income[j] - (net_income[0] + net_income[1] + net_income[2])
                fcf[j] = fcf[j] - (fcf[0] + fcf[1] + fcf[2])

            # 데이터프레임에 저장하는 부분
            df2.loc[path_string] = [current_assets[j], liabilities[j], equity[j],
                                revenue[j], grossProfit[j], income[j], net_income[j], cfo[j], fcf[j]]                
            df2.tail() # 데이터프레임 끝에 저장한다.
        # 너무 잦은 요청이 있을 경우 OpenDart API 측에서 IP 를 차단하니 텀을 둔다.    
        time.sleep(0.1)
#%% 
df2.drop(['1900-01-01'], inplace=True) # # 원본 dataframe 에도 영향을 끼치게끔 (inplace=True) 첫 행 drop.

df2 = df2.reset_index()
df2['ticker'] = stock_name
ddd = pd.melt(df2,id_vars = ['index','ticker'],value_vars=['유동자산_재무상태표', '부채총계_재무상태표', '자본총계_재무상태표', '매출액_손익계산서', '매출총이익_손익계산서', '영업이익_손익계산서',
                      '당기순이익_손익계산서', '영업활동현금흐름_현금흐름표',  '잉여현금흐름_현금흐름표'])

ddd[['variable','balance']] = ddd['variable'].str.split('_',expand=True)
ddd['period'] = '분기'


ddd.columns = ['update_time','ticker','label_id','value','balance_sheet','period']
ddd = ddd[['ticker','label_id','period','balance_sheet','value','update_time']]
ddd['update_time'] = pd.to_datetime(ddd['update_time'])

tuples = [tuple(x) for x in ddd.values.tolist()]


  
post = PostgresDataClass('192.168.0.3','stock','postgres','tjdwns00!')
post.insert_list(tuples, 'stock.financial_statements_korea')

  

# 이거 중간에 조건문이 너무 많아서 실패
    