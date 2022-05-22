from datetime import datetime, timedelta
from functools import wraps
import json
from urllib import request
from flask import Flask, redirect, url_for, render_template, jsonify, request, Response, abort
from flask_cors import CORS
from pymongo import MongoClient
import hashlib
from bson import ObjectId
import jwt

app = Flask(__name__)
cors = CORS(app, resources={r'*': {'origins': '*'}})

client = MongoClient('localhost', 27017)
db = client.MyLittleHero

SECRET_KEY = 'SPARTA'

# HTML 화면 보여주기
@app.route('/')
def home():
    return 'hello world'


# DB에 회원가입 정보 저장
# email: 사용자 이메일, pw: 사용자 비밀번호, name: 사용자 이름
# return: result = 0 (이메일중복) , result = 1 (가입성공)
@app.route("/sign-up", methods=['POST'])
def sign_up():
    # 브라우저에서 받은 회원 정보를 딕셔너리 형태로 저장
    signup_info = json.loads(request.data)  # json으로 꺼내와야 딕셔너리형태로 나온다.

    email_receive = signup_info.get('email')
    pw_receive = signup_info.get('pw')
    name_receive = signup_info.get('name')

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()  # 패스워드 해싱처리

    # 이메일 중복 확인
    if db.users.find_one({'email': email_receive}):
        return jsonify({'result': 0}), 401

    else:
        doc = {
            'email': email_receive,
            'pw': pw_hash,
            'name': name_receive
        }
        # db users에 저장
        db.users.insert_one(doc)

        return jsonify({'result': 1})



# 유저 로그인 후 클라이언트에 유저 토큰 반환
# return : token = 현재 로그인 유저 토큰 반환
@app.route("/login", methods=['POST'])
def sign_in():
    signin_info = json.loads(request.data)

    id_receive = signin_info.get('email')
    pw_receive = signin_info.get('pw')

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()    # 패스워드 해싱처리

    # 가입된 정보 찾기
    find_info = db.users.find_one({
        'email': id_receive,
        'pw': pw_hash
    })

    # 가입 정보 없으면
    if find_info is None:
        return jsonify({'result': 0}), 401

    # 정보있으면 payload에 아이디와 시간 저장
    payload = {
        'id': str(find_info['_id']),   # str 안붙이면 ObjectId()까지 같이나옴
        'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
    }

    # 토큰 생성
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # print(token)

    return jsonify({'result': 1, 'token': token})   # token 반환!!!



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)