from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 각 카메라별로 최신 데이터 저장하는거
latest_data = {}

@app.route('/upload', methods=['POST'])
def upload_data():
    global latest_data
    # 카메라 ID
    camera_id = request.form.get('camera_id')
    person_count = request.form.get('person_detected')
    anomaly_detected = request.form.get('anomaly_detected')
    video_url = request.form.get('video_url')

    # 필수 데이터 호ㅓㅏ인
    if 'file' not in request.files or not all([camera_id, person_count, anomaly_detected, video_url]):
        return jsonify({'error': '필수 데이터 없음'}), 400

    file = request.files['file']
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + f"{camera_id}_" + file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    # 카메라별러ㅗ 최신 데이터 저장함 (다른 카메라 데이터는 유지)
    latest_data[camera_id] = {
        'camera_id': camera_id,
        'filename': filename,
        'person_detected': person_count,
        'anomaly_detected': anomaly_detected,
        'video_url': video_url
    }

    return jsonify({'message': '업로드 성공', **latest_data[camera_id]})

@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/latest_data', methods=['GET'])
def get_latest_data():
    if not latest_data:
        return jsonify([])
    # 리스트 형태로 반환
    return jsonify(list(latest_data.values()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)