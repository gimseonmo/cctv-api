import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

SERVER_URL = "http://127.0.0.1:5001"

st.title("CCTV 대시보드 사이트")
st_autorefresh(interval=3000, limit=None, key="f5")

placeholder = st.empty()

try:
    response = requests.get(f"{SERVER_URL}/latest_data", timeout=3)
    if response.status_code == 200:
        cameras = response.json()  # 리스트 형태로 여러 카메라 데이터
        if cameras:
            # 카드 컨테이너 시작
            st.markdown("""
            <div style="
                display: flex;
                justify-content: center;   /* 가운데 정렬 */
                align-items: flex-start;
                flex-wrap: nowrap;         /* 한 줄로 유지 */
                gap: 20px;                 /* 카드 간 간격 */
            ">
            """, unsafe_allow_html=True)

            for cam in cameras:
                cam_id = cam.get("camera_id", "Unknown")
                filename = cam.get("filename")
                person_count = cam.get("person_detected", 0)
                anomaly = cam.get("anomaly_detected", "N")
                video_url = cam.get("video_url", "")

                time_str = "_".join(filename.split("_")[:2])
                upload_time = datetime.strptime(time_str, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

                border_color = "#ff4d4d" if anomaly.upper() == "Y" else "#ddd"
                box_shadow = "0 0 15px rgba(255,77,77,0.5)" if anomaly.upper() == "Y" else "2px 2px 5px rgba(0,0,0,0.1)"
                img_url = f"{SERVER_URL}/uploads/{filename}"

                card_html = f"""
                <div style="
                    width: 300px;
                    border: 2px solid {border_color};
                    border-radius: 10px;
                    padding: 10px;
                    box-shadow: {box_shadow};
                    text-align: center;
                ">
                    {'<a href="' + video_url + '" target="_blank">' if video_url else ''}
                        <img src="{img_url}" style="width:100%; aspect-ratio:4/3; object-fit:cover; border-radius:8px;">
                    {'</a>' if video_url else ''}
                    <div style="margin-top:10px; font-size:16px;">
                        <p><b>카메라 ID :</b> {cam_id}</p>
                        <p><b>업로드 시간 :</b> {upload_time}</p>
                        <p><b>인식된 사람 수 :</b> {person_count}</p>
                        <p><b>실신 감지 여부 :</b> {anomaly}</p>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

            # 카드 컨테이너 닫기
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            placeholder.warning("이미지가 업로드되지 않았습니다.")
    else:
        placeholder.error(f"통신 에러, {response.status_code}")

except Exception as e:
    placeholder.error(f"통신 에러, {e}")
