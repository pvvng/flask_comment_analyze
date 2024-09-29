# flask
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
# 띄어쓰기
from pykospacing import Spacing
# 형태소 분석
from konlpy.tag import Okt
# 감정 분석 함수 호출
from utils.my_functions.get_sentiment import get_sentiment
# 키워드 배열 반환함수 호출
from utils.my_functions.get_keyword import get_keyword
# sentiment 모델 불러오기
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
# 시간 재기
import time

# flask
app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 요청 허용

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

# Spacing 객체 생성
spacing = Spacing()

# okt 객체 생성
okt = Okt()

# 로컬 경로에서 KcBERT 모델과 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained("./models-steam")
model = AutoModelForSequenceClassification.from_pretrained("./models-steam")

@app.route('/')
def say_hello():
    return "Hello Flask"

# POST 요청을 처리할 API 엔드포인트
@app.route('/receive_data', methods=['POST'])
def receive_data():
    # 받은 파일 댓글 데이터 변환
    file = request.files['file']
    data = file.read().decode('utf-8')

    # 딕셔너리로 변환
    parsed_data = json.loads(data)

    keyword_dict = {}
    sentiment_dict = {
        "positive" : 0,
        "negative" : 0,
        "neutral" : 0
    }

    # 시작시간  
    start_time = time.time()
    for comment in parsed_data :
        text = comment['text']
        like = comment['like']
        like_to_add = round(like / 10)
        # 좋아요 100 이하는 1로 변경 
        if like_to_add == 0: 
            like_to_add = 1

        # 띄어쓰기 교정
        corrected_sentence = spacing(text)

        # 키워드 분석 결과 삽입
        keyword_result = []
        keyword_result.extend(get_keyword(okt, text))
        
        for keyword in keyword_result :
            if keyword in keyword_dict:
                # 키워드가 이미 존재하면 기존 값에 추가
                keyword_dict[keyword] += like_to_add
            else:
                # 키워드가 존재하지 않으면 새로 추가
                keyword_dict[keyword] = like_to_add
        
        # 감정 분석
        sentiment_result = get_sentiment(corrected_sentence, tokenizer, model, F)
        sentiment_dict[sentiment_result] += like_to_add

        print(corrected_sentence)
        print(sentiment_result)
        print('--------------------------------------')
    # 종료시간  
    end_time = time.time()
    ex_time = end_time - start_time
    print("소요시간 :", ex_time)
    print(sentiment_dict)

    # 성공 응답 반환
    return jsonify(
        {
            "message": "Data received successfully", 
            "data": {
                "pos" : keyword_dict,
                "sentiment" : sentiment_dict
            }
        }
    ), 200

# 가상환경 키는법
# .\venv\Scripts\activate
# 디버깅 키는 법
# flask --debug run