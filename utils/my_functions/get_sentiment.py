# https://velog.io/@fhflwhwl5/Python-KoBERT-7%EA%B0%80%EC%A7%80-%EA%B0%90%EC%A0%95%EC%9D%98-%EB%8B%A4%EC%A4%91%EA%B0%90%EC%84%B1%EB%B6%84%EB%A5%98%EB%AA%A8%EB%8D%B8-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0
# 감성 분석
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# KcBERT 모델과 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained("beomi/KcBERT-base")
model = AutoModelForSequenceClassification.from_pretrained("beomi/KcBERT-base")

def get_sentiment(data):
    # 문장을 토큰화
    inputs = tokenizer(data, return_tensors="pt", truncation=True)

    # 모델을 사용해 감정 분석 수행
    outputs = model(**inputs)
    logits = outputs.logits

    # Softmax 함수 적용하여 확률 계산
    probs = F.softmax(logits, dim=1)
    # tensor([[긍정, 부정]], grad_fn=<SoftmaxBackward0>)

    # 확률을 백분율로 변환
    negative_prob = probs[0][0].item() * 100  # 부정일 확률
    positive_prob = probs[0][1].item() * 100  # 긍정일 확률

    return [positive_prob, negative_prob]
