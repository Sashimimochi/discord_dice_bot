# TRPG dice bot on discord
ver.2

## 導入方法

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

## 使い方
お使いのdiscord.pyのバージョンに合わせてご利用ください。

- [ver.1](https://qiita.com/Sashimimochi/items/3cbea852f133fed5d44b)
- [ver.2](https://qiita.com/Sashimimochi/items/21fb534599407dfa4722)

## リリースノート
### ver.2

- ショートカットコマンド
- 一時的技能値補正
- 複数ダイスロール
- 対抗ロール
- シークレットダイス

### ver.1

- 任意ダイスを振る
- 自動技能判定
- ダメージ判定
- 狂気表

## 免責事項
本アプリケーションを利用する場合は、基本的に自己責任でご使用ください。