import os
from flask import Flask, render_template

# CSV 파일 경로와 임시 파일 경로입니다.
# CSV_FILEPATH = os.path.join(os.getcwd(), __name__, 'users.csv') 
# TMP_FILEPATH = os.path.join(os.getcwd(), __name__, 'tmp.csv') 

def create_app(config=None):
    """
    create_app 은 애플리케이션 팩토리 패턴에 따른 함수입니다.
    config 파라미터는 테스트에 필요하니 변경하지는 말아주세요!
    """
    app = Flask(__name__)
    


    from a import bp
    app.register_blueprint(bp)



    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug = True)






# @app.route('/<food_cat>')
# def index_number(food_cat):
#     return 'Welcome to Index '


# @app.route('/user', methods=['GET'])
# def get_user():
    
#     user_dict=[]
#     with open(CSV_FILEPATH, newline='') as csvfile:
#       spamreader = csv.DictReader(csvfile)
#       for row in spamreader:
#           user_dict.append({'id': row['id'], 'username': row['username']})
          
#     username = request.args.get('username')

#     if username == None: 
#       return "No username given", 400
#     else: 
#       for user in user_dict: 
#         if username == user['username']:
#           return str(user['id']), 200
#     return f"User '{ username }' doesn't exist", 404