#!/bin/bash
# Flask 백엔드와 Streamlit 프론트엔드를 별도 터미널 창에서 실행

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "======================================"
echo "CCTV 모니터링 시스템 시작"
echo "======================================"
echo ""
echo "Flask 백엔드와 Streamlit 프론트엔드를"
echo "각각 별도의 터미널 창에서 실행합니다."
echo ""

# Flask 백엔드를 새 터미널 창에서 실행
osascript <<END
tell application "Terminal"
    do script "cd '$PROJECT_DIR' && echo '🚀 Flask 백엔드 시작...' && echo '' && python3 app.py"
    activate
end tell
END

# 잠시 대기
sleep 1

# Streamlit 프론트엔드를 새 터미널 창에서 실행
osascript <<END
tell application "Terminal"
    do script "cd '$PROJECT_DIR' && echo '🚀 Streamlit 프론트엔드 시작...' && echo '' && python3 -m streamlit run front.py"
    activate
end tell
END

echo "✅ 두 개의 터미널 창이 열렸습니다."
echo ""
echo "Flask: http://0.0.0.0:5001"
echo "Streamlit: http://localhost:8501"
echo ""
echo "종료하려면 각 터미널 창에서 Ctrl+C를 누르세요."
