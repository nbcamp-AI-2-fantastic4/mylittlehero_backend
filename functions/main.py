# 메인페이지 기능 함수
from pymongo import MongoClient

from functions import common, model

client = MongoClient('mongodb://test:test@15.165.161.237', 27017)
db = client.dbmylittlehero


# 사용자 이미지로 예측 결과 저장
# user_img: 사용자 이미지 파일
# return: result - 가장 닮은 마블 캐릭터 정보 3개
def predict_img(user_img):
    # 현재 유저 정보 가져오기
    # 임시코드
    user_info = db.users.find_one({'email': 'kimphysicsman@gmail.com'}, {'_id': False, 'pw': False})

    # 이미지 저장하기
    user_email = user_info['email']
    # dir = common.save_user_img(user_img, user_email)
    # 임시코드
    dir = 'static/images/user/001.jpg'

    # 닮은 마블 캐릭터 예측 & 상위 3개 선정
    results = model.predict_hero(user_img)[0:3]  # DB에 저장할 결과 데이터

    # DB에 저장
    for result in results:
        result['email'] = user_email
        result['user_img'] = dir

        # db.results.insert_one(result)
        # 임시코드
        print(result)

    # 클라이언트에 보내줄 결과 리스트
    view_results = []
    for i, result in enumerate(results, start=1):
        rank = i
        hero_info = common.get_hero_info(result['hero'])
        view_result = {
            'rank': rank,
            'hero': result['hero'],
            'description': hero_info['description'],
            'hero_img': hero_info['hero_img']
        }
        view_results.append(view_result)

    return view_results
