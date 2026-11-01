# TODO REST API (Python学習用)

TODOの作成・一覧・更新・削除を行うREST APIです。FastAPIでHTTP APIを作り、SQLiteでデータを保存します。

## 起動方法

Python 3.10以上を用意し、プロジェクトのディレクトリで次を実行します。

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

PowerShellで仮想環境を有効化できない場合も、上のように `.venv\Scripts\python.exe` を直接使えます。

起動後、 http://127.0.0.1:8000/docs を開くとAPIを操作できます。SQLiteファイル `todos.db` は初回起動時に作成されます。

## API

| Method | Path | 内容 |
| --- | --- | --- |
| POST | `/todos` | `{"title":"買い物"}` で作成（204） |
| GET | `/todos` | 一覧を取得 |
| GET | `/todos?title=買` | タイトルの部分一致で検索 |
| PUT | `/todos/{id}` | タイトルや状態を変更（204、未存在なら404） |
| DELETE | `/todos/{id}` | 削除（204、未存在なら404） |

作成・更新時のJSONには、`title` に加えて `status` を指定できます。状態は `未着手`、`進行中`、`完了` のいずれかで、省略時は `未着手` です。

```json
{"title":"買い物","status":"進行中"
## 考察

今回私はcodexを利用してAIと対話しながらアプリを作りました。本格的なアプリを作ったことがなく、pythonの基本しかやったことがなかったため苦戦しました。アプリの仕組みが理解できず自分の中での最大を尽くしたものの応募している中では一番完成度が低いと思います。しかし技術面での考察はできませんが、楽しくプログラミングに触れることができました

## 起動と動作確認の手順

プロジェクトのフォルダーをPowerShellで開き、次のコマンドを順番に実行します。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload

＃＃伝えたいこと

私はまだpythonについて未熟なため今回の課題はcodexを利用しコードを作りましたまだまだできないため理解できない部分が多く苦戦しながらも今の自分の最大限の力を出しました不備等もたくさんあると思いますが熱意はあるので暖かいで見てほしいですお願いします。

