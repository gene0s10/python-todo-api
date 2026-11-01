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
{"title":"買い物","status":"進行中"}
```

## 技術を選んだ理由

- **FastAPI**: PythonでAPIを作るための道具です。URLと処理を結び付けやすく、入力内容の確認や操作画面（`/docs`）も用意しやすいため選びました。
- **SQLite**: TODOをファイルに保存できるデータベースです。別のデータベースサーバーを用意せずに始められるため、学習用の小さなアプリに向いています。利用者やデータ量が大きくなった場合は、別のデータベースへの移行を検討します。
- **標準ライブラリの `sqlite3`**: Pythonに含まれるSQLite接続機能を使い、追加のデータベース用ライブラリを減らしました。
## 学習メモ

- `app/main.py` の `TodoInput` は、受け取るJSONの形と入力制約を表します。
- `@app.get` や `@app.post` はURLとPython関数を結び付けます。
- SQLの値は `?` プレースホルダーで渡し、文字列連結でSQLを組み立てないようにしています。
- 一覧の検索にSQLiteの `LIKE` を使っています。大量データへの対応は、ページングやインデックスを学んだ後に追加します。
- SQLiteに状態欄を追加し、以前作成したTODOには「未着手」を設定します。

## 選考課題への提出について

これは学習用のたたき台です。提出前に各処理を自分で説明できるように読み解き、必要な改善やテストを自分で行ってください。問題用紙では、生成AIを使った場合は明記し、プロンプトやモデル入力コメントも提出物に記載するよう案内されています。提出時はその指示に従い、実際の利用内容を正確に記録してください。


