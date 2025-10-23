from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 각 카메라별 최신 데이터 저장
camera_latest_files = {}

@app.route('/upload', methods=['POST'])
def upload():
    camera_id = request.form.get('camera_id')
    file = request.files.get('file')
    person_detected = request.form.get('person_detected', '0')
    anomaly_detected = request.form.get('anomaly_detected', 'N')
    video_url = request.form.get('video_url', '')

    if not camera_id or not file:
        return jsonify({'error': 'Missing camera_id or file'}), 400

    # 이전 파일 삭제
    if camera_id in camera_latest_files:
        old_filename = camera_latest_files[camera_id]['filename']
        old_path = os.path.join(UPLOAD_FOLDER, old_filename)
        if os.path.exists(old_path):
            os.remove(old_path)

    # 새로운 파일 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{camera_id}.png"
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    # 카메라별 최신 데이터 저장
    camera_latest_files[camera_id] = {
        'filename': filename,
        'person_detected': person_detected,
        'anomaly_detected': anomaly_detected,
        'video_url': video_url
    }

    return jsonify({'message': '업로드 성공', **camera_latest_files[camera_id]})

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/latest_data', methods=['GET'])
def latest_data():
    data = []
    for cam_id, info in camera_latest_files.items():
        data.append({
            'camera_id': cam_id,
            'filename': info['filename'],
            'person_detected': info['person_detected'],
            'anomaly_detected': info['anomaly_detected'],
            'video_url': info['video_url']
        })
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)