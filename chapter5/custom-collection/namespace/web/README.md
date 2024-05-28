# Ansible URL Checker Module
## 概要
Ansible URL Checker Moduleは、指定されたURLにHTTP GETリクエストを送信し、その応答を検証するAnsibleのカスタムモジュールです。このモジュールは、特定のURLが指定された回数と間隔で正常に応答するかどうかをチェックするために使用されます。成功したリクエストと失敗したリクエストの数を返します。

## 要件
Pythonのrequestsライブラリが必要です。このライブラリがインストールされていない場合は、pip install requestsを実行してインストールしてください。
Ansible 2.9以上
### パラメーター
url: (必須) HTTP GETリクエストを送信するURL。
interval: (必須) 連続するHTTPリクエスト間の待機時間（秒）。
count: (必須) 送信するHTTP GETリクエストの総数。
モジュールの戻り値
changed: 常にFalseを返します（このモジュールは状態を変更しません）。
success_count: 成功したリクエストの数。
failure_count: 失敗したリクエストの数。
## 使用例
### 基本的な使用方法
以下のタスクは、http://example.comに対して10秒間隔で3回HTTP GETリクエストを送信し、結果を検証します。

yaml
Copy code
- name: Check URL availability
  tonoxx.web.url_checker:
    url: "http://example.com"
    interval: 10
    count: 3
  register: result

- name: Print the check result
  debug:
    msg: "Success: {{ result.success_count }}, Failure: {{ result.failure_count }}"
## インストール方法
このモジュールを使用するには、以下の手順に従ってください。

モジュールのPythonスクリプトをAnsibleのlibraryディレクトリに配置します。
必要に応じて、Ansibleの設定ファイルansible.cfgにlibraryパスを追加します。
## 注意事項
このモジュールは、requestsライブラリとの依存関係があります。
適切な環境で実行してください。
ネットワークの状態や指定されたURLのサーバーの応答によって、結果が変わる可能性があります。

