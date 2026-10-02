// Builds weekly Word textbooks (student + teacher) from the week-1 content.
// Quiz data is read from ../index.html so the web and Word versions stay in sync.
// Usage: node build_docx.js   (requires the `docx` npm package)
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, HeadingLevel, Footer, PageNumber,
} = require('docx');

const W = 9906; // content width in DXA (A4, 1000 margins)
const FONT = { ascii: 'Malgun Gothic', hAnsi: 'Malgun Gothic', eastAsia: 'Malgun Gothic', cs: 'Malgun Gothic' };
const BRAND = 'C2410C', BLUE = '1D4ED8', MUTED = '6B7280';
const CIRC = ['①', '②', '③', '④', '⑤'];

/* ---------- helpers ---------- */
function runs(text, o = {}) {
  return String(text).split('**').map((s, i) => new TextRun({
    text: s, bold: i % 2 === 1 || o.bold, size: o.size, color: o.color, italics: o.italics, font: FONT,
  }));
}
function p(text, o = {}) {
  return new Paragraph({
    children: runs(text, o),
    spacing: { after: o.after ?? 80, before: o.before ?? 0, line: o.line ?? 320 },
    alignment: o.align, indent: o.indent, keepNext: o.keepNext,
  });
}
function line(n = 1) {
  return Array.from({ length: n }, () => new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '999999', space: 1 } },
    spacing: { before: 200, after: 40 }, children: [],
  }));
}
function h1(text, sub) {
  const out = [new Paragraph({
    heading: HeadingLevel.HEADING_1, pageBreakBefore: true, keepNext: true,
    border: { left: { style: BorderStyle.SINGLE, size: 36, color: BRAND, space: 8 } },
    spacing: { after: 40 }, children: [new TextRun({ text, bold: true, size: 36, color: '1F2937', font: FONT })],
  })];
  if (sub) out.push(p(sub, { size: 18, color: MUTED, after: 160 }));
  return out;
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2, keepNext: true, spacing: { before: 240, after: 100 },
    children: [new TextRun({ text, bold: true, size: 26, color: '1F2937', font: FONT })],
  });
}
const thin = { style: BorderStyle.SINGLE, size: 4, color: 'D1D5DB' };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
function cell(content, width, o = {}) {
  const arr = Array.isArray(content) ? content : [content];
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders: o.borders || borders,
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
    margins: { top: 70, bottom: 70, left: 110, right: 110 }, columnSpan: o.span,
    children: arr.map((c) => (typeof c === 'string' ? p(c, { size: o.size ?? 21, after: 30, align: o.align }) : c)),
  });
}
function tbl(headers, rows, widths, o = {}) {
  const sum = widths.reduce((a, b) => a + b, 0);
  const trs = [];
  if (headers) trs.push(new TableRow({ tableHeader: true, cantSplit: true,
    children: headers.map((h, i) => cell(`**${h}**`, widths[i], { fill: 'FAF3EA', size: o.size })) }));
  rows.forEach((r) => trs.push(new TableRow({ cantSplit: true,
    children: r.map((c, i) => cell(c, widths[i], { size: o.size, align: o.center && o.center.includes(i) ? AlignmentType.CENTER : undefined })) })));
  return new Table({ width: { size: sum, type: WidthType.DXA }, columnWidths: widths, rows: trs });
}
function box(children, fill, color) {
  const b = { style: BorderStyle.SINGLE, size: 8, color };
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({
      width: { size: W, type: WidthType.DXA }, borders: { top: b, bottom: b, left: b, right: b },
      shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
      margins: { top: 100, bottom: 100, left: 160, right: 160 },
      children: children.map((c) => (typeof c === 'string' ? p(c, { size: 21, after: 50 }) : c)),
    })] })],
  });
}
const concept = (c) => box(c, 'EAF1FF', 'BFD3FF');
const tip = (c) => box(c, 'FFF7D6', 'F1DD8A');
const warn = (c) => box(c, 'FDECEC', 'F3B9B9');
const gap = () => new Paragraph({ spacing: { after: 60 }, children: [] });

/* ---------- read quiz data from the web version ---------- */
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
function toBold(s) {
  return s.replace(/<b>/g, '**').replace(/<\/b>/g, '**').replace(/<[^>]+>/g, '')
    .replace(/&lt;/g, '<').replace(/&amp;/g, '&').replace(/❓/g, '      ').replace(/\s+\)/g, ' )').trim();
}
const sets = [...html.matchAll(/<div class="quiz-set" data-title="([^"]*)">([\s\S]*?)<\/ol>\s*<\/div>/g)].map((m) => {
  const items = [...m[2].matchAll(/<li class="(q|ord)"([^>]*)>(?:<span class="stem">([\s\S]*?)<\/span>)?<\/li>/g)].map((im) => {
    const a = {}; for (const x of im[2].matchAll(/data-(\w+)="([^"]*)"/g)) a[x[1]] = x[2];
    return { type: im[1], ox: a.ox === '1', opts: (a.opts || '').split('|'), answer: a.answer, exp: a.exp || '',
      chips: a.chips ? a.chips.split('|') : [], stem: im[3] ? toBold(im[3]) : '' };
  });
  return { title: m[1], items };
});
if (sets.length !== 6) throw new Error('expected 6 quiz sets, got ' + sets.length);

function quizBlock(set, intro) {
  const out = [h2(set.title)];
  if (intro) out.push(p(intro, { size: 20, color: MUTED }));
  set.items.forEach((it, i) => {
    if (it.type === 'q') {
      out.push(p(`${i + 1}. ${it.stem}`, { keepNext: true, after: 40, before: 80 }));
      const opts = it.ox ? '(   O   /   X   )' : it.opts.map((o, j) => `${CIRC[j]} ${o}`).join('      ');
      out.push(p(opts, { indent: { left: 360 }, color: BLUE, after: 100 }));
    } else {
      out.push(p(`${i + 1}. 낱말을 순서대로 놓아 문장을 쓰세요.`, { keepNext: true, after: 40, before: 80 }));
      out.push(p('[ ' + it.chips.slice().reverse().join(' / ') + ' ]', { indent: { left: 360 }, color: BLUE, after: 0, keepNext: true }));
      out.push(...line(1));
    }
  });
  return out;
}

/* ---------- content ---------- */
function buildBody(teacher) {
  const c = [];

  // cover
  c.push(new Paragraph({ spacing: { before: 1800, after: 120 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: '재외동포 한국어 2 · 1주 차', bold: true, size: 26, color: BRAND, font: FONT })] }));
  c.push(new Paragraph({ spacing: { after: 120 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: '소리는 같고 뜻은 달라요!', bold: true, size: 64, font: FONT })] }));
  c.push(p('동음이의어 어휘 · 문장 만들기 · 문법 ‘-아/어서’ · 읽기 · 퀴즈', { align: AlignmentType.CENTER, size: 24, color: MUTED }));
  c.push(p('Heritage Korean Learners · Level 2 · Week 1 — Same Sound, Different Meaning', { align: AlignmentType.CENTER, size: 19, color: MUTED, after: 360 }));
  c.push(p('👁️  🍐  🌉  🚗', { align: AlignmentType.CENTER, size: 56, after: 360 }));
  c.push(box([
    p('**🎯 이번 주 학습 목표 (Goals)**', { size: 23 }),
    p('1. ‘눈, 배, 다리, 차’의 여러 가지 뜻을 알고 문장 속에서 구별할 수 있어요.', { size: 21 }),
    p('2. ‘-아/어서’로 **이유**를 말하고 쓸 수 있어요.', { size: 21 }),
    p('3. 배운 어휘와 문법으로 **내 문장**을 만들 수 있어요.', { size: 21 }),
    p('4. 짧은 글을 읽고 내용을 이해하고 퀴즈로 확인할 수 있어요.', { size: 21 }),
  ], 'FFFFFF', 'D1D5DB'));
  c.push(p('이름 ____________________     날짜 ____________________', { align: AlignmentType.CENTER, before: 480, color: MUTED }));
  if (teacher) c.push(p('【교사용 — 정답 및 수업 운영안 포함】', { align: AlignmentType.CENTER, bold: true, color: BRAND, before: 240 }));

  // ch1
  c.push(...h1('제1장 어휘', 'Vocabulary · 오늘의 주제: 모습이 같지만 뜻이 다른 단어 (동음이의어)'));
  c.push(concept([
    p('**📘 개념: 동음이의어란?**', { size: 23, color: BLUE }),
    p('**동음이의어(同音異義語)**는 **소리와 글자가 같지만 뜻이 다른 말**이에요. (Homonyms: same sound and spelling, different meanings)', { size: 21 }),
    p('예) **배** ➡️ 🧍 몸의 배  ·  🍐 과일 배  ·  ⛴️ 타는 배', { size: 21 }),
    p('**어떤 뜻일까요? 3단계로 찾아요!**', { size: 21 }),
    p('① 문장을 **끝까지** 읽어요.   ② 함께 쓰인 **단서 말(동사·형용사)**을 찾아요.   ③ 머릿속에 **그림**을 떠올려요.', { size: 21 }),
  ]));
  c.push(gap());
  c.push(tbl(['단어', '그림', '뜻 (Meaning)', '짝꿍 표현'], [
    ['**눈**', '👁️', '사람이나 동물의 눈 (Eye)', '눈이 아프다 · 눈이 나쁘다 · 눈을 감다'],
    ['**눈**', '❄️', '겨울에 하늘에서 내리는 하얀 눈 (Snow)', '눈이 오다/내리다 · 눈싸움 · 눈사람'],
    ['**배**', '🧍', '사람의 신체 부위 (Stomach)', '배가 고프다 · 배가 부르다 · 배가 아프다'],
    ['**배**', '🍐', '먹는 과일 (Pear)', '배를 먹다 · 배를 깎다 · 배가 달다'],
    ['**배**', '⛴️', '물 위에 떠다니는 배 (Boat)', '배를 타다 · 배가 출발하다'],
    ['**다리**', '🦵', '걷거나 뛸 때 쓰는 신체 부위 (Leg)', '다리가 아프다 · 다리를 다치다'],
    ['**다리**', '🌉', '강이나 바다를 건너는 다리 (Bridge)', '다리를 건너다 · 다리를 놓다'],
    ['**차**', '🚗', '도로를 달리는 자동차 (Car)', '차를 타다 · 차를 운전하다 · 차가 막히다'],
    ['**차**', '🍵', '따뜻하게 마시는 음료 (Tea)', '차를 마시다 · 차를 끓이다 · 유자차'],
  ], [1100, 900, 3700, 4206], { center: [0, 1] }));
  c.push(gap());
  c.push(tip([p('💡 **단서 말 모아 보기**', { size: 21 }),
    p('아프다 → 눈 / 배 / 다리   |   내리다 → 눈(Snow)   |   먹다 → 배(Pear)   |   타다 → 배(Boat) / 차(Car)   |   건너다 → 다리(Bridge)   |   마시다 → 차(Tea)', { size: 20 }),
    p('Tip: ‘타다’ is used with both 배 and 차 — look at the other words in the sentence (바다, 섬, 도로, 운전 …).', { size: 18, color: MUTED })]));
  c.push(h2('✏️ 어휘 확인 1 — 그림과 뜻 연결하기'));
  c.push(p('다음 그림에 알맞은 말을 쓰세요. (눈 · 배 · 다리 · 차)', { size: 21 }));
  c.push(tbl(['👁️', '❄️', '🍐', '⛴️', '🦵', '🌉', '🚗', '🍵'],
    [Array(8).fill('　')], [1238, 1238, 1238, 1238, 1238, 1238, 1239, 1239], { center: [0, 1, 2, 3, 4, 5, 6, 7], size: 28 }));

  // ch2
  c.push(...h1('제2장 문장 만들기', 'Sentence Building · 어휘 + 단서 말 = 문장'));
  c.push(concept([
    p('**📘 개념: 문장은 이렇게 만들어요**', { size: 23, color: BLUE }),
    p('① 무엇이/을 (눈이 · 배를 · 다리가 · 차를)  +  ② 단서 말 (아프다 · 먹다 · 건너다 · 마시다)  =  ③ 문장 (배를 먹어요.)', { size: 21 }),
    p('조사 **이/가**(주어)와 **을/를**(목적어)은 앞말과 **붙여 써요.** (Particles attach directly to the noun: 눈이, 배를.)', { size: 21 }),
  ]));
  c.push(h2('1. 소리 내어 읽어 보세요 (Read aloud)'));
  c.push(tbl(['단어', '문장', 'English'], [
    ['눈 (Eye)', '스마트폰을 너무 많이 봐서 **눈**이 아파요.', 'My eyes hurt because I look at my phone too much.'],
    ['눈 (Snow)', '밖을 보세요! 하늘에서 하얀 **눈**이 내려요.', 'Look outside! White snow is falling.'],
    ['배 (Stomach)', '밥을 많이 먹어서 **배**가 불러요.', 'I ate a lot, so I’m full.'],
    ['배 (Pear)', '식사 후에 달콤한 **배**를 먹었어요.', 'I ate a sweet pear after the meal.'],
    ['배 (Boat)', '섬에 가기 위해서 **배**를 탔어요.', 'I took a boat to go to the island.'],
    ['다리 (Leg)', '많이 걸어서 **다리**가 아파요.', 'My legs hurt because I walked a lot.'],
    ['다리 (Bridge)', '강 위의 **다리**를 건너면 학교가 있어요.', 'If you cross the bridge over the river, there is the school.'],
    ['차 (Car)', '아버지는 **차**를 운전해서 회사에 가세요.', 'My father drives a car to work.'],
    ['차 (Tea)', '추운 날에는 따뜻한 **차**를 마셔요.', 'On cold days I drink warm tea.'],
  ], [1500, 4300, 4106], { size: 20 }));
  c.push(h2('2. 짝꿍 말 연결하기 (Match the clue word)'));
  c.push(p('왼쪽 말과 어울리는 단서 말을 골라 **한 문장**으로 써 보세요.', { size: 21 }));
  c.push(tbl(['단어', '단서 말 (보기)'], [
    ['눈 (Eye)', '아프다 · 나쁘다 · 감다'], ['눈 (Snow)', '내리다 · 오다 · 쌓이다'],
    ['배 (Pear)', '먹다 · 깎다 · 달다'], ['배 (Boat)', '타다 · 출발하다'],
    ['다리 (Bridge)', '건너다 · 놓다'], ['차 (Tea)', '마시다 · 끓이다'],
  ], [3000, 6906], { size: 20 }));
  ['눈(Snow) + 내리다', '배(Boat) + 타다', '다리(Bridge) + 건너다', '차(Tea) + 마시다'].forEach((t, i) => {
    c.push(p(`${i + 1}) ${t}  ➡️`, { before: 100, after: 0, keepNext: true })); c.push(...line(1));
  });
  c.push(h2('3. 나만의 문장 만들기 (Make your own)'));
  c.push(p('내가 고른 단어: (              )   뜻: ______________', { before: 60 }));
  c.push(p('직접 만든 문장 1', { after: 0 })); c.push(...line(1));
  c.push(p('내가 고른 단어: (              )   뜻: ______________', { before: 160 }));
  c.push(p('직접 만든 문장 2', { after: 0 })); c.push(...line(1));
  c.push(p('🎨 **도전!** 한 단어의 **다른 뜻**으로 문장을 하나 더 만들어 보세요.', { before: 160, after: 0 })); c.push(...line(1));
  c.push(gap());
  c.push(tip([p('🗣️ **짝 활동** — 짝에게 문장을 읽어 주세요. 짝은 **어떤 뜻인지** 영어나 그림으로 맞혀 보세요!', { size: 21 })]));

  // ch3
  c.push(...h1('제3장 문법', 'Grammar · 오늘의 문법: -아/어서 (이유를 나타낼 때)'));
  c.push(concept([
    p('**📘 핵심 개념 — 한 장면으로 이해하기**', { size: 23, color: BLUE }),
    p('앞의 말이 뒤의 말이 일어난 **이유·원인**일 때 써요. (because / so)', { size: 21 }),
    p('🅐 원인: 비가 **와서**   ➡️   🅑 결과: 집에 있었어요.', { size: 24, align: AlignmentType.CENTER, before: 60, after: 60 }),
    p('**A-아/어서 B**  =  “A 때문에 B”  =  A. **그래서** B.', { size: 22, align: AlignmentType.CENTER }),
  ]));
  c.push(h2('① 만드는 방법: 3단계'));
  c.push(tbl(['STEP 1', 'STEP 2', 'STEP 3'], [[
    ['기본형에서 **‘-다’**를 빼요 (어간)', '가다 → **가**'],
    ['마지막 **모음**을 봐요', 'ㅏ, ㅗ 인가요?'],
    ['**-아서 / -어서 / -해서**를 붙여요'],
  ]], [3302, 3302, 3302], { size: 21 }));
  c.push(gap());
  c.push(tbl(['규칙 1: -아서', '규칙 2: -어서', '규칙 3: -해서'], [[
    ['마지막 모음이 **ㅏ, ㅗ**', '가다 → **가서**', '오다 → **와서**', '좋다 → **좋아서**'],
    ['마지막 모음이 **ㅏ, ㅗ가 아님**', '먹다 → **먹어서**', '걸리다 → **걸려서**', '막히다 → **막혀서**'],
    ['‘**하다**’로 끝남', '피곤하다 → **피곤해서**', '공부하다 → **공부해서**'],
  ]], [3302, 3302, 3302], { size: 21 }));
  c.push(h2('② 변화표 (Conjugation table)'));
  c.push(tbl(['기본형', '어간', '+ -아/어서', '예문'], [
    ['가다', '가-', '**가서**', '학교에 가서 친구를 만났어요.*'],
    ['오다', '오-', '**와서**', '비가 와서 집에 있었어요.'],
    ['많다', '많-', '**많아서**', '사람이 많아서 시끄러워요.'],
    ['먹다', '먹-', '**먹어서**', '밥을 많이 먹어서 배가 불러요.'],
    ['걸리다', '걸리-', '**걸려서**', '감기에 걸려서 학교에 못 갔어요.'],
    ['막히다', '막히-', '**막혀서**', '길이 막혀서 늦었어요.'],
    ['피곤하다', '피곤하-', '**피곤해서**', '피곤해서 일찍 잤어요.'],
    ['아프다', '아프-', '**아파서**', '배가 아파서 병원에 갔어요.'],
    ['춥다', '춥-', '**추워서**', '날씨가 추워서 두꺼운 옷을 입었어요.'],
  ], [1600, 1500, 1800, 5006], { size: 20 }));
  c.push(p('* ‘가서’ can also mean “go and then …” (sequence). In this unit we focus on the reason meaning.', { size: 17, color: MUTED, before: 40 }));
  c.push(gap());
  c.push(tip([p('⚠️ **모양이 바뀌는 말 (조금 어려워요!)**', { size: 21 }),
    p('**아프다 → 아파서**, **바쁘다 → 바빠서** : ‘ㅡ’가 빠지고 앞 모음(ㅏ)을 봐요.', { size: 20 }),
    p('**춥다 → 추워서**, **덥다 → 더워서**, **맵다 → 매워서** : ‘ㅂ’이 ‘우/오’로 바뀌어요. 통째로 외워 두면 편해요!', { size: 20 })]));
  c.push(h2('③ 꼭 기억해요! 3가지 약속'));
  c.push(warn([
    p('**❌ 약속 1.** ‘-아/어서’ 앞에는 **과거형(-았/었-)**을 쓰지 않아요.', { size: 21 }),
    p('비가 왔어서 (✗) → 비가 **와서** 집에 있었어요. (과거는 뒤 문장 끝에서 말해요.)', { size: 20, indent: { left: 300 } }),
    p('**❌ 약속 2.** 뒤 문장에 **명령(-(으)세요)·권유(-(으)ㅂ시다)**를 쓰지 않아요.', { size: 21 }),
    p('비가 와서 우산을 쓰세요. (✗) → 비가 와요. **그러니까** 우산을 쓰세요.', { size: 20, indent: { left: 300 } }),
    p('**❌ 약속 3.** ‘-아/어서’는 **한 문장 안**에서 이어 써요. 문장을 나누면 **‘그래서’**를 써요.', { size: 21 }),
    p('비가 와요. **그래서** 집에 있어요. = 비가 **와서** 집에 있어요.', { size: 20, indent: { left: 300 } }),
  ]));
  c.push(gap());
  c.push(p('👍 **자주 쓰는 인사말에도 있어요!**  만나서 반갑습니다. · 늦어서 죄송합니다. · 도와줘서 고마워요.', { size: 21 }));
  c.push(h2('✏️ 문법 연습 1 — 두 문장을 한 문장으로'));
  c.push(p('‘-아/어서’를 사용하여 한 문장으로 연결해 보세요.', { size: 21 }));
  ['날씨가 춥다. + 두꺼운 옷을 입었어요.', '눈이 많이 오다. + 차가 막혀요.', '배가 아프다. + 병원에 갔어요.',
    '다리가 아프다. + 의자에 앉았어요.', '피곤하다. + 일찍 잤어요.'].forEach((t, i) => {
    c.push(p(`${i + 1}. ${t}`, { before: 100, after: 0, keepNext: true })); c.push(p('➡️', { after: 0, keepNext: true })); c.push(...line(1));
  });
  c.push(h2('✏️ 문법 연습 2 — 이유를 넣어 문장 완성하기'));
  ['1. 저는 ______________________________ 학교에 늦었어요.', '2. 어제 ______________________________ 집에 일찍 왔어요.',
    '3. 오늘은 ______________________________ 기분이 좋아요.'].forEach((t) => c.push(p(t, { before: 120 })));
  c.push(h2('🗣️ 말하기 활동 — 왜요?'));
  c.push(tbl(['질문', '대답 (-아/어서)'], [
    ['왜 늦었어요?', '길이 막혀서 늦었어요.'], ['왜 병원에 갔어요?', '배가 아파서 병원에 갔어요.'],
    ['왜 차를 마셔요?', '감기에 걸려서 따뜻한 차를 마셔요.'], ['왜 한국어를 배워요?', '(내 이유로 대답해 보세요) ______________'],
  ], [3500, 6406], { size: 21 }));

  // ch4
  c.push(...h1('제4장 읽기', 'Reading · 짧은 글을 읽고 질문에 답해 보세요'));
  c.push(box([
    p('오늘은 겨울 방학이 시작되는 날입니다. 아침에 일어나서 창밖을 보니 하얀 **눈**이 내리고 있었습니다. 저는 기분이 너무 좋아서 동생과 함께 밖으로 나갔습니다. 우리는 마당에서 즐겁게 **눈**싸움을 했습니다.', { size: 23, line: 400, after: 160 }),
    p('그런데 너무 오래 밖에서 놀아서 감기에 걸리고 말았습니다. 머리에 열이 나고 **배**도 아팠습니다. 엄마는 저에게 따뜻한 유자**차**를 주셨습니다. 저는 따뜻한 **차**를 마시고 푹 쉬었습니다. 내일은 아프지 않았으면 좋겠습니다.', { size: 23, line: 400 }),
  ], 'FFFFFF', 'D1D5DB'));
  c.push(p('새 낱말: 방학 vacation · 마당 yard · 눈싸움 snowball fight · 감기 cold · 열이 나다 have a fever · 유자차 citron tea · 푹 쉬다 rest well', { size: 18, color: MUTED, before: 80 }));
  c.push(h2('✏️ 이해 확인 (쓰기)'));
  c.push(p('1. 이 글의 주인공은 왜 감기에 걸렸나요? (문법 ‘-아/어서’를 사용해 답해 보세요.)', { after: 0, keepNext: true })); c.push(...line(1));
  c.push(p('2. 엄마는 주인공에게 무엇을 주셨나요?', { before: 160, after: 0, keepNext: true })); c.push(...line(1));
  c.push(...quizBlock(sets[0]));

  // ch5
  c.push(...h1('제5장 퀴즈', 'Quiz · 어휘와 문장 구성력, 문법을 확인해요'));
  c.push(...quizBlock(sets[1], '문장 속 밑줄 친(굵은) 단어의 뜻을 고르세요. (Choose the meaning used in the sentence.)'));
  c.push(...quizBlock(sets[2], '단서 말을 보고 ( ) 안에 알맞은 단어를 고르세요.'));
  c.push(...quizBlock(sets[3]));
  c.push(...quizBlock(sets[4]));
  c.push(...quizBlock(sets[5], '섞여 있는 낱말을 순서대로 놓아 문장을 쓰세요. 이유(-아/어서) 문장이 먼저, 결과 문장이 나중에 와요.'));

  // appendix
  c.push(...h1('부록', 'Appendix'));
  c.push(h2('부록 1. 맞춤법 · 띄어쓰기 연습'));
  c.push(concept([p('한국어는 띄어쓰기를 잘해야 뜻이 정확하게 전달돼요. **① 낱말(명사·동사 등)은 띄어 써요. ② 조사(이/가, 을/를, 은/는, 에, 도 …)는 앞말에 붙여 써요.** 예) 눈이 / 많이 / 와서 / 차를 / 탔어요.', { size: 21 })]));
  c.push(p('띄어쓰기가 안 된 문장을 알맞게 띄어서 다시 써 보세요.', { before: 120, size: 21 }));
  ['오늘은눈이많이와서차가막혔습니다.', '동생이너무많이뛰어서다리가아프다고말했습니다.', '식사후에따뜻한차를마시며맛있는배를먹었습니다.', '어제는배가아파서병원에갔습니다.']
    .forEach((t, i) => { c.push(p(`${i + 1}. ${t}`, { before: 100, after: 0, keepNext: true })); c.push(p('➡️', { after: 0, keepNext: true })); c.push(...line(1)); });
  c.push(h2('부록 2. 더 알아보기 — 다른 동음이의어'));
  c.push(tbl(['단어', '뜻', '예문'], [
    ['**밤**', '🌙 night · 🌰 chestnut', '밤이 깊었어요. / 밤을 구웠어요.'],
    ['**말**', '🐴 horse · 💬 speech, words', '말을 타요. / 말을 잘해요.'],
    ['**병**', '🍼 bottle · 🤒 illness', '병에 물을 담았어요. / 병이 나았어요.'],
  ], [1500, 3500, 4906], { size: 21 }));
  c.push(gap());
  c.push(tip([p('🔎 **숙제:** 집이나 우리 동네에서 ‘소리는 같고 뜻이 다른 말’을 2개 찾아 문장으로 써 오세요.', { size: 21 })]));
  c.push(h2('부록 3. 이번 주 학습 점검표 (Can-do checklist)'));
  ['‘눈, 배, 다리, 차’의 뜻을 모두 말할 수 있어요.', '문장의 단서 말을 보고 알맞은 뜻을 고를 수 있어요.',
    '‘-아서 / -어서 / -해서’를 규칙대로 만들 수 있어요.', '‘-아/어서’ 앞에는 과거형을, 뒤에는 명령형을 쓰지 않아요.',
    '이유를 넣어 내 문장을 말하고 쓸 수 있어요.'].forEach((t) => c.push(p('☐  ' + t, { size: 21, before: 60 })));

  if (teacher) {
    c.push(...h1('교사용 수업 운영안', '50~60분 기준'));
    c.push(tbl(['시간', '단계', '활동'], [
      ['5′', '도입', '그림 카드(👁️🍐⛴️🌉🚗🍵)를 보여 주고 “이게 뭐예요?” → 같은 소리 발견하기'],
      ['15′', '어휘(1장)', '동음이의어 개념 → 3단계 찾기 → 단서 말 짝꿍 → 어휘 확인 1'],
      ['10′', '문장(2장)', '소리 내어 읽기 → 짝꿍 말 문장 → 나만의 문장 → 짝 활동'],
      ['15′', '문법(3장)', '원인→결과 그림 → 3단계 규칙 → 변화표 → 3가지 약속 → 연습/말하기'],
      ['10′', '읽기(4장)', '범독 → 문맥 단서로 눈·배·차 뜻 찾기 → 이해 확인'],
      ['5′+', '퀴즈(5장)', '틀린 문항은 ‘단서 말’을 찾아 함께 설명'],
    ], [1000, 1800, 7106], { size: 20 }));
    c.push(gap());
    c.push(tip([p('💡 헤리티지 학습자는 말하기는 유창해도 **띄어쓰기·받침·조사**에서 자주 틀려요. 부록 1을 매주 반복해 주세요. 영어 해설은 보조 수단이므로 점차 줄여 가세요.', { size: 21 })]));

    c.push(...h1('정답 및 해설', '교사용'));
    const L = (arr) => arr.forEach((t, i) => c.push(p(`${i + 1}. ${t}`, { size: 21, after: 40, indent: { left: 240 } })));
    c.push(h2('제1장 어휘 확인 1'));
    c.push(p('눈 · 눈 · 배 · 배 · 다리 · 다리 · 차 · 차 (그림 순서대로)', { size: 21 }));
    c.push(h2('제2장 짝꿍 말 연결 (예시 답)'));
    L(['눈이 내려요. / 눈이 와요.', '배를 탔어요. / 배를 타요.', '다리를 건너요. / 다리를 건넜어요.', '차를 마셔요. / 차를 마셨어요.']);
    c.push(h2('제3장 문법 연습 1'));
    L(['날씨가 추워서 두꺼운 옷을 입었어요.', '눈이 많이 와서 차가 막혀요.', '배가 아파서 병원에 갔어요.', '다리가 아파서 의자에 앉았어요.', '피곤해서 일찍 잤어요.']);
    c.push(p('연습 2·말하기·나만의 문장은 학습자 답에 따라 달라요. **점검 포인트** — ① 앞 절에 과거형이 없는지 ② ‘-아/어서’ 형태가 맞는지 ③ 조사를 붙여 썼는지.', { size: 20, before: 60 }));
    c.push(h2('제4장 읽기 (쓰기)'));
    L(['너무 오래 밖에서 놀아서 감기에 걸렸어요.', '따뜻한 유자차를 주셨어요.']);
    c.push(h2('부록 1 띄어쓰기'));
    L(['오늘은 눈이 많이 와서 차가 막혔습니다.', '동생이 너무 많이 뛰어서 다리가 아프다고 말했습니다.', '식사 후에 따뜻한 차를 마시며 맛있는 배를 먹었습니다.', '어제는 배가 아파서 병원에 갔습니다.']);
    sets.forEach((s) => {
      c.push(h2(s.title));
      s.items.forEach((it, i) => {
        if (it.type === 'q') {
          const a = parseInt(it.answer, 10);
          const label = it.ox ? it.opts[a - 1] : `${CIRC[a - 1]} ${it.opts[a - 1]}`;
          c.push(p(`${i + 1}. **${label}** — ${it.exp}`, { size: 20, after: 40, indent: { left: 240 } }));
        } else c.push(p(`${i + 1}. ${it.answer}`, { size: 20, after: 40, indent: { left: 240 } }));
      });
    });
  }
  return c;
}

function makeDoc(teacher) {
  return new Document({
    creator: 'Korean Textbook', title: '재외동포 한국어 2 – 1주 차' + (teacher ? ' (교사용)' : ' (학생용)'),
    styles: {
      default: { document: { run: { font: FONT, size: 22 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 36, bold: true }, paragraph: { outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 26, bold: true }, paragraph: { outlineLevel: 1 } },
      ],
    },
    sections: [{
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1000, bottom: 1000, left: 1000, right: 1000 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: '재외동포 한국어 2 · 1주 차   |   ', size: 18, color: '888888', font: FONT }),
        new TextRun({ children: [PageNumber.CURRENT], size: 18, color: '888888', font: FONT }),
      ] })] }) },
      children: buildBody(teacher),
    }],
  });
}

(async () => {
  for (const [name, teacher] of [['week01_student.docx', false], ['week01_teacher.docx', true]]) {
    fs.writeFileSync(path.join(__dirname, name), await Packer.toBuffer(makeDoc(teacher)));
    console.log('wrote', name);
  }
})();
