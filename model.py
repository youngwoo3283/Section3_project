##먼저 db에 있는 테이블을 csv로 내보낸다
##그리고 read_csv로 읽어서 사용한다
from cgi import print_arguments
import pandas as pd

df = pd.read_csv('save_df.csv')

## 라벨의 경우 리뷰의 특성상 대부분 후하게 주는 경향이 있어서 만족이라고 예측하였을때 불만족일 경우를 최소화 하기 위해서 일단 4점미만은 불만족(0) 이라고 표시하자 
## 아래는 query로 받아서 라벨을 바꿔준 다음에 concat으로 합쳐서 다시 만든 코드
a = df.query('pri_rate < 4.5')
b = df.query('pri_rate >= 4.5')

a['pri_rate'] = 0
b['pri_rate'] = 1

df = pd.concat([a,b],axis = 0)



#라벨값의 비율 확인
#6:4정도로 비슷하게 나온다
#print(df['pri_rate'].value_counts()) 



# 분석에 쓰일 데이터만 따로 분리하기
# 식당이름과 주소는 따로 필요없으니 나중에 대시보드에서만 적용하고 지금은 제거하자
df_a = df.drop(columns=['name','address','ad_cat'])
df_a = df_a.drop(columns = 'Unnamed: 0')

#print(df_a)

# 모델링 파트


# 데이터 라벨값의 분포를 확인하기 
# 확인하지는 않았지만 아마도 불균형할것이라고 예상됨
# 따라서 모델링시에 가중치를 줘야 할 것임

# print(df['pri_rate'].value_counts())


# 기준모델 만들기

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


base_major  = df_a['pri_rate'].mode()[0]
y_pred_base = [base_major] * len(df_a['pri_rate'])
accuracy_score1 = accuracy_score(df_a['pri_rate'], y_pred_base)
accuracy_score1

# 스코어를 확인 해보기
# 0.6257142857142857
#print(accuracy_score1)



# 훈련,검증,테스트 데이터로 나누기

y = df_a['pri_rate']
X = df_a.drop(columns = 'pri_rate')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2 ,random_state=2)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,test_size = 0.2 ,random_state=2)


# print(X_train)
# print(y_train)

# print(X_test)
# print(y_test)


### 파이프 라인 만들어서 분류모델 만들기

from category_encoders import OrdinalEncoder
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
from sklearn.pipeline import make_pipeline

from sklearn.metrics import f1_score


pipe = make_pipeline(
    OrdinalEncoder(),
    XGBClassifier(
        objective="binary:logistic",
        eval_metric="error",
        n_estimators=1000,
        random_state=2,
        n_jobs=-1,
        max_depth=7,
        learning_rate=0.1,
    ),
)

pipe.fit(X_train, y_train)


# 잘 출력된다
# 0.8135593220338982
#print(f1_score(y_val,pipe.predict(X_val)))




### 굳이 모델 튜닝을 안해도 성능이 잘나와서 그냥 테스트데이테로 마지막 스코어를 구하자




### 특성 중요도 구하기

feature_importances = list(
    zip(X_train.columns, pipe.named_steps["xgbclassifier"].feature_importances_)
)
feature_importances = sorted(feature_importances, key=lambda x: x[1], reverse=True)



#print(feature_importances)

#결과 - 푸드의 랭크가 가장 중요도가 높았고 서비스 랭크와 가게의 리뷰 개수가 그 다음으로 중요도가 높았다.



### 테스트 데이터로 확인해보기
#print(pipe.predict(X_test))


#print(pipe.predict_proba(X_test))
#print(X_test)




# 상황을 가정하고 이 상황일때 만족할지? 만족하지 못할지 예측하기

import numpy as np

### 방법
# 데이터를 입력하면 생성된 데이터에 첫번째 부분만 데이터 입력한 것으로 바꿔서 결과의 첫번쨰 값만 보여주면 되지 않을까??



#방법2 : 이걸쓰자
# x_test는 작동을 잘하니 여기에 첫번째 인덱스만 바꾼다음에 predict를 해서 첫번쨰 값만 불러오면 된다.
# 아래코드는 카테고리가 피자이고 푸드 랭크는 35 서비스는 40 가격은 40 리뷰의 숫자는 33개 가게의 순위는 100일때 예측
# 1이 리턴되어서 만족한다고 볼 수 있다.



# 리턴값 : 1
X_test1 = X_test.copy()
X_test1.iloc[0] = ['restaurant','Pizza', 35,40,40,33,100]
#print(pipe.predict(X_test1)[0])







### 여기서부터는 피클링을 이용해서 모델을 인코딩
# https://gaussian37.github.io/ml-sklearn-saving-model/
import pickle
import joblib


#dumps를 통해서 잘 저장됨
saved_model = pickle.dumps(pipe)



#여기서 다시 디코딩을 해서 predict를 해보자
#제대로 라벨값을 리턴해준다

# clf_from_pickle = pickle.loads(saved_model)
# print(clf_from_pickle.predict(X_val))



## 여기서는 피클링을 해서 파일로 만들자
## 여기서 만든 피자속피클을 플라스크로 보내서 하면된다.
## 파일로 만든 것을 다시 디코딩하기
## 잘 작동된다.

joblib.dump(pipe, '피자속피클.pkl') 


clf_from_joblib = joblib.load('피자속피클.pkl') 
#print(clf_from_joblib.predict(X_test))
