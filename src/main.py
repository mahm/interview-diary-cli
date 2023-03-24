import speech_recognition as sr
from dotenv import load_dotenv
from voicevox import VoiceVox
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
    except Exception as e:
        print(f"想定外のエラー：{e}")
        return None


def main():
    # .envファイルを読み込む
    load_dotenv()

    # マイクから音声を取得するための設定
    r = sr.Recognizer()

    # ボイスボックスインスタンス
    v = VoiceVox()

    # チャットインスタンス
    c = Chat()

    message = c.start()
    print(message)
    v.say(message)

    while True:
        text = record_speech(r)
        if text is None:
            continue
        print(f"あなた: {text}")
        reply = c.reply(text)
        if c.is_finished(reply):
            last_message = """
ここまで答えてくれてありがとうなのだ。今日の日記をまとめてスラックで送信したのだ。さらばなのだ。また会おうなのだ。
            """
            print(f"ずんだもん: {last_message}")
            v.say(last_message)
            print("日記の作成処理中です。完了までしばらくこのままお待ちください...")
            c.finish(reply)
            break
        print(f"ずんだもん: {reply}")
        v.say(reply)


if __name__ == '__main__':
    main()
