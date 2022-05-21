# 페이지 공통 사용 함수
from pymongo import MongoClient
import jwt
from datetime import datetime

client = MongoClient('mongodb://test:test@15.165.161.237', 27017)
db = client.dbmylittlehero
SECRET_KEY = 'SPARTA'


# DB에서 사용자 정보 불러오기
# email: 사용자 이메일
# return: 사용자 정보
def get_user_info(email):
    user_info = db.users.find_one({'email': email}, {'_id': False, 'pw': False})
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
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    email = payload['id']
    user_info = get_user_info(email)
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

    save_to = f'static/images/{email}_{filename}.{extension}'
    user_img.save(save_to)

    return save_to


# 사용자 이미지로 닮은 마블 캐릭터 예측
# user_img: 사용자 이미지 파일
# return: 마블 캐릭터별 예측 확률 (확률이 높은 순으로 정렬)
def predict_hero(user_img):
    # 임시코드
    results = [
        {
            'hero': '타노스',
            'accuracy': 0.665
        },
        {
            'hero': '헐크',
            'accuracy': 0.565
        },
        {
            'hero': '스파이더맨',
            'accuracy': 0.365
        },
        {
            'hero': '블랙위도우',
            'accuracy': 0.265
        },
        {
            'hero': '캡틴아메리카',
            'accuracy': 0.165
        },
        {
            'hero': '로키',
            'accuracy': 0.005
        },
        {
            'hero': '닥터스트레인지',
            'accuracy': 0.003
        },
        {
            'hero': '아이언맨',
            'accuracy': 0.465
        }
    ]

    results.sort(key=acc_of_result, reverse=True)

    return results


# 닮은 캐릭터 예측 결과를 정렬하기위한 key 함수
def acc_of_result(result):
    return result['accuracy']
