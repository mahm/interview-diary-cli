# 〇〇〇もんが日記を書いてくれる

## 環境設定

- .envファイルを作成し、以下の環境変数を設定する（Slackへの送信用）

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX
```

- [VOICEVOX](https://voicevox.hiroshiba.jp/)を使うため、スクリプトを実行する前にVOICEVOXを起動しておく
- poetryをインストールし、必要なライブラリをインストールする

```
$ pip install poetry
$ poetry install
```

## 使い方

- `run`ファイルに実行権限を追加し、実行する。

```
$ chmod +x run
$ ./run
```
