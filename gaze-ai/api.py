from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from gaze_tracking import GazeTracking
import cv2

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

def generate_frames():
    while True:
        success, frame = webcam.read()
        if not success:
            break
        if gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        gaze.refresh(frame)
        frame = gaze.annotated_frame() 

        _, buffer = cv2.imencode(".jpg", frame)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/predict")
async def predict():
    _, frame = webcam.read()
    gaze.refresh(frame)

    if gaze.is_left():
        return {"choice": 1}  
    elif gaze.is_right():
        return {"choice": 2}   
    elif gaze.is_center():
        return {"choice": 0} 
    return {"choice": -1}  

@app.on_event("shutdown")
async def shutdown_event():
    webcam.release()
