const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');
const app = express();

// CORS 설정 추가
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// YouTube 분석 요청 처리
app.post('/analyze', (req, res) => {
    const youtubeUrl = req.body.youtubeUrl;

    if (!youtubeUrl) {
        return res.status(400).json({ error: 'YouTube URL이 필요합니다.' });
    }

    // 1단계: YouTube 요약 스크립트 실행 (요약 생략)
    const summarizeScript = `python summarizer.py ${youtubeUrl}`;
    exec(summarizeScript, { encoding: 'utf-8' }, (error, stdout, stderr) => {
        if (error) {
            console.error(`요약 스크립트 오류: ${stderr}`);
            return res.status(500).json({ error: 'YouTube 텍스트 변환 중 오류가 발생했습니다.' });
        }

        // stdout에서 JSON 부분만 추출
        let jsonStartIndex = stdout.indexOf("{");
        let jsonEndIndex = stdout.lastIndexOf("}");
        let jsonString = stdout.substring(jsonStartIndex, jsonEndIndex + 1);

        let result;
        try {
            result = JSON.parse(jsonString);  // JSON 부분만 파싱
        } catch (parseError) {
            console.error(`JSON 파싱 오류: ${parseError}`);
            return res.status(500).json({ error: 'YouTube 텍스트 변환 결과 처리 중 오류가 발생했습니다.' });
        }

        const transcriptionFile = result.transcription_file;

        // 2단계: 감정 분석 스크립트 실행
        const sentimentScript = `python sentiment_analyzer.py ${transcriptionFile}`;
        exec(sentimentScript, { encoding: 'utf-8' }, (sentimentError, sentimentStdout, sentimentStderr) => {
            if (sentimentError) {
                console.error(`감정 분석 스크립트 오류: ${sentimentStderr}`);
                return res.status(500).json({ error: '감정 분석 중 오류가 발생했습니다.' });
            }

            // 3단계: 욕설 비율 분석 스크립트 실행
            const profanityScript = `python profanity_detector.py ${transcriptionFile}`;
            exec(profanityScript, { encoding: 'utf-8' }, (profanityError, profanityStdout, profanityStderr) => {
                if (profanityError) {
                    console.error(`욕설 분석 스크립트 오류: ${profanityStderr}`);
                    return res.status(500).json({ error: '욕설 분석 중 오류가 발생했습니다.' });
                }

                // 최종 결과 반환 (요약은 생략)
                res.json({
                    summary: result.summary,
                    sentiment: sentimentStdout.trim(),
                    profanity_ratio: profanityStdout.trim(),
                    transcription_file: result.transcription_file,
                    summary_file: result.summary_file
                });
            });
        });
    });
});

// 서버 시작
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

