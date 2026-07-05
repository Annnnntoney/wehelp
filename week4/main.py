# WeHelp 第四週：FastAPI 登入驗證系統 + 旅館查詢系統
# 執行方式：uvicorn main:app --reload
import json
import urllib.request

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# Task 4 用的旅館資料（沿用第三週 Task 1 的兩個政府 URL）
URL_CH = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
URL_EN = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="wehelp-week4-secret-key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def load_hotels():
    # 啟動時抓一次旅館資料，整理成 { 編號: {中文名, 英文名, 電話} }，之後查找 O(1)
    ch = json.loads(urllib.request.urlopen(URL_CH).read().decode("utf-8"))["list"]
    en = json.loads(urllib.request.urlopen(URL_EN).read().decode("utf-8"))["list"]

    en_name_by_id = {}
    for h in en:
        en_name_by_id[h["_id"]] = h["hotel name"]

    hotels = {}
    for h in ch:
        hotels[h["_id"]] = {
            "ch_name": h["旅宿名稱"],
            "en_name": en_name_by_id.get(h["_id"], ""),
            "phone": h["電話或手機號碼"],
        }
    return hotels


hotels = load_hotels()


# ===== Task 1：首頁 =====
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ===== Task 2 + 3：驗證端點 =====
@app.post("/login")
def login(request: Request, email: str = Form(""), password: str = Form("")):
    if email == "" or password == "":
        return RedirectResponse("/ohoh?msg=請輸入信箱和密碼", status_code=303)

    if email == "abc@abc.com" and password == "abc":
        request.session["logged_in"] = True          # Task 3：記下登入狀態
        return RedirectResponse("/member", status_code=303)

    return RedirectResponse("/ohoh?msg=信箱或密碼輸入錯誤", status_code=303)


# ===== Task 2 + 3：成功頁（每次都檢查登入狀態）=====
@app.get("/member")
def member(request: Request):
    if not request.session.get("logged_in"):          # 沒登入就強制導回首頁、不顯示內容
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("member.html", {"request": request})


# ===== Task 2：錯誤頁（從 Query String 取訊息）=====
@app.get("/ohoh")
def ohoh(request: Request, msg: str = ""):
    return templates.TemplateResponse("error.html", {"request": request, "msg": msg})


# ===== Task 3：登出端點 =====
@app.get("/logout")
def logout(request: Request):
    request.session["logged_in"] = False
    return RedirectResponse("/", status_code=303)


# ===== Task 4：旅館頁（路徑參數）=====
@app.get("/hotel/{hotel_id}")
def hotel(request: Request, hotel_id: int):
    info = hotels.get(hotel_id)                       # 查不到會是 None
    return templates.TemplateResponse("hotel.html", {"request": request, "hotel": info})
