import json
import requests
# flaskモジュールからFlaskクラスをインポートする
from flask import Flask

# Flaskクラスのインスタンスを作成する
app = Flask(__name__)

# FlaskアプリのルートURL（"/"）にアクセスしたときの処理
@app.route("/")
def index():
   # OpenAIのAPIキー
   api_key = "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"

   # OpenAI APIのエンドポイント
   url = "https://api.openai.com/v1/chat/completions"

   # HTTPヘッダーの内容
   headers = {
       "Content-Type": "application/json",
       "Authorization": f"Bearer {api_key}"
   }

   # HTTPリクエストのPOSTメソッドで送信するデータ
   data = {
       "model": "gpt-4o",
       "messages": [
           {"role": "system", "content": "友人と接するように砕けた口調で返答して。"},
           {"role": "user",   "content": "夏におすすめの日本の映画を教えて。"}
       ],
       "max_tokens": 500
   }

   try:
       # OpenAI APIにHTTPリクエストを送信し、HTTPレスポンスを取得する
       response = requests.post(url, headers=headers, data=json.dumps(data))
       # HTTPステータスコードをチェックし、200番台（成功）以外の場合は例外を発生させる
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       # 例外が発生した場合、そのエラー内容を返す（ネットワークエラーなど）
       return f"HTTPリクエストエラー: {str(e)}"
   else:
       # 例外が発生しなかった場合、JSON形式のHTTPレスポンスをPythonの辞書型に変換する
       result = response.json()
       if "error" in result:
           # HTTPレスポンスにエラーが含まれていれば、そのエラー内容を返す（OpenAI API側のエラー）
           api_error_message = result["error"].get("message", "原因不明のエラー")
           return f"APIエラー: {api_error_message}"
       else:
           content = result.get("choices", [{}])[0].get("message", {}).get("content")
           if content:
               # contentが存在する場合、その内容（ChatGPTからの返答内容）を返す
               return content
           else:
               # contentが存在しない場合は何らかのエラーが発生しているため、HTTPレスポンスの内容をそのまま返す
               return f"エラー: {json.dumps(result, ensure_ascii=False)}"

# このファイルが直接実行された場合、Flaskアプリとして起動する（デフォルトではポート番号5000）
if __name__ == "__main__":
   app.run(debug=True)