from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gaze_tracking import GazeTracking
import cv2
import asyncio
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


url = 'http://172.20.10.3/cam-hi.jpg'  

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


@app.on_event("startup")
async def startup_event():
    print("Server started.")


@app.on_event("shutdown")
async def shutdown_event():
    print("Server shutting down.")

    await asyncio.sleep(1)
