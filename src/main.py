import speech_recognition as sr
import voicevox as vv
from chat import Chat


def record_speech(recognizer):
    with sr.Microphone() as source:
        print("話しかけてください...")
        audio = recognizer.listen(source, timeout=10)

    # 音声認識を実行する
    try:
        print("認識中...")
        text = recognizer.recognize_google(audio, language='ja-JP')
        return text
    except sr.UnknownValueError:
        print("音声が認識できませんでした。")
        return None
    except sr.RequestError as e:
        print(f"音声認識サービスへの接続エラー：{e}")
        return None


def main():
    # マイクから音声を取得するための設定
    r = sr.Recognizer()

    # チャットインスタンス
    c = Chat()

    message = c.start()
    print(message)
    # vv.say("こんにちは！ずんだもんだよ。一緒に日記を書こう！")

    while True:
        text = record_speech(r)
        if text is None:
            continue
        print(f"あなた: {text}")
        reply = c.reply(text)
        print(f"ずんだもん: {reply}")
        # vv.say(reply)


if __name__ == '__main__':
    main()
