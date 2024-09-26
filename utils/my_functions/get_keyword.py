# 키워드 후처리 함수 호출
from utils.my_functions.process_keyword import process_keyword
import time

def get_keyword(okt, data) :
    # 형태소 분리
    pos_start_time = time.time()  # 시작 시간 기록
    pos_result = okt.pos(data)
    pos_end_time = time.time()  # 시작 시간 기록
    # print(pos_result)
    pos_execution_time = pos_end_time - pos_start_time  # 실행 시간 계산
    print(f"pos execution time: {pos_execution_time} seconds")

    # 기존 댓글 split
    splited_sentence = data.split()

    key_start_time = time.time()  # 시작 시간 기록
    # 키워드 배열 생성
    keyword = process_keyword(splited_sentence, pos_result)
    key_end_time = time.time()  # 시작 시간 기록
    key_execution_time = key_end_time - key_start_time  # 실행 시간 계산
    # print(keyword)
    print(f"keyword execution time: {key_execution_time} seconds")
    return keyword
