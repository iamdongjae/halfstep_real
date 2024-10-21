# halfstep_real
## Half Step Real Version

### 1. 우분투 22.04 기준 사전 라이브러리 및 Nodejs 설치.
- sudo apt install ffmpeg python3-dev nodejs npm <br/>
- models 폴더내에 Colab에서 KOBERT를 이용하여 감성 분석한 모델 파일들을 복사한다.<br/>
  7emotions_all.tar, 7emotions_model_state_dict.pt, 7emotions_model.pt


### 2. 깃허브에서 소스를 다운로드.
- git clone https://github.com/iamdongjae/halfstep_real.git <br/>


### 3. nodejs 라이브러리 설치.
- 다운로드 받은 소스 폴더내에서 nodejs 라이브러리 (express, cors 등)를 설치한다.<br/>
- npm install <br/>


### 4. 파이썬 가상환경 설치.
- 다운로드 받은 소스 폴더내에서 파이썬 가상환경을 설치한다.<br/>
- python -m venv venv <br/>


### 5. 파이썬 가상환경.
- 가상환경 실행 : source dev 를 실행하거나 source ./venv/bin/activate 를 실행.<br/>
- 가상환경 종료 : deactivate 를 실행.<br/>


### 6. 파이썬 라이브러리 설치.
- whisper와 kobert 라이브러리는 github에서 소스를 받아와 설치하고 나머지는 req.txt를 이용하여 설치한다.<br/>
- pip install -r req.txt <br/>
- pip install git+https://github.com/openai/whisper.git <br/>
- pip install 'git+https://github.com/SKTBrain/KoBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf' <br/>

- 필수 라이브러리 설명.<br/>
  a. yt-dlp: YouTube 동영상에서 오디오 파일을 추출하는 도구.<br/>
  b. whisper: OpenAI의 Whisper 모델을 통해 음성 파일을 텍스트로 변환.<br/>
  c. google-generativeai: Google Generative AI API를 통해 텍스트를 생성.<br/>
  d. textblob: 텍스트의 감정을 분석하는 라이브러리.<br/>
  e. better-profanity: 텍스트에서 욕설을 감지하는 라이브러리.<br/>
  f. mxnet: 딥 신경망 훈련 및 배포하기 위한 라이브러리.<br/>
  g. gluonnlp: BERT 를 간단하게 로딩하기 위한 인터페이스를 제공하는 라이브러리.<br/>
  h. sentencepiece: 내부 단어 분리를 위한 라이브러리.<br/>
  i. transformers: 자연어처리, 컴퓨터비전, 오디오처리 작업에 대해 사전훈련된 모델 라이브러리.<br/>
  j. torch: 머신러닝 라이브러리.<br/>


### 7. Google API 발급 방법.
- Google Generative AI API를 사용하려면 Google Cloud에서 API 키를 발급받아야 합니다. 아래 절차에 따라 API 키를 발급받으세요.<br/>
  a. Google Cloud 계정 생성 및 로그인.<br/>
     Google Cloud에 접속하여 계정을 생성하고 로그인합니다.<br/>
     Google Cloud Console에서 새로운 프로젝트를 생성합니다.<br/>
     API 라이브러리 활성화.<br/>
  b. 새 프로젝트 생성.<br/>
     프로젝트가 생성되면, API 및 서비스 메뉴에서 Generative AI API를 검색하고 활성화합니다.<br/>
  c. API 키 생성.<br/>
     API 및 서비스 > 인증 정보로 이동하여 API 키 만들기 버튼을 클릭합니다.<br/>
     생성된 API 키는 이후 코드에서 사용될 것이므로 안전하게 보관합니다.<br/>


### 8. Google API 키 사용.
- API 키 입력 위치.<br/>
  API 키는 코드에서 Google AI와 통신하는 부분에 입력됩니다. 아래 예시 코드에서 api_key 변수를 설정하여 발급받은 API 키를 입력하세요.<br/>

- 예시 코드.<br/>
api_key = '발급받은 API 키를 여기에 입력하세요'<br/>
genai.configure(api_key=api_key)<br/>
이 설정은 summarizer.py 파일 내에서 YouTube 요약 및 감정 분석을 수행하는 곳에 위치합니다​.<br/>


### 9. Nodejs 서버 실행.
- npm start 또는 node server.js<br/>


### 10. 웹페이지 실행.
/home/iamdongjae/works/halfstep_real/public/templates/home.html <br/>



토사물 뉴스 행복
https://www.youtube.com/watch?v=Ut6PS-0gVKY

태풍 뉴스 
놀람: https://www.youtube.com/watch?v=2vQjp-Nx31s
공포: https://www.youtube.com/watch?v=rh5t-4-V2GU

아빠 아들 혼냄
혐오: https://www.youtube.com/watch?v=ot-EVhokGOY

야구 분노표출
분노: https://www.youtube.com/watch?v=MGoy5-G3Ap0
