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

// Self-Discovery: pick interests -> suggest experiences (not a career verdict).
const INTERESTS = {
  "Research": ["University Science Lab Visit", "Research facility tour (e.g. ANSTO-style STEM day)"],
  "People": ["Healthcare Mentor Session", "School & Boarding Experience"],
  "Problem-solving": ["Design the Metro Station of the Future (mini challenge)", "Engineering Experience Day"],
  "Building": ["Infrastructure Experience (metro, dam, water)", "Urban Planning Design Challenge"],
  "Nature": ["Environment & Water Experience", "Conservation / Field Study Day"],
  "Creativity": ["Future City design project", "Media & Design Mentor Session"],
  "Technology": ["AI & Technology Mentor Session", "STEM Innovation Experience"],
  "Leadership": ["Parliament & Policy Experience", "School Leadership & Sport Day"],
};
const MAX_PICKS = 3;
const chips = document.getElementById("chips");
const result = document.getElementById("result");
const picked = new Set();

function render() {
  chips.querySelectorAll(".chip").forEach((b) => {
    const on = picked.has(b.dataset.key);
    b.setAttribute("aria-pressed", on);
    b.disabled = !on && picked.size >= MAX_PICKS;
  });
  if (!picked.size) {
    result.innerHTML = '<p class="muted">관심사를 선택하면 추천 경험이 여기에 나타납니다.</p>';
    return;
  }
  const items = [...new Set([...picked].flatMap((k) => INTERESTS[k]))];
  result.innerHTML =
    `<h4>Your profile suggests you may enjoy: ${[...picked].join(", ")}</h4>` +
    "<p>Why not experience it?</p><ul>" +
    items.map((t) => `<li>${t}</li>`).join("") +
    "</ul>";
}

Object.keys(INTERESTS).forEach((key) => {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "chip";
  b.dataset.key = key;
  b.textContent = key;
  b.addEventListener("click", () => {
    picked.has(key) ? picked.delete(key) : picked.add(key);
    render();
  });
  chips.appendChild(b);
});
render();

const CONTACT_EMAIL = "info@thescholaredu.com";

document.getElementById("contact-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const data = new FormData(e.target);
  const subject = encodeURIComponent(`[The Scholar Edu 문의] ${data.get("name")}`);
  const body = encodeURIComponent(data.get("message"));
  location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;
});
