import json
import tempfile
import time
import requests
import re

HOST = "127.0.0.1"
PORT = 50021

def say(text):
    # 句読点で分割する
    sentences = re.split('[、。！？]', text)
    # 空の要素を除去する
    sentences = [s for s in sentences if s]
    for sentence in sentences:
        text_to_audio(sentence)


def text_to_audio(text):
    params = (
        ("text", text),
        ("speaker", 3),
    )
    audio_query = requests.post(
        f"http://{HOST}:{PORT}/audio_query",
        params=params
    )
    audio = requests.post(
        f"http://{HOST}:{PORT}/synthesis",
        headers={"Content-Type": "application/json"},
        params=params,
        data=json.dumps(audio_query.json())
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_file_name = f"{tmpdir}/audio_{time.time()}.wav"
        with open(audio_file_name, "wb") as f:
            f.write(audio.content)
        import os
        os.system(f"afplay {audio_file_name}")
