import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

SERVER_URL = "http://127.0.0.1:5001"

st.title("CCTV 대시보드 사이트")
st_autorefresh(interval=3000, limit=None, key="f5") # 3초마다 새로고침함

if "latestData" not in st.session_state:
    st.session_state["latestData"] = {}

placeholder = st.empty()

try:
    # 여기서 최신 데이터 요청함
    response = requests.get(f"{SERVER_URL}/latest_data", timeout=3)
    if response.status_code == 200:
        latestData = response.json()
        latestImageFile = latestData.get("filename")  # 최근 업로드된 파일 이름

        if latestImageFile:
            # 가장 최신의 데이터 저장
            st.session_state["latestData"] = latestData

            # 파일 이름으로 업로드 시간 정함
            timeStr = "_".join(latestImageFile.split("_")[:2])
            uploadTime = datetime.strptime(timeStr, "%Y%m%d_%H%M%S")
            formattedTime = uploadTime.strftime("%Y-%m-%d %H:%M:%S")

            # 이미지, 영상 링크, 감지 정보
            imgSrc = f"{SERVER_URL}/uploads/{latestImageFile}"
            videoLink = latestData.get("video_url")
            numPeopleDetected = latestData.get("person_detected", 0)
            alertStatus = latestData.get("anomaly_detected", "N")

            # 실신 감지 시 스티림릿 경고 표시
            if alertStatus.upper() == "Y":
                st.warning("Camera n: Fall detected! Please check immediately!")

            # 실신 감짖되면 빨간색으로 강조함
            borderColor = "#ff4d4d" if alertStatus.upper() == "Y" else "#ddd"
            boxShadow = "0 0 15px rgba(255,77,77,0.5)" if alertStatus.upper() == "Y" else "2px 2px 5px rgba(0,0,0,0.1)"

            cardHtml = f"""
            <div style="
                width: 300px;
                border: 2px solid {borderColor};
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0;
                box-shadow: {boxShadow};
                text-align: center;
                transition: 0.3s;
            ">
                {'<a href="' + videoLink + '" target="_blank">' if videoLink else ''}
                    <img src="{imgSrc}" style="width:100%; aspect-ratio:4/3; object-fit:cover; border-radius:8px;">
                {'</a>' if videoLink else ''}
                <div style="margin-top:10px; font-size:16px;">
                    <p><b>업로드 시간:</b> {formattedTime}</p>
                    <p><b>감지된 사람 수:</b> {numPeopleDetected}</p>
                    <p><b>이상 감지 여부:</b> {alertStatus}</p>
                </div>
            </div>
            """

            st.markdown(cardHtml, unsafe_allow_html=True)
        else:
            placeholder.warning("아직 업로드된 이미지가 없습니다.")
    else:
        placeholder.error(f"서버 에러: {response.status_code}")

except Exception as e:
    placeholder.error(f"통신 에러: {e}")