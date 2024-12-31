from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gaze_tracking import GazeTracking
import cv2
import asyncio

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

@app.get("/predict")
async def predict():
    _, frame = webcam.read()
    gaze.refresh(frame)

    if gaze.is_left():
        return {"choice": 1}   # 1 for looking left
    elif gaze.is_right():
        return {"choice": 2}   # 2 for looking right
    elif gaze.is_center():
        return {"choice": 0}   # 0 for looking center
    return {"choice": -1}  # Default case (if no direction detected)

async def release_webcam():
    await asyncio.sleep(5)
    webcam.release()

@app.on_event("shutdown")
async def shutdown_event():
    await release_webcam()

