/* Career Discovery & Matching widget (sample).
 *
 * The user picks up to three Holland (RIASEC) interest types in order, e.g. from the result of a free
 * interest test such as the O*NET Interest Profiler. The widget then lists matching job groups and
 * the programs they connect to. The mapping is a general classification, not a verdict.
 *
 * Usage:  initMatcher(document.getElementById("matcher"), { lang: "ko" });   // or "en"
 *          options: contactHref, programHref (empty string hides the button), target ("_top" inside an iframe)
 * Edit the TYPES, JOBS and PROGRAMS tables below to change the content.
 */
(function () {
  var MAX_PICKS = 3;
  var RANK_WEIGHT = [3, 2, 1];

  var TYPES = {
    R: { ko: ["현실형", "Realistic"],     d: { ko: "직접 만들고, 고치고, 다루는 일을 좋아합니다.",           en: "You like hands-on work: building, fixing and operating things." } },
    I: { ko: ["탐구형", "Investigative"], d: { ko: "궁금한 것을 분석하고 연구하는 일을 좋아합니다.",         en: "You like analysing problems and researching how things work." } },
    A: { ko: ["예술형", "Artistic"],      d: { ko: "상상하고 표현하고 창작하는 일을 좋아합니다.",             en: "You like imagining, expressing and creating." } },
    S: { ko: ["사회형", "Social"],        d: { ko: "사람을 돕고 가르치고 돌보는 일을 좋아합니다.",           en: "You like helping, teaching and caring for people." } },
    E: { ko: ["진취형", "Enterprising"],  d: { ko: "이끌고 설득하고 새로운 일을 벌이는 것을 좋아합니다.",     en: "You like leading, persuading and starting new things." } },
    C: { ko: ["관습형", "Conventional"],  d: { ko: "자료를 정리하고 규칙에 맞게 정확하게 처리하는 일을 좋아합니다.", en: "You like organising information and working accurately to clear rules." } },
  };

  // [Korean, English] job groups per interest type, in priority order.
  var JOBS = {
    R: [["공학·기술 엔지니어", "Engineering & technical"], ["의료·실험 장비 기술", "Medical & lab equipment technology"], ["건설·시설 관리", "Construction & facilities"], ["환경·자연 현장", "Environment & field work"]],
    I: [["연구원·과학자", "Research & science"], ["바이오·생명공학 연구", "Biotechnology & bioengineering research"], ["의사·의학 전문직", "Medicine & medical professions"], ["데이터·AI 분석", "Data & AI analysis"]],
    A: [["디자인·미디어", "Design & media"], ["콘텐츠·글쓰기", "Content & writing"], ["건축·공간 디자인", "Architecture & spatial design"], ["의료·과학 시각화·커뮤니케이션", "Medical & science visualisation and communication"]],
    S: [["간호·보건 돌봄", "Nursing & health care"], ["교육·상담", "Education & counselling"], ["재활·치료", "Rehabilitation & therapy"], ["사회복지", "Social work"]],
    E: [["경영·창업", "Business & entrepreneurship"], ["마케팅·영업", "Marketing & sales"], ["법률·정책", "Law & policy"], ["헬스케어·바이오 비즈니스", "Healthcare & biotech business"]],
    C: [["회계·재무", "Accounting & finance"], ["행정·사무 관리", "Administration"], ["의료정보·기록 관리", "Health information management"], ["품질·규정 관리", "Quality & regulatory affairs"]],
  };

  // How strongly each interest type points to a program category (0 = not at all).
  var PROGRAMS = [
    { name: ["Biotechnology & Bioengineering", "Biotechnology & Bioengineering"], w: { I: 3, R: 2, C: 1, E: 0.5 } },
    { name: ["Medicine, Nursing & Health Sciences", "Medicine, Nursing & Health Sciences"], w: { S: 3, I: 2, C: 1, E: 0.5, R: 0.5 } },
  ];

  var T = {
    ko: {
      pickLead: "점수가 높은 순서대로 유형을 눌러 주세요 (최대 3개). 다시 누르면 취소됩니다.",
      yourCode: "나의 유형 코드", reset: "처음부터",
      empty: "유형을 선택하면 어울리는 직업군과 프로그램이 여기에 나타납니다.",
      jobs: "어울리는 직업군", programs: "연결되는 프로그램", seminar: "직무 관련 세미나 프로그램",
      next: "다음 단계", nextText: "연관 학과의 커리어 과정과 학업을 함께 알아보고 싶다면 커리어 전환 및 학업 병행 프로그램을 문의하세요.",
      contact: "상담 문의", programsLink: "프로그램 보기", more: "3개를 고르면 더 정확하게 매칭됩니다.", group: "흥미 유형 선택",
      rank: function (n) { return n + "순위"; },
    },
    en: {
      pickLead: "Click your types in order, highest score first (up to three). Click again to remove.",
      yourCode: "Your type code", reset: "Start over",
      empty: "Pick your interest types and matching job groups and programs will appear here.",
      jobs: "Job groups that fit you", programs: "Connected programs", seminar: "Job-Related Seminar Program",
      next: "Next step", nextText: "To study the career course of a related department while you study, ask about the Career Change & Study Program.",
      contact: "Contact us", programsLink: "See programs", more: "Pick three types for a closer match.", group: "Choose interest types",
      rank: function (n) { return "#" + n; },
    },
  };

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  window.initMatcher = function (root, opts) {
    if (!root) return;
    var lang = (opts && opts.lang) === "en" ? "en" : "ko";
    var L = lang === "ko" ? 0 : 1;
    var t = T[lang];
    var o = opts || {};
    var contactHref = "contactHref" in o ? o.contactHref : "#contact";   // empty string hides the button
    var programHref = "programHref" in o ? o.programHref : "#program";
    var linkTarget = o.target || "";                                       // "_top" when embedded in an iframe
    var picked = [];

    root.textContent = "";
    root.classList.add("matcher");
    var lead = el("p", "matcher-lead", t.pickLead);
    var grid = el("div", "types");
    grid.setAttribute("role", "group");
    grid.setAttribute("aria-label", t.group);
    var codeRow = el("div", "code-row");
    var out = el("div", "match-result");
    out.setAttribute("aria-live", "polite");
    root.append(lead, grid, codeRow, out);

    var buttons = {};
    Object.keys(TYPES).forEach(function (k) {
      var ty = TYPES[k];
      var b = el("button", "type");
      b.type = "button";
      b.dataset.key = k;
      var letter = el("span", "type-letter", k);
      var body = el("span", "type-body");
      var name = el("strong", null, lang === "ko" ? ty.ko[0] + " " : ty.ko[1]);
      if (lang === "ko") name.appendChild(el("small", null, ty.ko[1]));
      body.append(name, el("span", "type-desc", ty.d[lang]));
      var rank = el("span", "type-rank");
      b.append(letter, body, rank);
      b.addEventListener("click", function () {
        var i = picked.indexOf(k);
        if (i >= 0) picked.splice(i, 1);
        else if (picked.length < MAX_PICKS) picked.push(k);
        render();
      });
      buttons[k] = b;
      grid.appendChild(b);
    });

    function scoreOf(prog) {
      return picked.reduce(function (s, k, i) { return s + RANK_WEIGHT[i] * (prog.w[k] || 0); }, 0);
    }

    function render() {
      Object.keys(buttons).forEach(function (k) {
        var b = buttons[k], i = picked.indexOf(k);
        b.setAttribute("aria-pressed", i >= 0);
        b.disabled = i < 0 && picked.length >= MAX_PICKS;
        b.querySelector(".type-rank").textContent = i >= 0 ? t.rank(i + 1) : "";
      });

      codeRow.textContent = "";
      out.textContent = "";
      if (!picked.length) {
        out.appendChild(el("p", "muted", t.empty));
        return;
      }

      codeRow.appendChild(el("span", "code-label", t.yourCode));
      codeRow.appendChild(el("strong", "code", picked.join(" · ")));
      var reset = el("button", "link-btn", t.reset);
      reset.type = "button";
      reset.addEventListener("click", function () { picked = []; render(); });
      codeRow.appendChild(reset);

      // Job groups: 3 from the first type, 2 from the second, 1 from the third.
      var quota = [3, 2, 1], seen = {}, jobs = [];
      picked.forEach(function (k, i) {
        JOBS[k].slice(0, quota[i]).forEach(function (j) {
          if (!seen[j[0]]) { seen[j[0]] = 1; jobs.push({ text: j[L], type: k }); }
        });
      });
      out.appendChild(el("h4", null, t.jobs));
      var ul = el("ul", "jobs");
      jobs.forEach(function (j) {
        var li = el("li", null, j.text);
        li.appendChild(el("span", "job-type", j.type));
        ul.appendChild(li);
      });
      out.appendChild(ul);

      // Programs: best-scoring category, plus the other if it is close.
      var scored = PROGRAMS.map(function (p) { return { p: p, s: scoreOf(p) }; }).sort(function (a, b) { return b.s - a.s; });
      var top = scored[0].s;
      out.appendChild(el("h4", null, t.programs));
      var pl = el("ul", "progs");
      scored.filter(function (x) { return top > 0 && x.s >= top * 0.75; }).forEach(function (x, idx) {
        var li = el("li");
        li.appendChild(el("strong", null, x.p.name[L]));
        li.appendChild(el("span", "muted", " · " + t.seminar));
        if (idx === 0) li.classList.add("best");
        pl.appendChild(li);
      });
      out.appendChild(pl);

      var next = el("div", "next");
      next.appendChild(el("strong", null, t.next));
      next.appendChild(el("p", null, t.nextText));
      var acts = el("div", "next-actions");
      [[contactHref, t.contact, "btn primary"], [programHref, t.programsLink, "btn"]].forEach(function (x) {
        if (!x[0]) return;
        var a = el("a", x[2], x[1]);
        a.href = x[0];
        if (linkTarget) a.target = linkTarget;
        acts.appendChild(a);
      });
      next.appendChild(acts);
      out.appendChild(next);

      if (picked.length < MAX_PICKS) out.appendChild(el("p", "note", t.more));
    }

    render();
  };
})();
