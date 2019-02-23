1. Googleスプレッドシートでキャラシートを作成する
1. [Google Developers Console](https://console.developers.google.com/)でプロジェクトを作る
1. Google Sheets APIを有効化する
1. OAuth用クライアントIDを作成し、認証情報が書かれたjsonファイルをダウンロードする
1. jsonファイル内に書かれたe-mailアドレスをスプレッドシートの共有アドレスに追加する
1. discordでチャンネルにbotを作る
1. `config.json`に必要情報を書く
```
{
    "json_file": "gs.json", #google spread sheet のjsonファイルのパス
    "doc_id": "gss_id", #google spread sheet のid
    "client_id": "discord_bot_id" # discord botのid
}
```
1. trpg_bot.pyを実行する

[解説記事](https://sashimimochi.qrunch.io/entries/Uzc0aOcZBUMywxuV)

本アプリケーションを利用する場合は、基本的に自己責任でご使用ください。
