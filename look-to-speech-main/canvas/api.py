import cv2
import urllib.request
import numpy as np
from gaze_tracking import GazeTracking
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

url = 'http://172.20.10.3/cam-hi.jpg'

gaze = GazeTracking()

@app.get("/predict")
def predict():
    """
    JSON
    """
    try:
        img_resp = urllib.request.urlopen(url)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        gaze.refresh(frame)

        if gaze.is_blinking():
            text = "Blinking"
            choice = -1
        elif gaze.is_right():
            text = "Looking right"
            choice = 2
        elif gaze.is_left():
            text = "Looking left"
            choice = 1
        elif gaze.is_center():
            text = "Looking center"
            choice = 0

        # JSON
        return {
            "status": "success",
            "text": text,
            "choice": choice
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def generate_video():
    """
    MJPEG
    """
    while True:
        try:
            img_resp = urllib.request.urlopen(url)
            img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

            gaze.refresh(frame)

            if gaze.is_blinking():
                text = "Blinking"
            elif gaze.is_right():
                text = "Looking right"
            elif gaze.is_left():
                text = "Looking left"
            elif gaze.is_center():
                text = "Looking center"

            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print(f"Lỗi: {e}")
            break

@app.get("/video_feed")
def video_feed():
    """
    MJPEG
    """
    return StreamingResponse(generate_video(), media_type="multipart/x-mixed-replace; boundary=frame")
