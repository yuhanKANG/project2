#!/usr/bin/env python
# coding: utf-8

# In[30]:


import time
loading_start = time.time() 
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from sklearn.preprocessing import MinMaxScaler

df_final = pd.read_csv('추천테이블_소분류_속성.csv',index_col='P_CODE')
df_recommend =  pd.read_csv('추천테이블_고객_상품_잠재요인.csv',index_col=0)
df_history = pd.read_csv('고객별 제품 구매여부.csv',index_col='CUSTOMER_ID')
df_product = pd.read_csv('군집화_대중성_가격.csv',index_col='P_CODE').drop(columns=['Unnamed: 0'])

df_RMF = pd.read_csv('전체_RFM등급_LABEL.csv',index_col='CUSTNO')[['F_SCORE','M_SCORE']]
df_RMF['NEW_SCORE'] = df_RMF.pipe(lambda x: (x['M_SCORE'] - x['F_SCORE'])/10)



def recommend_product_allCat(P_code,count=10):
    try:
        se_recommend = df_final.loc[P_code].sort_values(ascending=False)[1:(count+1)]
    except:
        return '존재하지 않는 상품 코드입니다.'
    return pd.DataFrame(se_recommend).join(df_product)



def recommend_product_SameCat(P_code,count=10):
    try:
        se_recommend = df_final.loc[P_code].sort_values(ascending=False)
    except:
        return '존재하지 않는 상품 코드입니다.'
    
    temp = pd.DataFrame(se_recommend).join(df_product)
    cat = df_product.loc[P_code,'nc_1']
    return temp[temp['nc_1'] == cat] [1:(count+1)]



def recommend_potential_allHistory(customer_id,count=10):
    try:
        temp = pd.DataFrame(df_recommend.loc[customer_id].sort_values(ascending=False))
    except:
        return '존재하지 않는 고객코드입니다.'
    
    return temp[:count].join(df_product)



def recommend_potential_NonHistory(customer_id,count=10):
    try:
        temp_recommend = pd.DataFrame(df_recommend.loc[customer_id].sort_values(ascending=False))
        temp_history = df_history.loc[customer_id]
    except:
        return '존재하지 않는 고객코드입니다.'
  
    return temp_recommend[temp_history][:count].join(df_product)



def recommend_potential_NonHistory_LikeProduct(customer,count=10,poten_Range = 20, product_Range = 20):
    
    li_pcode = recommend_potential_allHistory(customer,poten_Range).index
    
    df_temp = pd.DataFrame()
    for pruduct in li_pcode:
        df_temp = pd.concat([df_temp,pd.DataFrame({pruduct:recommend_product_SameCat(pruduct,product_Range).index}).T])

    history =  df_temp.applymap(lambda x: df_history.loc[customer,x])
    data = np.array(df_temp[history].fillna('')).reshape(-1)
    data = data[data != '']
        
    return pd.DataFrame(df_recommend.loc[customer,data]).join(df_name)[:count]



def recommend_potential_NonHistory_LikeProduct_vSort_poten(customer,count=10,poten_Range = 20, product_Range = 20):
    
    li_pcode = recommend_potential_allHistory(customer,poten_Range).index
    
    df_temp = pd.DataFrame()
    for pruduct in li_pcode:
        df_temp = pd.concat([df_temp,pd.DataFrame({pruduct:recommend_product_SameCat(pruduct,product_Range).index}).T])
    
    history =  df_temp.applymap(lambda x: df_history.loc[customer,x])
    data = np.array(df_temp[history].fillna('')).reshape(-1)
    data  = data[data != '']
    
    data_sort = df_recommend.loc[customer,data].sort_values(ascending=False).index
    
    return df_name.loc[data_sort][:count]
    
    
    
def recommend_potential_NonHistory_LikeProduct_vSort_price(customer,count=10,poten_Range = 20, product_Range = 20):
    
    li_pcode = recommend_potential_allHistory(customer,poten_Range).index
    
    df_temp = pd.DataFrame()
    for pruduct in li_pcode:
        df_temp = pd.concat([df_temp,pd.DataFrame({pruduct:recommend_product_SameCat(pruduct,product_Range).index}).T])
    
    history =  df_temp.applymap(lambda x: df_history.loc[customer,x])
    data = np.array(df_temp[history].fillna('')).reshape(-1)
    data  = data[data != '']
    
    data_sort = df_name.loc[data,'AVG'].sort_values(ascending=False).index

    return df_name.loc[data_sort][:count]



def newsys(customer,count=10,poten_Range = 20, product_Range_Min = 20,product_Range_MaxAddSearch = 3):
    
    li_pcode = recommend_potential_allHistory(customer,poten_Range).index
    
    for i in range(product_Range_MaxAddSearch):
        df_temp = pd.DataFrame()
        
        for pruduct in li_pcode:
            df_temp = pd.concat([df_temp,pd.DataFrame({
                pruduct:recommend_product_SameCat(pruduct,product_Range_Min + i*5).index}).T])

        history =  df_temp.applymap(lambda x: df_history.loc[customer,x])
        data = np.array(df_temp[history].fillna('')).reshape(-1)
        data  = data[data != '']
    
        if count <= len(data):
            break
    
    
    data_price = df_name.loc[data,'AVG']
    data_poten = df_recommend.loc[customer,data]


    t= pd.concat([data_price,data_poten],axis=1)
    t.columns = ['poten','price']
    
    scaler = MinMaxScaler()
    
    
    try: ## t의 크기가 0일 때 스케일러가 터짐
        a = pd.DataFrame(scaler.fit_transform(t))
        a.columns = t.columns
        a.index = t.index
        a['weight'] = a.pipe(lambda x: (a['poten']* (0.5 + (df_RMF.loc[customer,'NEW_SCORE']))) 
                                        +(a['price'] * (0.5 - df_RMF.loc[customer,'NEW_SCORE'])))
    except(ValueError):
        # 스케일러가 터질경우 poten_Range = 20, product_Range_Min = 20,product_Range_MaxAddSearch = 5 기준으로 나오는
        # 900개의 제품을 모두 구매한적이 있다는 뜻 그럴경우는 그냥 recommend_potential_allHistory 로 반환
        return recommend_potential_allHistory(customer,poten_Range)[:count]

    
    return df_name.loc[a.sort_values('weight',ascending=False)[:count].index]



print('Ready')
print('loadingTime:',time.time()-loading_start)


# In[ ]:




