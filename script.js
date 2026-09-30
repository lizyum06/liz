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

// TODO: 본인 이메일 주소로 바꿔 주세요.
const CONTACT_EMAIL = "hello@example.com";

document.getElementById("contact-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const data = new FormData(e.target);
  const subject = encodeURIComponent(`${data.get("name")}님의 메시지`);
  const body = encodeURIComponent(data.get("message"));
  location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;
});
