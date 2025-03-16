from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from gaze_tracking import GazeTracking
import cv2
import threading
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Biến toàn cục để lưu trữ khung hình mới nhất
latest_frame = None
frame_lock = threading.Lock()

def capture_frames():
    global latest_frame
    while True:
        success, frame = webcam.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        with frame_lock:
            latest_frame = frame.copy()
        time.sleep(0.03)  # Giảm tải CPU

def generate_frames():
    global text
    while True:
        with frame_lock:
            if latest_frame is None:
                continue
            frame = latest_frame.copy()

        gaze.refresh(frame)
        # if gaze.is_right():
        #     text = "Looking left"
        # elif gaze.is_left():
        #     text = "Looking right"
        # elif gaze.is_center():
        #     text = "Looking center"

        # cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        frame = gaze.annotated_frame()

        _, buffer = cv2.imencode(".jpg", frame)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/predict")
async def predict():
    with frame_lock:
        if latest_frame is None:
            return {"choice": -1}
        frame = latest_frame.copy()

    gaze.refresh(frame)
    if gaze.is_left():
        return {"choice": 2}
    elif gaze.is_right():
        return {"choice": 1}
    elif gaze.is_center():
        return {"choice": 0}
    return {"choice": -1}

@app.on_event("startup")
async def startup_event():
    # Bắt đầu luồng đọc khung hình từ webcam
    threading.Thread(target=capture_frames, daemon=True).start()

@app.on_event("shutdown")
async def shutdown_event():
    webcam.release()