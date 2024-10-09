import sys
from kobert.kobert_model import kobert_model

# 감성 분석 함수
# file_path로 받은 파일의 텍스트 내용을 읽어 kobert 모델을 이용하여 감성을 분석하여 
# 7가지 감성 단어로 리턴한다.
# 7가지 감성 - 공포, 놀람, 분노, 슬픔, 중립, 행복, 혐오
def analyze_sentiment(file_path):
    # encoding utf-8로 file_path 파일을 읽기 전용으로 읽어 변수 text에 담는다.
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # kobert_model 클래스의 인스턴스 생성.
    kobert = kobert_model()
    # kobert클래스의 predict 함수에 text를 입력하여 감성을 분석하여 결과값을 반환한다.
    return kobert.predict(text)
    
# 단독 파일로 실행했을 때.  테스트용. 
if __name__ == "__main__":
    file_path = sys.argv[1]
    sentiment = analyze_sentiment(file_path)
    print(sentiment)
