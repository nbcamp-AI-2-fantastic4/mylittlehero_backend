# 페이지 공통 사용 함수
from pymongo import MongoClient
import jwt
from datetime import datetime
from bson import ObjectId

client = MongoClient('mongodb://test:test@15.165.161.237', 27017)
db = client.dbmylittlehero
SECRET_KEY = 'SPARTA'


# DB에서 사용자 정보 불러오기
# email: 사용자 이메일
# return: 사용자 정보
def get_user_info_from_email(email):
    user_info = db.users.find_one({'email': email}, {'_id': False, 'pw': False})
    return user_info


# DB에서 사용자 정보 불러오기
# id: 사용자 object id
# return: 사용자 정보
def get_user_info_from_id(id):
    user_info = db.users.find_one({'_id': id}, {'_id': False, 'pw': False})
    return user_info


# DB에서 마블 캐릭터 정보 가져오기
# hero: 마블 캐릭터 이름
# return: 마블 캐릭터 정보
def get_hero_info(hero):
    hero_info = db.heros.find_one({'hero': hero}, {'_id': False})
    return hero_info


# 토큰으로부터 사용자 정보 추출
# token: 사용자 토큰
# return: 사용자 정보
def get_user_from_token(token):
    # 토큰값 디코딩해서 object id가 string상태로 payload에 저장
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    # string 상태에서 ObjectId 붙여서 옵젝화해야 DB에서 찾을수있다.
    # '_id': False 해야 object 에러 안남
    user_info = db.users.find_one({'_id': ObjectId(payload['id'])}, {'_id': False})
    
    # 딕셔너리 형태의 유저정보 리턴
    return user_info


# 사용자 이미지를 저장
# user_img: 사용자 이미지 파일
# email: 사용자 이메일
# return: 저장한 경로
def save_user_img(user_img, email):
    extension = user_img.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{mytime}'

    save_to = f'static/images/user/{email}_{filename}.{extension}'
    user_img.save(save_to)

    return save_to


