# CCTV 실신 감지 프로젝트

## Flask 서버 역할

- **이미지 및 데이터 업로드**: 카메라에서 촬영한 이미지와 감지 정보를 서버에 저장
- **이미지 제공**: `/uploads/<filename>` 경로로 브라우저나 대시보드에서 접근 가능


### Request
| **필드** | **타입** | **설명** | **예시** |
| --- | --- | --- | --- |
| camera_id | string | 카메라 ID | CAM1 |
| file | file | 업로드 이미지 | cam1.jpg |
| person_detected | int | 감지된 사람 수 | 1 |
| anomaly_detected | string | 이상 감지 여부 (Y/N) | Y |
| video_url | string | 관련 영상 URL | http://~~~.com |

### cURL 예시
```bash
curl -X POST http://127.0.0.1:5001/upload \
  -F "camera_id=CAM1" \
  -F "file=@./cam1.jpg" \
  -F "person_detected=1" \
  -F "anomaly_detected=N" \
  -F "video_url=http://example.com/cam1.mp4"
```

### 주의
5. 주의 사항
	1.	file 필드는 정확한 로컬 경로 필요
	•	예: -F "file=@<filename>"
	2.	app.py와 front.py가 정상 동작하려면 프로젝트 루트에 uploads 폴더가 있어야 함
	3.	모든 필드 다 적어줘여,,
	4.	127.0.0.1은 로컬 서버 주소라서 외부 접속 불가 (나중에 버셀로 업로드할 생각)
    
