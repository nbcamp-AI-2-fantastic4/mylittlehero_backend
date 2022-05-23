# 머신러닝 모델 기능 함수

from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

from tensorflow.keras.models import load_model

model = load_model('../static/models/MbileNetV2_2_2.h5')

hero_class = [
    '블랙위도우',
    '캡틴아메리카',
    '닥터스트레인지',
    '헐크',
    '아이언맨',
    '로키',
    '스파이더맨',
    '타노스']


# 사용자 이미지로 닮은 마블 캐릭터 예측
# user_img: 사용자 이미지 파일
# return: 마블 캐릭터별 예측 확률 (확률이 높은 순으로 정렬)
def predict_hero(user_img):
    # 임시코드
    img_dir = '../static/images/user/001.jpg'
    image = load_img(img_dir, target_size=(224, 224))
    input_arr = img_to_array(image)
    input_arr = np.array([input_arr])
    input_arr = input_arr / 255

    predictions = model.predict(input_arr)

    results = []
    for i in range(8):
        result = {
            'hero': hero_class[i],
            'accuracy': predictions[0][i]
        }
        results.append(result)

    results.sort(key=acc_of_result, reverse=True)

    return results


# 닮은 캐릭터 예측 결과를 정렬하기위한 key 함수
def acc_of_result(result):
    return result['accuracy']

