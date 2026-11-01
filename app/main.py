"""学習用のTODO REST API。DB操作は標準ライブラリ sqlite3 を使います。"""
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).resolve().parent.parent / "todos.db"
TodoStatus = Literal["未着手", "進行中", "完了"]


def connect_db() -> sqlite3.Connection:
    """SQLiteへ接続し、行を辞書のように扱える設定にします。"""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def now_iso() -> str:
    """タイムゾーン付きの現在時刻をISO 8601形式で返します。"""
    return datetime.now(timezone.utc).isoformat()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """起動時に、TODO保存用テーブルと状態欄を準備します。"""
    with connect_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT '未着手'
        )""")
        # 以前作ったDBにもstatus欄を追加し、既存TODOの状態は「未着手」にします。
        columns = {row["name"] for row in db.execute("PRAGMA table_info(todos)")}
        if "status" not in columns:
            db.execute("ALTER TABLE todos ADD COLUMN status TEXT NOT NULL DEFAULT '未着手'")
    yield


app = FastAPI(title="Learning TODO API", lifespan=lifespan)


class TodoInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    status: TodoStatus = "未着手"


@app.post("/todos", status_code=204)
def create_todo(todo: TodoInput) -> Response:
    """タイトルと状態を保存します。状態を省略すると「未着手」です。"""
    timestamp = now_iso()
    with connect_db() as db:
        db.execute(
            "INSERT INTO todos (title, created_at, updated_at, status) VALUES (?, ?, ?, ?)",
            (todo.title, timestamp, timestamp, todo.status),
        )
    return Response(status_code=204)


@app.get("/todos")
def list_todos(title: str | None = None) -> dict:
    """一覧を返します。titleがあると部分一致で絞り込みます。"""
    with connect_db() as db:
        if title:
            rows = db.execute(
                "SELECT id, title, created_at, updated_at, status FROM todos WHERE title LIKE ? ORDER BY id",
                (f"%{title}%",),
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT id, title, created_at, updated_at, status FROM todos ORDER BY id"
            ).fetchall()
    return {"todos": [dict(row) for row in rows]}


@app.put("/todos/{todo_id}", status_code=204)
def update_todo(todo_id: int, todo: TodoInput) -> Response:
    """指定IDのタイトル・状態・更新日時を変更します。"""
    with connect_db() as db:
        result = db.execute(
            "UPDATE todos SET title = ?, status = ?, updated_at = ? WHERE id = ?",
            (todo.title, todo.status, now_iso(), todo_id),
        )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="TODO not found")
    return Response(status_code=204)


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> Response:
    """指定IDのTODOを削除します。"""
    with connect_db() as db:
        result = db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="TODO not found")
    return Response(status_code=204)
