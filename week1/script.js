// ===== 產生 10 個 Content Blocks =====
const blocks = document.getElementById("blocks");
for (let i = 1; i <= 10; i++) {
  const div = document.createElement("div");
  div.className = "block";
  div.style.backgroundImage = `url("images/original.webp")`;
  div.innerHTML = `
    <span class="block__star">&#9733;</span>
    <div class="block__text">Title ${i}</div>
  `;
  blocks.appendChild(div);
}

// ===== 手機漢堡選單開關 =====
const burgerBtn = document.getElementById("burgerBtn");
const closeBtn  = document.getElementById("closeBtn");
const popupMenu = document.getElementById("popupMenu");

burgerBtn.addEventListener("click", () => popupMenu.classList.add("open"));
closeBtn.addEventListener("click", () => popupMenu.classList.remove("open"));
