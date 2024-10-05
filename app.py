# flask
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
# 형태소 분석
from konlpy.tag import Okt
from utils.my_functions.process_received_data import process_received_data
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

# okt 객체 생성
okt = Okt()

# 로컬 경로에서 KcBERT 모델과 토크나이저 로드
v4_tokenizer = AutoTokenizer.from_pretrained("./models-v4")
v4_model = AutoModelForSequenceClassification.from_pretrained("./models-v4")

@app.route('/')
def say_hello():
    return "Hello Flask"

# POST 요청을 처리할 API 엔드포인트
@app.route('/receive_data', methods=['POST'])
def receive_data():

    # 받은 파일 댓글 데이터 변환
    file = request.files['file']
    data = file.read().decode('utf-8')

    # 받은 데이터 딕셔너리로 변환
    parsed_data = json.loads(data)

    # 시작시간  
    start_time = time.time()

    # log 출력
    print("pending...")

    # 반환할 데이터 가공하기
    [return_keyword, sentiment_dict] = process_received_data(parsed_data, v4_tokenizer, v4_model, okt, F)

    end_time = time.time()
    ex_time = end_time - start_time
    # 소요시간 출력
    print(f"소요시간 :{ex_time}")

    # 성공 응답 반환
    return jsonify({
        "pos" : return_keyword,
        "sentiment" : sentiment_dict
    }), 200

# 가상환경 키는법
# .\venv\Scripts\activate
# 디버깅 키는 법
# flask --debug run