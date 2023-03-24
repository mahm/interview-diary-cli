import hashlib
import json
import os
import tempfile
import time
from pathlib import Path

import requests
import re
import asyncio


def _text_to_array(text):
    # 句読点で分割する
    sentences = re.split('[、。！？]', text)
    # 空の要素を除去する
    sentences = [s for s in sentences if s]

    return sentences


def _play(wav_file):
    os.system(f"afplay {wav_file}")


class VoiceVox:
    HOST = "127.0.0.1"
    PORT = 50021

    def __init__(self):
        self.tmp_dir = 'tmp'
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
        else:
            self.clear_tmp_dir()

    def clear_tmp_dir(self):
        for file in os.listdir(self.tmp_dir):
            file_path = os.path.join(self.tmp_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    def say(self, text):
        asyncio.run(self._say(text))

    async def _say(self, text):
        play_queue = []
        tasks = []
        texts = _text_to_array(text)

        # 最初のテキストのみ別途処理
        first_task = asyncio.create_task(self.text_to_wav(texts[0]))
        first_wav_file = await first_task
        _play(first_wav_file)

        for elem in texts[1:]:
            task = asyncio.create_task(self.text_to_wav(elem))
            tasks.append(task)

        wav_files = await asyncio.gather(*tasks)
        for wav_file in wav_files:
            play_queue.append(wav_file)

        for wav_file in play_queue:
            _play(wav_file)

    async def text_to_wav(self, text):
        params = (
            ("text", text),
            ("speaker", 3),
        )
        audio_query = requests.post(
            f"http://{self.HOST}:{self.PORT}/audio_query",
            params=params
        )
        audio = requests.post(
            f"http://{self.HOST}:{self.PORT}/synthesis",
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(audio_query.json())
        )
        digest = hashlib.sha256(f"{text}{time.time()}".encode()).hexdigest()
        audio_file_name = f"{self.tmp_dir}/voice_{digest}.wav"
        with open(audio_file_name, "wb") as f:
            f.write(audio.content)
        return audio_file_name
