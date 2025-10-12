from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
camera_latest_files = {}

@app.route('/upload', methods=['POST'])
def upload():
    camera_id = request.form.get('camera_id')
    file = request.files['file']
    person_detected = request.form.get('person_detected', 0)
    anomaly_detected = request.form.get('anomaly_detected', 'N')
    video_url = request.form.get('video_url', '')

    if not camera_id or not file:
        return jsonify({'error': 'Missing camera_id or file'}), 400

    # 이전 파일 삭제하는거
    if camera_id in camera_latest_files:
        old_filename = camera_latest_files[camera_id]
        old_path = os.path.join(UPLOAD_FOLDER, old_filename)
        if os.path.exists(old_path):
            os.remove(old_path)

    # 새로운 파일 저ㅏㅇ
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{camera_id}.png"
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    camera_latest_files[camera_id] = filename

    return jsonify({
        'camera_id': camera_id,
        'filename': filename,
        'person_detected': person_detected,
        'anomaly_detected': anomaly_detected,
        'video_url': video_url
    })

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/latest_data', methods=['GET'])
def latest_data():
    data = []
    for cam_id, filename in camera_latest_files.items():
        data.append({
            'camera_id': cam_id,
            'filename': filename,
            'person_detected': 0,
            'anomaly_detected': 'N',
            'video_url': ''
        })
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5001)