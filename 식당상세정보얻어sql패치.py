import requests
import json
import time
import sqlite3

# 10:43에 시작


#여기서 레스토랑의 id를 확인하기
#50개씩 뽑아오니 start_page는 1, 51 , 101, 이런식으로 진행된다.
url = "https://worldwide-restaurants.p.rapidapi.com/search"

#start_pages = [1,51,101,151,201]
#start_pages =[i for i in range(1,26000,50)]
start_pages = [i for i in range(1,6452,50)]
url_li = []

for start_page in start_pages:
	payload = f"offset={start_page}&language=en_US&limit=50&location_id=294197&currency=USD"
	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"X-RapidAPI-Key": "0056e95ce9mshac99dd269f7065cp1045aajsnb8ebcba2180f",
		"X-RapidAPI-Host": "worldwide-restaurants.p.rapidapi.com"
	}

	response = requests.request("POST", url, data=payload, headers=headers).text
	response = json.loads(response)

	res =response['results']['data']

	
	#res에서 주소를 뽑는다
	#주소 뒷부분이 식당 id이니 이걸 문자열 메서드를 이용해서 뽑아서 리스트에 넣는다.
	for i in res:
		url_name = i['web_url'].split('com')[1][1:-5]
		url_li.append(url_name)
		
	time.sleep(60)














#code = 'Restaurant_Review-g294197-d11832256-Reviews-C_Tavern-Seoul' 세부 평점이 없다
#code = 'Restaurant_Review-g294197-d6352912-Reviews-Soigne_Restaurant-Seoul' #세부평점 존재함 얘는 가격이 달러
code2 = 'Restaurant_Review-g294197-d10751162-Reviews-Choban_Sikdang-Seoul' #얘는 가격이 w
code1 = 'Restaurant_Review-g294197-d1437932-Reviews-Pierre_Gagnaire_Seoul-Seoul'
url = "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/getRestaurantDetails"

#50개의 리스트를 가져옴
#code_list = ['Restaurant_Review-g294197-d7033774-Reviews-New_Delhi-Seoul', 'Restaurant_Review-g294197-d21127141-Reviews-Cleo-Seoul', 'Restaurant_Review-g294197-d20941492-Reviews-Privilege_Bar-Seoul', 'Restaurant_Review-g294197-d21127142-Reviews-Blind_Spot-Seoul', 'Restaurant_Review-g294197-d14090441-Reviews-853-Seoul', 'Restaurant_Review-g294197-d1978666-Reviews-Gusto_Taco-Seoul', 'Restaurant_Review-g294197-d10257443-Reviews-Jihwaja-Seoul', 'Restaurant_Review-g294197-d5972615-Reviews-Casablanca_Sandwicherie-Seoul', 'Restaurant_Review-g294197-d3200324-Reviews-Jungsik-Seoul', 'Restaurant_Review-g294197-d2170347-Reviews-Jyoti_Indian_Restaurant-Seoul', 'Restaurant_Review-g294197-d6904237-Reviews-Hemlagat-Seoul', 'Restaurant_Review-g294197-d2330577-Reviews-Braai_Republic-Seoul', 'Restaurant_Review-g294197-d4030459-Reviews-Kyochon_Chicken_Dongdaemun_1-Seoul', 'Restaurant_Review-g294197-d1371740-Reviews-Mugyodong_Bugeokukjib-Seoul', 'Restaurant_Review-g294197-d9565154-Reviews-The_Griffin_Bar-Seoul', 'Restaurant_Review-g294197-d17423735-Reviews-Jangseng_Geongangwon-Seoul', 'Restaurant_Review-g294197-d8472275-Reviews-Choigozip_Hongdae-Seoul', 'Restaurant_Review-g294197-d8953695-Reviews-Viking_s_Wharf_Lotte_World_Mall-Seoul', 'Restaurant_Review-g294197-d9171053-Reviews-Jonny_Dumpling-Seoul', 'Restaurant_Review-g294197-d3616586-Reviews-The_Park_View-Seoul', 'Restaurant_Review-g294197-d6463317-Reviews-Tavolo_24-Seoul', 'Restaurant_Review-g294197-d7118098-Reviews-Jyoti_Restaurant_Chungmuro-Seoul', 'Restaurant_Review-g294197-d11785643-Reviews-Gwanghwamun_Ichungjib-Seoul', 'Restaurant_Review-g294197-d3922956-Reviews-Jamaejip-Seoul', 'Restaurant_Review-g294197-d7105808-Reviews-Yang_Good-Seoul', 'Restaurant_Review-g294197-d7161373-Reviews-Beansbins_Myeongdong-Seoul', 'Restaurant_Review-g294197-d2230268-Reviews-Jin_Ok_Hwa_Original_Chicken_Restaurant-Seoul', 'Restaurant_Review-g294197-d2228910-Reviews-Yeonnamseo_Sikdang-Seoul', 'Restaurant_Review-g294197-d7939918-Reviews-Sulbing_Myeongdong_1st-Seoul', 'Restaurant_Review-g294197-d1196214-Reviews-Myeongdong_Kyoja_Main-Seoul', 'Restaurant_Review-g294197-d7132369-Reviews-Hongdae_Dakgalbi-Seoul', 'Restaurant_Review-g294197-d9105334-Reviews-Maple_Tree_House_Itaewon-Seoul', 'Restaurant_Review-g294197-d2476809-Reviews-Vatos_Urban_Tacos_Itaewon-Seoul', 'Restaurant_Review-g294197-d1174982-Reviews-Tosokchon_Samgyetang-Seoul', 'Restaurant_Review-g294197-d7033805-Reviews-Linus_Bama_Style_BBQ-Seoul', 'Restaurant_Review-g294197-d8135346-Reviews-Brera-Seoul', 'Restaurant_Review-g294197-d14141515-Reviews-Haedo_Sikdang-Seoul', 'Restaurant_Review-g294197-d4171321-Reviews-Brooklyn_The_Burger_Joint-Seoul', 'Restaurant_Review-g294197-d4075980-Reviews-La_Seine-Seoul', 'Restaurant_Review-g294197-d2228988-Reviews-Myeongdong_Dakhanmari_Main-Seoul', 'Restaurant_Review-g294197-d8468424-Reviews-Mingles-Seoul', 'Restaurant_Review-g294197-d2327459-Reviews-Buddha_s_Belly-Seoul', 'Restaurant_Review-g294197-d3457929-Reviews-Isaac_Toast_Myeongdong-Seoul', 'Restaurant_Review-g294197-d7042180-Reviews-Plant-Seoul', 'Restaurant_Review-g294197-d9205326-Reviews-Yukjeon_Sikdang_Main_Store-Seoul', 'Restaurant_Review-g294197-d4826338-Reviews-Brew_3_14-Seoul', 'Restaurant_Review-g294197-d21127150-Reviews-Rumpus_Room-Seoul', 'Restaurant_Review-g294197-d3568808-Reviews-Odarijip_Myeongdong-Seoul', 'Restaurant_Review-g294197-d6463321-Reviews-BLT_Steak-Seoul', 'Restaurant_Review-g294197-d3227530-Reviews-Jinmi_Sikdang-Seoul'] 

cnt = 0

for code in url_li:
	try:
		querystring = {"restaurantsId":code,"currencyCode":"USD"}

		headers = {
			"X-RapidAPI-Key": "0056e95ce9mshac99dd269f7065cp1045aajsnb8ebcba2180f",
			"X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
		}

		response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
		location = response['data']['location']


		# 여기에서는 홈페이지에서 원하는 것만 크롤링해서 변수로 저장하기
		# 식당이름과 카테고리 랭킹 그리고 음식의 카테고리
		name = location['name']
		cat  = location['ranking_category']
		food_cat = location['cuisine'][0]['name']


		# 3분야의 평점
		# 만약 없으면 평균값으로 대치하자 
		# 음식의 평점과 서비스의 평점 가격의 평점
		food_rank    = response['data']['overview']['rating']['ratingQuestions'][0]['rating']
		service_rank = response['data']['overview']['rating']['ratingQuestions'][1]['rating']
		price_rank   = response['data']['overview']['rating']['ratingQuestions'][2]['rating']



		# 최소 가격과 최대가격 
		# 가격이 $40 - $100 이런식으로 얻어지는데 이걸 문자열메서드로 가격을 나눠서 저장한다.
		# 단위가 한국 원이라도 자동으로 $로 얻어진다.
		# min_price = int(location['price'].split('-')[0][1:].strip())
		# max_price = int(location['price'].split('-')[1].strip()[1:])


		#리뷰 개수와 식당의 순위
		#식당에 쓰여진 리뷰의 개수
		#이 식당이 몇개의 식당중에 몇위인지???

		review_num = response['data']['overview']['rating']['reviewCount']
		ranking_pos = location['ranking_position']

		#평점 - 여기서 얘가 종속변수임
		#가게의 총 평점을 의미함
		#얘는 float임

		pri_rate = response['data']['overview']['rating']['primaryRating']



		#여기부터는 머신러닝에 쓰일 것은 아님
		#주소같은것


		address = location['address'] # 세부주소 
		ad_cat = location['neighborhood_info'][0]['name'] #얘는 처리가 좀 필요함 처리하면 지역카테고리로 쓰일 수 있음

		### 우편번호 postalcode의 경우에는 네이버에 검색을 하면 나오는데 여기서 split을 하고 [1]을 하면 구단위로 표시됨



		### 그리고 머신러닝이에선 여기까지만 쓰고 여기부터는 대시보드 혹은 통계분석을 위해서 여러 요소도 껴보자




		### 여기서부터 sql 실습하기

		
		conn = sqlite3.connect('pro.db')
		cur = conn.cursor()

		#cur.execute("DROP TABLE IF EXISTS tt;")
		if cnt == 0:
			cur.execute('''
			CREATE TABLE tots(
				name VARCHAR(32),
				cat VARCHAR(32),
				food_cat VARCHAR(32),
				food_rank integer,
				service_rank integer,
				price_rank integer,
				review_num integer,
				ranking_pos integer,
				ad_cat VARCHAR(32),
				pri_rate REAL,
				address VARCHAR(32)
				)'''
				)


		data = [name,cat,food_cat,food_rank,service_rank,price_rank,review_num,ranking_pos,ad_cat,pri_rate,address]

		sql = "insert into tots(name,cat,food_cat,food_rank,service_rank,price_rank,review_num,ranking_pos,ad_cat,pri_rate,address) values (?,?,?,?,?,?,?,?,?,?,?)"
		cur.execute(sql, data)
		conn.commit()
		cnt += 1
		if cnt % 30 == 0:
			time.sleep(5)
	
	except:
		pass


conn.close()
