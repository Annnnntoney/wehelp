// ===== 第六週 Task 5、6：會員頁的留言功能（前後端分離，資料靠 fetch 拿）=====
const API_URL = "/api/message";

const listEl = document.getElementById("messageList");
const formEl = document.getElementById("messageForm");
const inputEl = document.getElementById("messageInput");

// ===== Task 5：跟後端要所有留言，再交給 render 畫出來 =====
async function loadMessages() {
  const res = await fetch(API_URL);
  const result = await res.json();
  if (result.error) return;   // 沒登入或出錯就什麼都不畫
  render(result.data);
}

// ===== 建立一則留言（全程用 createElement / appendChild，不用 innerHTML）=====
function createMessage(msg) {
  const item = document.createElement("div");
  item.className = "message-item";

  const name = document.createElement("span");
  name.className = "message-item__name";
  name.textContent = msg.name + "：";

  const content = document.createElement("span");
  content.textContent = msg.content;   // 用 textContent，留言內容才不會被當成 HTML 執行

  item.appendChild(name);
  item.appendChild(content);

  // Task 6：只有自己的留言才給刪除鈕
  if (msg.self) {
    const delBtn = document.createElement("button");
    delBtn.className = "message-item__delete";
    delBtn.textContent = "x";
    delBtn.addEventListener("click", () => removeMessage(msg.id));
    item.appendChild(delBtn);
  }

  return item;
}

// ===== Task 5：把整份留言重畫一次 =====
function render(messages) {
  listEl.textContent = "";   // 先清空，不然會一直疊加

  for (const msg of messages) {
    listEl.appendChild(createMessage(msg));
  }
}

// ===== Task 5：送出新留言 =====
formEl.addEventListener("submit", async (e) => {
  e.preventDefault();   // 不攔下來整頁會重新載入

  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },   // 少了這行後端讀不到 body
    body: JSON.stringify({ content: inputEl.value }),
  });
  const result = await res.json();
  if (result.error) return;

  inputEl.value = "";
  loadMessages();   // 重抓一次，畫面才會出現剛剛那則
});

// ===== Task 6：刪除自己的留言 =====
async function removeMessage(id) {
  if (!confirm("確定要刪除這則留言嗎？")) return;   // 按取消就什麼都不做

  const res = await fetch(API_URL + "/" + id, { method: "DELETE" });
  const result = await res.json();
  if (result.error) return;

  loadMessages();   // 重畫以反映刪除結果
}

// 進到會員頁就先載入一次
loadMessages();
