# Task 1：從網路抓台北市旅館資料，合併中英、依行政區統計，輸出兩個 CSV
# 不使用任何第三方函式庫（只用 Python 內建 urllib / json / csv / re）
import os
import csv
import json
import urllib.request

URL_CH = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
URL_EN = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_json(url):
    # 發出請求、把回應 decode 成 UTF-8、再轉成 Python 物件
    with urllib.request.urlopen(url) as res:
        return json.loads(res.read().decode("utf-8"))


def get_district(address):
    # 從地址裡抓出行政區（例如「臺北市萬華區忠孝西路2段38號」→「萬華區」）
    # 區一定在「市」後面，所以先切「市」再切「區」
    if "市" in address and "區" in address:
        after_city = address.split("市")[1]      # 萬華區忠孝西路2段38號
        return after_city.split("區")[0] + "區"   # 萬華區
    return "其他"


def to_int(value):
    # 房間數可能是字串或空值，轉不出來就當 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def main():
    hotels_ch = fetch_json(URL_CH)["list"]
    hotels_en = fetch_json(URL_EN)["list"]

    # 把英文資料用 _id 做成字典，之後 O(1) 查找
    en_by_id = {}
    for h in hotels_en:
        en_by_id[h["_id"]] = h

    # ===== 組出 hotels.csv 的每一列，同時順便做行政區統計 =====
    rows = []
    stats = {}   # { 區名: {"hotels": 間數, "rooms": 房間數} }

    for h in hotels_ch:
        en = en_by_id.get(h["_id"], {})
        ch_name = h["旅宿名稱"]
        ch_addr = h["地址"]
        phone = h["電話或手機號碼"]
        room_count = to_int(h["房間數"])
        en_name = en.get("hotel name", "")
        en_addr = en.get("address", "")

        rows.append([ch_name, en_name, ch_addr, en_addr, phone, room_count])

        district = get_district(ch_addr)
        s = stats.setdefault(district, {"hotels": 0, "rooms": 0})
        s["hotels"] += 1
        s["rooms"] += room_count

    # ===== 寫出 hotels.csv =====
    with open(os.path.join(OUT_DIR, "hotels.csv"), "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    # ===== 寫出 districts.csv =====
    with open(os.path.join(OUT_DIR, "districts.csv"), "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for district, s in stats.items():
            writer.writerow([district, s["hotels"], s["rooms"]])

    print("完成！共", len(rows), "間旅館，", len(stats), "個行政區")


if __name__ == "__main__":
    main()
