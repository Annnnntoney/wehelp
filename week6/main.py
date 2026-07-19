# WeHelp 第六週：會員系統 + 留言板（FastAPI + MySQL）
# 執行方式：uvicorn main:app --reload --port 8000
# 資料表沿用第五週建立的 website 資料庫（member、message 兩張表）
import os

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()   # 啟動時自動讀取同資料夾的 .env

# 密碼一律從環境變數讀，不寫死在程式碼裡（見 .env.example）
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "wehelp-week6-dev-key")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_conn():
    # 每次請求開一條連線，用完在 finally 關掉
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=DB_PASSWORD,
        database="website",
    )


def current_user(request):
    # 目前登入者，沒登入回 None。身分只從 session 拿，不接受前端指定
    return request.session.get("member")


# ===== Task 1：首頁（註冊表單 + 登入表單）=====
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ===== Task 1 + 4：會員頁（每次都在後端驗證登入狀態）=====
@app.get("/member")
def member(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse("/", status_code=303)   # 沒登入就導回首頁，不吐任何內容
    return templates.TemplateResponse("member.html", {"request": request, "user": user})


# ===== Task 1：錯誤頁（從 Query String 取訊息）=====
@app.get("/ohoh")
def ohoh(request: Request, msg: str = ""):
    return templates.TemplateResponse("error.html", {"request": request, "msg": msg})


# ===== Task 2：註冊 =====
@app.post("/signup")
def signup(name: str = Form(""), email: str = Form(""), password: str = Form("")):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        # SQL 一律用 %s 帶參數，不用 f-string 拼字串，避免 SQL Injection
        cursor.execute("SELECT id FROM member WHERE email = %s", (email,))
        if cursor.fetchone():
            # email 已存在，不寫入任何資料
            return RedirectResponse("/ohoh?msg=重複的電子郵件", status_code=303)

        cursor.execute(
            "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password),
        )
        conn.commit()   # 沒有 commit 資料不會真的寫進去
        return RedirectResponse("/", status_code=303)
    finally:
        cursor.close()
        conn.close()


# ===== Task 3：登入 =====
@app.post("/login")
def login(request: Request, email: str = Form(""), password: str = Form("")):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, name, email FROM member WHERE email = %s AND password = %s",
            (email, password),
        )
        row = cursor.fetchone()
        if not row:
            return RedirectResponse("/ohoh?msg=電子郵件或密碼錯誤", status_code=303)

        # 登入成功，把身分記進 session（不放密碼）
        request.session["member"] = {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
        }
        return RedirectResponse("/member", status_code=303)
    finally:
        cursor.close()
        conn.close()


# ===== Task 4：登出 =====
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


# ===== Task 5：新增留言 =====
class MessageIn(BaseModel):
    content: str


@app.post("/api/message")
def create_message(request: Request, body: MessageIn):
    user = current_user(request)
    if not user:
        return {"error": True}

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        # member_id 取自 session，不是前端傳來的，否則任何人都能冒名留言
        cursor.execute(
            "INSERT INTO message (member_id, content) VALUES (%s, %s)",
            (user["id"], body.content),
        )
        conn.commit()
        return {"ok": True}
    except Exception:
        return {"error": True}
    finally:
        cursor.close()
        conn.close()


# ===== Task 5：取得所有留言（JOIN member 取得留言者姓名）=====
@app.get("/api/message")
def get_messages(request: Request):
    user = current_user(request)
    if not user:
        return {"error": True}

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT message.id, member.name, message.content, message.member_id "
            "FROM message JOIN member ON message.member_id = member.id "
            "ORDER BY message.time DESC"
        )
        rows = cursor.fetchall()

        # self 由後端判斷，因為只有後端知道現在這個請求是誰發的
        data = []
        for row in rows:
            data.append({
                "id": row["id"],
                "name": row["name"],
                "content": row["content"],
                "self": row["member_id"] == user["id"],
            })
        return {"ok": True, "data": data}
    except Exception:
        return {"error": True}
    finally:
        cursor.close()
        conn.close()


# ===== Task 6：刪除留言（只能刪自己的）=====
@app.delete("/api/message/{message_id}")
def delete_message(request: Request, message_id: int):
    user = current_user(request)
    if not user:
        return {"error": True}

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        # AND member_id 這半句是關鍵：前端只在自己的留言旁顯示刪除鈕，那只是畫面，
        # 別人還是可以直接打這個 API。少了這個條件就能刪掉任何人的留言
        cursor.execute(
            "DELETE FROM message WHERE id = %s AND member_id = %s",
            (message_id, user["id"]),
        )
        conn.commit()

        if cursor.rowcount == 0:
            return {"error": True}   # 留言不存在、或不是這個人的
        return {"ok": True}
    except Exception:
        return {"error": True}
    finally:
        cursor.close()
        conn.close()
