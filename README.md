# look-to-speech

Look to Speech is a tool that lets you use eye movements—such as looking left, right, or straight—to select phrases or emojis from a menu, which are then read aloud through a speaker.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary libraries.

```bash
pip install requirements.txt
```

## Usage
Start AI & Webserver
```bash
python app/app.py
```

```bash
cd gaze-ai
uvicorn api:app --host 127.0.0.1 --port 8888
```

