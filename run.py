import subprocess
from multiprocessing import Process

def start_flask():
    subprocess.run(["python", "app/app.py"])

def start_fastapi():
    subprocess.run(["uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8888"], cwd="gaze-ai")

if __name__ == "__main__":
    flask_process = Process(target=start_flask)
    fastapi_process = Process(target=start_fastapi)

    flask_process.start()
    fastapi_process.start()

    flask_process.join()
    fastapi_process.join()

