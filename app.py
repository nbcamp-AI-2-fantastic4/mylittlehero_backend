from flask import Response, Flask, redirect, url_for, render_template, jsonify, request
from flask_cors import CORS

from functions import model, common, main

app = Flask(__name__)
cors = CORS(app, resources={r'*': {'origins': '*'}})


# HTML 화면 보여주기
@app.route('/')
def home():
    resp = Response("My Little Hero")
    return resp


# token으로 회원정보 반환 API
@app.route('/user-info', methods=['GET'])
def user():
    token = request.args.get('token')
    user_info = common.get_user_from_token(token)

    return jsonify({'user_info': user_info})


# 메인 결과 보여주기 API
@app.route('/main/result', methods=['POST'])
def main_result():
    # token = request.form['token']
    # user_img = request.files['user_img']

    # 임시코드
    # 예측 결과 가져오기
    results = main.predict_img("")


    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)