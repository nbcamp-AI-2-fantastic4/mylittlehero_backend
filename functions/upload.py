# DB 구축을 위한 코드
from pymongo import MongoClient

client = MongoClient('mongodb://test:test@15.165.161.237', 27017)
db = client.dbmylittlehero


def save_user_img(user_img, email):
    extension = user_img.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{mytime}'

    save_to = f'static/images/{email}_{filename}.{extension}'
    user_img.save(save_to)

    return save_to
