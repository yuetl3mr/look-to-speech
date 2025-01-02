from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gaze_tracking import GazeTracking
from fastapi.responses import StreamingResponse
import cv2
import urllib.request
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gaze = GazeTracking()
url = 'http://172.20.10.3/cam-hi.jpg'  # Đường dẫn camera ngoài

# Endpoint lấy hướng nhìn
@app.get("/predict")
async def predict():
    try:
        img_resp = urllib.request.urlopen(url)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        gaze.refresh(frame)

        if gaze.is_left():
            return {"choice": 1}  # 1: Nhìn sang trái
        elif gaze.is_right():
            return {"choice": 2}  # 2: Nhìn sang phải
        elif gaze.is_center():
            return {"choice": 0}  # 0: Nhìn thẳng
        return {"choice": -1}  # -1: Không xác định
    except Exception as e:
        return {"error": str(e)}

# Endpoint luồng video MJPEG
@app.get("/video_feed")
def video_feed():
    def generate():
        while True:
            try:
                # Lấy dữ liệu từ camera ngoài
                img_resp = urllib.request.urlopen(url)
                img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
                frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

                # Mã hóa khung hình thành JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()

                # Gửi luồng MJPEG
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            except Exception as e:
                print(f"Lỗi trong luồng video: {e}")
                break

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")

# Sự kiện khởi động server
@app.on_event("startup")
async def startup_event():
    print("Server started.")

# Sự kiện tắt server
@app.on_event("shutdown")
async def shutdown_event():
    print("Server shutting down.")
