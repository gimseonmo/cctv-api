import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

SERVER_URL = "http://127.0.0.1:5001"

st.set_page_config(page_title="CCTV 대시보드", layout="wide")

st.session_state.clear()

st.markdown("""
<style>
body {
    background-color: #1e1e1e;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("CCTV 대시보드")
st_autorefresh(interval=3000, limit=None, key="f5")

try:
    response = requests.get(f"{SERVER_URL}/latest_data", timeout=3)
    if response.status_code == 200:
        cameras = response.json()
        if cameras:
            html = """
            <div style="
                display: flex;
                flex-wrap: wrap;              
                justify-content: center;   
                align-items: flex-start;
                gap: 20px;                  
                padding: 10px;
            ">
            """

            for cam in cameras:
                cam_id = cam.get("camera_id", "Unknown")
                filename = cam.get("filename")
                person_count = cam.get("person_detected", 0)
                anomaly = cam.get("anomaly_detected", "N")
                video_url = cam.get("video_url", "")
                time_str = "_".join(filename.split("_")[:2])
                upload_time = datetime.strptime(time_str, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

                if anomaly.upper() == "Y":st.error(f"{cam_id}에서 실신이 감지되었습니다!")

                border_color = "#ff4d4d" if anomaly.upper() == "Y" else "#555"
                box_shadow = (
                    "0 0 15px rgba(255,77,77,0.5)"
                    if anomaly.upper() == "Y"
                    else "2px 2px 5px rgba(255,255,255,0.1)"
                )
                img_url = f"{SERVER_URL}/uploads/{filename}"

                html += f"""
                <div style="
                    flex: 0 1 calc(25% - 20px);   /* 4개씩 배치 */
                    max-width: 300px;
                    min-width: 250px;
                    border: 2px solid {border_color};
                    border-radius: 10px;
                    padding: 10px;
                    box-shadow: {box_shadow};
                    background-color: #2a2a2a;
                    color: white;
                    font-family: 'Segoe UI', sans-serif;
                    text-align: center;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                "
                onmouseover="this.style.transform='scale(1.03)'; this.style.boxShadow='0 0 25px rgba(255,255,255,0.2)';"
                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='{box_shadow}';"
                >
                    {'<a href="' + video_url + '" target="_blank" style="text-decoration:none; color:white;">' if video_url else ''}
                        <img src="{img_url}" style="width:100%; aspect-ratio:4/3; object-fit:cover; border-radius:8px;">
                    {'</a>' if video_url else ''}
                    <div style="margin-top:10px; font-size:16px; line-height:1.6; text-shadow: 1px 1px 3px rgba(0,0,0,0.6);">
                        <p><b>카메라 ID :</b> {cam_id}</p>
                        <p><b>업로드 시간 :</b> {upload_time}</p>
                        <p><b>인식된 사람 수 :</b> {person_count}</p>
                        <p><b>실신 감지 여부 :</b> {anomaly}</p>
                    </div>
                </div>
                """

            html += "</div>"

            st.components.v1.html(html, height=900, scrolling=True)

        else:
            st.warning("아직 업로드된 이미지가 없습니다.")
    else:
        st.error(f"통신 에러, {response.status_code}")

except Exception as e:
    st.error(f"통신 에러, {e}")