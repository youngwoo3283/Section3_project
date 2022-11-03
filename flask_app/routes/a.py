from flask import Blueprint, request

import pickle
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split


bp = Blueprint('query', __name__, url_prefix='/query')

# @bp.route('/?cat=<cat>&foot_cat=<food_cat>&service_rank=<service_rank>&price_rank=<price_rank>&food_rank=<food_rank>&num_review=<num_review>&ranking=<ranking>')
# def index(cat,food_cat,service_rank,price_rank,food_rank,num_review,ranking):
    

#     df = pd.read_csv('save_df.csv')   
#     a = df.query('pri_rate < 4.5')
#     b = df.query('pri_rate >= 4.5')

#     a['pri_rate'] = 0
#     b['pri_rate'] = 1

#     df = pd.concat([a,b],axis = 0)
#     df_a = df.drop(columns=['name','address','ad_cat','Unnamed: 0'])
   


#     y = df_a['pri_rate']
#     X = df_a.drop(columns = 'pri_rate')

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2 ,random_state=2)
#     X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,test_size = 0.2 ,random_state=2)

#     clf_from_joblib = joblib.load('피자속피클.pkl') 


#     X_test1 = X_test.copy()

#     X_test1.iloc[0] = [cat,food_cat,int(service_rank),int(price_rank),int(food_rank),int(num_review),int(ranking)]
#     ans = clf_from_joblib.predict(X_test1)[0]



#     ### 여기서 ans가 1일때와 0일떄를 나눠서 출력하자







    
#     return str(ans)

@bp.route('/')
def get_i():
    #쿼리로 url에서 get하기
    cat = request.args.get('cat')
    food_cat = request.args.get('food_cat')
    service_rank = int(request.args.get('service_rank'))
    price_rank = int(request.args.get('price_rank'))
    food_rank  = int(request.args.get('food_rank')) 
    num_review = int(request.args.get('num_review')) 
    ranking = int(request.args.get('ranking'))

    #데이터 프레임을 가져와서 저장
    df = pd.read_csv('save_df.csv')   
    a = df.query('pri_rate < 4.5')
    b = df.query('pri_rate >= 4.5')

    a['pri_rate'] = 0
    b['pri_rate'] = 1
    df = pd.concat([a,b],axis = 0)
    df_a = df.drop(columns=['name','address','ad_cat','Unnamed: 0'])
    df.drop(columns = 'Unnamed: 0',inplace = True)
    y = df_a['pri_rate']
    X = df_a.drop(columns = 'pri_rate')


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2 ,random_state=2)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,test_size = 0.2 ,random_state=2)

    #피클을 가져와서 모델을 불러옴
    clf_from_joblib = joblib.load('피자속피클.pkl') 


    X_test1 = X_test.copy()

    #X_test1.iloc[0] = [cat,food_cat,int(service_rank),int(price_rank),int(food_rank),int(num_review),int(ranking)]
    X_test1.iloc[0] = [cat,food_cat,service_rank,price_rank,food_rank,num_review,ranking]

    ans = clf_from_joblib.predict(X_test1)[0]

    #ans가 1이면 비슷한 조건의 음식점을 이름과 카테고리 위치를 리턴해줌
    #이때 여러개 조건으로 하면 해당 조건에 부합하는 음식점이 안나올수 있으니 피쳐중요도가 높은 음식의 점수를 기준으로 하였다.
    #조건은 해당 카테고리(food_cat)과 만족여부(pri_rate) 음식의 점수(food_rank)를 기준으로 검색하도록 하였다.
    

    if ans == 1:
        temp = df[df['food_cat'] == food_cat]
        temp = temp[temp['pri_rate'] == 1]
        temp1 = temp[temp['food_rank'] >= food_rank]
        temp
        #tt = temp1.values.tolist()
        temp1 = temp1.reset_index(drop = True)
        temp1 = temp1.loc[0:4] #5개의 추천 식당을 리턴해줌 
        tt_d = temp1.to_dict('records')
        #tt_d['a_message'] = '해당 조건은 만족할 것으로 예상됩니다. 조건에 부합하는 5개의 식당입니다'
        return tt_d
    
    # 만약 ans가 0이라면?
    # 해당 조건은 만족하지 않을 것이기 때문에 푸드의 랭크가 가장 중요도가 높았고 서비스 랭크와 가게의 리뷰 개수가 그 다음으로 중요도가 높았으니 이들을 살짝 바꾼다
    # 그리고 추천식당을 리턴한다.
    if ans == 0:
        food_rank += 5
        temp = df[df['food_cat'] == food_cat]
        temp = temp[temp['pri_rate'] == 1]
        temp1 = temp[temp['food_rank'] >= food_rank]
        temp
        #tt = temp1.values.tolist()
        temp1 = temp1.reset_index(drop = True)
        temp1 = temp1.loc[0:4] #5개의 추천 식당을 리턴해줌 
        tt_d = temp1.to_dict('records')
        #tt_d['a_message'] = '해당 조건은 만족하지 못할 확률이 높은 것으로 예측됩니다 ㅠㅠ 따라서 만족할 만한 조건으로 검색한 결과입니다'
        return tt_d


