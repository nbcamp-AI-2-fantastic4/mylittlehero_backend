from flask import Flask, redirect, url_for, render_template, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

client = MongoClient('mongodb://test:test@15.165.161.237', 27017)
db = client.dbmylittlehero
app = Flask(__name__)
cors = CORS(app, resources={r'*': {'origins': '*'}})

# HTML 화면 보여주기
@app.route('/')
def home():
    return 'hello world'


@app.route('/result', methods=['GET'])
def result():
    # result db 전체 리스트 가져오기
    all_results = list(db.results.find({}, {'_id': False}))
    # all_list 라는 빈 리스트값을 지정
    all_list = []
    # all_results에서 for 문으로 반복 할때 필요한 정보만 가져오기
    for result in all_results:
        element = {
            'user_img': result['user_img'],
            'accuracy': result['accuracy'],
            'hero': result['hero']
        }
        # hero_info db값을 가져오기 이때 element 리스트에 hero_info 원하는 값을 넣어주기
        hero_info = db.heros.find_one({'hero': element['hero']}, {'_id': False})
        element['hero_img'] = hero_info['hero_img']
        element['description'] = hero_info['description']
        all_list.append(element)
        print(element)
    # for i in all_list:
    #     print(i)
    return jsonify({"all_result": all_list})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
