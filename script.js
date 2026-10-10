const root = document.documentElement;

try {
  const saved = localStorage.getItem("theme");
  if (saved) root.dataset.theme = saved;
} catch (e) {}

document.getElementById("theme-toggle").addEventListener("click", () => {
  const isDark =
    root.dataset.theme === "dark" ||
    (!root.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches);
  const next = isDark ? "light" : "dark";
  root.dataset.theme = next;
  try {
    localStorage.setItem("theme", next);
  } catch (e) {}
});

document.getElementById("year").textContent = new Date().getFullYear();

// Career Discovery & Matching widget (see matching.js)
if (window.initMatcher) initMatcher(document.getElementById("matcher"), { lang: "ko" });

// Contact: show the address and let people copy it (works everywhere, no mail app needed).
const emailText = document.getElementById("contact-email");
const copyStatus = document.getElementById("copy-status");
document.getElementById("copy-email").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(emailText.textContent.trim());
    copyStatus.textContent = "이메일 주소를 복사했습니다.";
  } catch (e) {
    const r = document.createRange();
    r.selectNodeContents(emailText);
    const s = getSelection();
    s.removeAllRanges();
    s.addRange(r);
    copyStatus.textContent = "주소를 선택했습니다. Ctrl+C(맥은 ⌘C)로 복사하세요.";
  }
});
