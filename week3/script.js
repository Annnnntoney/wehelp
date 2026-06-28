// ===== 景點資料 URL =====
const DATA_URL_1 = "https://cwpeng.github.io/test/assignment-3-1"; // 基本資料（名稱）
const DATA_URL_2 = "https://cwpeng.github.io/test/assignment-3-2"; // 圖片資料

const BAR_COUNT = 3;    // 前 3 個景點放進 bars
const PAGE_SIZE = 10;   // 每批 10 個景點放進 blocks

let spots = [];               // 合併後的完整景點清單
let nextIndex = BAR_COUNT;    // 下一批 block 要從這個 index 開始（前 3 個給 bars）

const barsEl = document.getElementById("bars");
const blocksEl = document.getElementById("blocks");
const loadMoreBtn = document.getElementById("loadMoreBtn");

// ===== Task 3：抓取並合併兩份資料 =====
async function loadSpots() {
  const [res1, res2] = await Promise.all([fetch(DATA_URL_1), fetch(DATA_URL_2)]);
  const data1 = await res1.json();
  const data2 = await res2.json();

  // 把圖片資料用 serial 做成字典，方便對應
  const host = data2.host;
  const imageBySerial = {};
  for (const row of data2.rows) {
    const firstPic = row.pics.split(".jpg")[0] + ".jpg";   // pics 把多張圖串在一起，只取第一張
    imageBySerial[row.serial] = host + firstPic;
  }

  // 以基本資料為主，補上對應的第一張圖片
  return data1.rows.map((row) => ({
    name: row.sname,
    image: imageBySerial[row.serial] || "",
  }));
}

// ===== 建立一個 bar（全程用 createElement / appendChild，不用 innerHTML）=====
function createBar(spot) {
  const bar = document.createElement("div");
  bar.className = "bar";

  const img = document.createElement("img");
  img.src = spot.image;
  img.alt = spot.name;

  const span = document.createElement("span");
  span.textContent = spot.name;

  bar.appendChild(img);
  bar.appendChild(span);
  return bar;
}

// ===== 建立一個 content block =====
function createBlock(spot) {
  const block = document.createElement("div");
  block.className = "block";
  block.style.backgroundImage = `url("${spot.image}")`;

  const star = document.createElement("span");
  star.className = "block__star";
  star.textContent = "★";   // ★

  const text = document.createElement("div");
  text.className = "block__text";
  text.textContent = spot.name;

  block.appendChild(star);
  block.appendChild(text);
  return block;
}

// ===== Task 4：渲染下一批 10 個 block（初次載入與點按鈕共用同一段邏輯）=====
function renderNextPage() {
  const end = Math.min(nextIndex + PAGE_SIZE, spots.length);
  for (let i = nextIndex; i < end; i++) {
    blocksEl.appendChild(createBlock(spots[i]));
  }
  nextIndex = end;

  // 資料到底了就把按鈕藏起來
  if (nextIndex >= spots.length) {
    loadMoreBtn.style.display = "none";
  }
}

// ===== 頁面載入完成後才連線取資料、渲染 =====
window.addEventListener("load", async () => {
  spots = await loadSpots();

  // 前 3 個放 bars
  for (let i = 0; i < BAR_COUNT; i++) {
    barsEl.appendChild(createBar(spots[i]));
  }

  // 先渲染第一批 10 個 block
  renderNextPage();

  // 點 Load More 再渲染下一批
  loadMoreBtn.addEventListener("click", renderNextPage);
});

// ===== 手機漢堡選單開關（沿用第一週）=====
const burgerBtn = document.getElementById("burgerBtn");
const closeBtn = document.getElementById("closeBtn");
const popupMenu = document.getElementById("popupMenu");

burgerBtn.addEventListener("click", () => popupMenu.classList.add("open"));
closeBtn.addEventListener("click", () => popupMenu.classList.remove("open"));
