import pandas as pd

df_a = pd.read_csv('tots_202211012308.csv')
df_b  = pd.read_csv('tots_202211021017.csv')


# 1050개의 데이터
# 아직 전처리는 안함
df = pd.concat([df_a,df_b],axis = 0)
df.reset_index(inplace = True)
#print(df.shape)



# 결측값은 사전에 예외처리를 해서 없음
# 주요 전처리는 food_cat에서 카디널리티를 줄이기 위한 카테고리의 통일
# Asian Cafe Italian Korean Barbecue American Japanese Chinese Bar Steakhouse French Indian Fast Food  Mexican International Seafood Pizza European
# df = df.replace({'열 이름' : 기존 값}, 변경 값) 이걸로 전처리를 할꺼임

# 카테고리수가 작은 것들을 파악한다.
# print(df['food_cat'].value_counts())

#print(df.query('food_cat == "Asian"'))



# brew pub과 pub은 bar에 이동
# 살짝 다르긴 하지만 비슷한 카테고리이니 통일;;

a= df.query('food_cat == "Brew Pub"')['food_cat'].index
b= df.query('food_cat == "Pub"')['food_cat'].index

df = df.replace({'food_cat' : 'Brew Pub'},'Bar')
df = df.replace({'food_cat' : 'Pub'},'Bar')


# Turkish  German Russian Belgian Swedish Caribbean Spanish Mediterranean Spanish Swiss Australian
# 다 European 으로 보내기

a= df.query('food_cat == "Russian"')['food_cat'].index

li = ['Turkish' , 'German', 'Russian', 'Belgian' ,'Swedish' ,'Caribbean' ,'Spanish' ,'Mediterranean' ,'Spanish' ,'Swiss','Australian']
for i in li:
    df = df.replace({'food_cat' : i},'European')
#print(df.loc[a]) # 잘 바뀐 것을 확인


# Sushi Thai Vietnamese 은 아시안으로 이동
# Asian
a= df.query('food_cat == "Thai"')['food_cat'].index

li = ['Sushi','Thai','Vietnamese']
for i in li:
    df = df.replace({'food_cat' : i},'Asian')

#print(df.loc[a])

#print(df['food_cat'].value_counts())

# Middle Eastern(중동) Lebanese(레바논) Brazilian Moroccan(모로코) Irish Uzbek
# 얘네는 따로 속하는 큰 분류가 없으니 International로 이동시킴

a= df.query('food_cat == "Brazilian"')['food_cat'].index

li = ['Middle Eastern','Lebanese','Brazilian','Moroccan','Irish','Uzbek']
for i in li:
    df = df.replace({'food_cat' : i},'International')

#print(df['food_cat'].value_counts())


df = df.replace({'food_cat' : 'Grill'},'Barbecue')

#나머지 Dining bars Street Food  Fusion Vegetarian Friendly 는 직접확인후에 바꾸자
# print(df[df['food_cat'] == 'Dining bars']) #해산물임
# print(df[df['food_cat'] == 'Street Food']) #카페
# print(df[df['food_cat'] == 'Fusion']) #스테이크
# print(df[df['food_cat'] == 'Vegetarian Friendly']) #유러피언
df = df.replace({'food_cat' : 'Dining bars'},'Seafood')
df = df.replace({'food_cat' : 'Street Food'},'Cafe')
df = df.replace({'food_cat' : 'Fusion'},'Steakhouse')
df = df.replace({'food_cat' : 'Vegetarian Friendly'},'European')


#결과 
#기존에 카테고리에 속함으로써 카디널리티를 약간 줄일 수 있게됨
#print(df['food_cat'].value_counts())

df = df.drop(columns = 'index')


#이제 다시 얘를 데이터 베이스로 보내자
#df.to_csv('./save_df.csv') 





