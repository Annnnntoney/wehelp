# Task 2：爬 PTT Steam 板前 3 頁，抓每篇文章的標題、推文數、發文時間，輸出 articles.csv
# 這題允許使用 BeautifulSoup 解析 HTML
import os
import csv
import time
import urllib.request
from bs4 import BeautifulSoup

BASE = "https://www.ptt.cc"
START = "/bbs/Steam/index.html"
PAGES = 3

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# PTT 有些板需要年齡確認，帶上 User-Agent 與 over18 cookie 比較保險
HEADERS = {"User-Agent": "Mozilla/5.0", "Cookie": "over18=1"}


def get_soup(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as res:
        return BeautifulSoup(res.read().decode("utf-8"), "html.parser")


def get_publish_time(article_url):
    # 進到文章內頁，從 meta 區塊找「時間」那一列
    soup = get_soup(article_url)
    for tag in soup.select(".article-metaline"):
        name = tag.select_one(".article-meta-tag")
        value = tag.select_one(".article-meta-value")
        if name and value and name.get_text() == "時間":
            return value.get_text()
    return ""   # 找不到時間就回空字串


def parse_list_page(soup):
    # 解析一個列表頁，回傳這一頁的所有文章資料
    articles = []
    for ent in soup.select(".r-ent"):
        link = ent.select_one(".title a")
        if not link:
            continue   # 沒有連結代表文章已被刪除，跳過

        title = link.get_text().strip()
        like = ent.select_one(".nrec").get_text().strip()   # 可能是空字串、數字、爆、X1
        publish_time = get_publish_time(BASE + link["href"])
        time.sleep(0.2)   # 設定0.2避免請求太密集被擋

        articles.append([title, like, publish_time])
    return articles


def main():
    rows = []
    url = BASE + START

    for _ in range(PAGES):
        soup = get_soup(url)
        rows.extend(parse_list_page(soup))

        # 找「‹ 上頁」連結當作下一個要爬的頁面（往更舊的方向）
        prev = soup.find("a", string="‹ 上頁")
        if not prev:
            break
        url = BASE + prev["href"]
        time.sleep(0.2)

    with open(os.path.join(OUT_DIR, "articles.csv"), "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    print("完成，共抓到", len(rows), "篇文章")


if __name__ == "__main__":
    main()
