#!/usr/bin/env python3
"""
Flask 백엔드와 Streamlit 프론트엔드를 동시에 실행하는 런처
"""
import subprocess
import sys
import os
import time
import signal

def run_flask():
    """Flask 백엔드 실행"""
    print("🚀 Flask 백엔드 시작 중...")
    return subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

def run_streamlit():
    """Streamlit 프론트엔드 실행"""
    print("🚀 Streamlit 프론트엔드 시작 중...")
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "front.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

def main():
    print("=" * 60)
    print("CCTV 모니터링 시스템 시작")
    print("=" * 60)
    print()
    
    flask_process = None
    streamlit_process = None
    
    try:
        # Flask 백엔드 실행
        flask_process = run_flask()
        print("✅ Flask 서버가 http://0.0.0.0:5001 에서 실행 중")
        
        # Flask가 시작될 시간을 주기
        time.sleep(2)
        
        # Streamlit 프론트엔드 실행
        streamlit_process = run_streamlit()
        print("✅ Streamlit이 곧 브라우저에서 열립니다")
        print()
        print("=" * 60)
        print("종료하려면 Ctrl+C를 누르세요")
        print("=" * 60)
        
        # 프로세스들이 실행 중인지 계속 확인
        while True:
            flask_status = flask_process.poll()
            streamlit_status = streamlit_process.poll()
            
            if flask_status is not None:
                print("\n⚠️  Flask 프로세스가 종료되었습니다.")
                break
            
            if streamlit_status is not None:
                print("\n⚠️  Streamlit 프로세스가 종료되었습니다.")
                break
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n🛑 종료 신호를 받았습니다. 서버들을 종료 중...")
    
    finally:
        # 프로세스 종료
        if flask_process:
            print("Flask 서버 종료 중...")
            flask_process.terminate()
            try:
                flask_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                flask_process.kill()
        
        if streamlit_process:
            print("Streamlit 종료 중...")
            streamlit_process.terminate()
            try:
                streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                streamlit_process.kill()
        
        print("✅ 모든 서버가 종료되었습니다.")

if __name__ == "__main__":
    main()
