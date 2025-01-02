import cv2
import mediapipe as mp
import urllib.request
import numpy as np
from flask import Flask, Response

# Khởi tạo Flask
app = Flask(__name__)

# Khởi tạo Mediapipe FaceMesh
face_mesh = mp.solutions.face_mesh.FaceMesh()

# Đường dẫn camera ngoài
url = 'http://172.20.10.3/cam-hi.jpg'

def generate_frames():
    while True:
        try:
            # Lấy dữ liệu ảnh từ URL
            img_resp = urllib.request.urlopen(url)
            img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

            # Kiểm tra nếu không đọc được frame
            if frame is None:
                print("Không thể đọc hình ảnh từ camera ngoài.")
                continue

            # Chuyển đổi khung hình sang RGB để xử lý với Mediapipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = face_mesh.process(rgb_frame)
            landmark_point = output.multi_face_landmarks
            frame_h, frame_w, _ = frame.shape

            # Vẽ các điểm landmark nếu có khuôn mặt được phát hiện
            if landmark_point:
                for landmarks in landmark_point:
                    for landmark in landmarks.landmark:
                        x = int(landmark.x * frame_w)
                        y = int(landmark.y * frame_h)
                        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            # Mã hóa hình ảnh thành JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Trả về hình ảnh dạng MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print(f"Lỗi: {e}")
            break

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
