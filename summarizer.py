import yt_dlp
import whisper
import os
import google.generativeai as genai
import json
import sys
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Google API 키 설정
api_key = '실제 Google API 키를 여기에 입력하세요'  # 실제 Google API 키를 여기에 입력하세요
genai.configure(api_key=api_key)

def summarize_video(youtube_url):
    # YouTube ID 추출
    video_id = youtube_url.split('v=')[1]

    # yt-dlp 옵션 설정 (YouTube ID를 파일 이름으로 지정)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{video_id}.%(ext)s',  # YouTube ID로 파일 저장
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # 다운로드 실행
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # 다운로드된 파일 경로 출력
    downloaded_file = f"{video_id}.mp3"
    print(f"다운로드된 파일: {downloaded_file}")

    # Whisper를 사용한 텍스트 변환
    file_name = video_id + '.mp3'
    model = whisper.load_model("small")
    result = model.transcribe(file_name)
    raw_text = result['text']

    # 트랜스크립션 텍스트 파일로 저장 (UTF-8 인코딩)
    raw_file_name = video_id + '.txt'
    with open(raw_file_name, 'w', encoding='utf-8') as file:
        file.write(raw_text)
    print(f"텍스트 변환 결과 저장: {raw_file_name}")

    # Google Gemini API 사용
    prompt = '다음 영상은 유튜브 내용을 텍스트로 변환한 내용인데 너무 길어서 3줄로 요약해서 항상 한국어로 알려줘. \n 내용: \n' + raw_text

    # Google Generative AI에서 텍스트 생성 요청
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        contents=prompt, 
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
    })

    try:
        # 요약된 텍스트 추출
        summary_text = response.text  # 생성된 텍스트 추출
        # 요약된 텍스트 파일로 저장 (UTF-8 인코딩)
        summary_file_name = video_id + '_summary.txt'
        with open(summary_file_name, 'w', encoding='utf-8') as file:
            file.write(summary_text)
    except Exception as ex:
        print("{error}".format(error=ex))
        summary_text = "NA"
        summary_file_name = "NA"

    # 결과를 JSON으로 출력 (stdout) - ensure_ascii=False로 UTF-8 인코딩 보장
    output_data = {
        "summary": summary_text,
        "transcription_file": raw_file_name,
        "summary_file": summary_file_name,
        "raw_text": raw_text
    }

    # JSON 형식으로 출력할 때 ensure_ascii=False 옵션 추가
    print(json.dumps(output_data, ensure_ascii=False, indent=4))
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python summarizer.py <YouTube URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    summarize_video(youtube_url)
