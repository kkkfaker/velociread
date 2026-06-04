# Output Modes Reference

## Purpose

Detailed specification of the three depth levels and three translation engine options, including exact differences in output.

---

## Depth Level Comparison

### ⚡ Quick Mark / 快速标注 (~15 min)

**Goal:** Rapid triage — is this paper worth reading deeply?

**PDF annotations:**
- 🔴 Red highlights — 1 per paragraph (core argument)
- 🔵 Blue highlights — key quantitative results only (≤2 per section)
- 🟢 Green highlights — figure/table conclusion sentences
- 📊 Figure/Table sticky notes — chart type + main conclusion only
- 📑 IMRaD bookmarks

**NOT included:**
- Terminology sticky notes
- Paragraph summaries
- Core sentence translations

**MD note:**
```markdown
# {Title} — 精读笔记（快速标注）

> 深度: ⚡ 快速标注 | 翻译: {引擎类型} | 日期: {date}

## 📋 速览卡片
[5-row table]

## 📊 图表速览
[Figure/Table list with 基本信息 + 主要结论 only, no extended analysis]

## 📄 阅读日志
[Timestamps]
```

**Output files:**
- Annotated PDF → Zotero

---

### 📖 Standard Reading / 标准精读 (~45 min)

**Goal:** Comprehensive understanding for most papers in your field.

**PDF annotations:** All Quick + 
- 💛 Terminology sticky notes (first occurrence)
- 📊 Extended figure/table sticky notes (variables + conclusion + line ref)

**MD note:** Full template (see SKILL.md §4)

**Output files:**
- Annotated PDF → Zotero
- MD notes → Obsidian `文献精读/`
- Figure images → `文献精读/figures/`

---

### 🔬 Deep Dissection / 深度解剖 (~2 h)

**Goal:** Master important papers in your research area.

**PDF annotations:** Same as Standard (keep PDF clean)

**MD note:** Full template PLUS:
- ✨ 精辟句子收藏
- 📝 学习句型分析
- 🔗 段间逻辑标注
- 🔗 个性化关联 (if Q5 filled)
- 🃏 复习卡片 (5-10 Q&A pairs)
- 🔗 跨论文关联 (if user opted in)

**Output files:**
- Annotated PDF → Zotero
- MD notes → Obsidian (with all extra sections)
- Figure images → `文献精读/figures/`
- Bilingual HTML (if Q1=B)

---

## Translation Engine Comparison

### Q1 = A: 小绿鲸用户

**Philosophy:** Claude marks what's important; 小绿鲸 translates on demand.

**What Claude does:**
- Highlight core sentences on PDF → user can划词翻译 in 小绿鲸
- Annotate figures/tables with Chinese summaries
- Annotate terminology with Chinese translations (first occurrence)
- MD note: 速览卡片 in Chinese, 图表结论 in Chinese
- MD note: NO core sentence translation section

**What 小绿鲸 does:**
- User opens annotated PDF in 小绿鲸
- Reads highlighted sections → manually划词翻译
- Uses 小绿鲸's translation engine for any sentence

**Output:** Annotated PDF + MD notes (Chinese summaries, no English→Chinese translation)

### Q1 = B: 其它工具用户 (Claude 翻译)

**Philosophy:** Claude translates core sentences and generates a bilingual HTML for non-小绿鲸 users.

**What Claude does additionally:**
- Translate ALL core sentences (red-highlighted)
- Generate bilingual HTML with side-by-side layout
- MD note: 核心句对照 section with 原文 → 中文翻译 pairs

**HTML Format:**
```html
<!-- Two-column layout -->
<div class="section">
  <div class="en-col"><p>Original English paragraph...</p></div>
  <div class="zh-col"><p>中文翻译...</p></div>
</div>
<!-- Red-highlighted sentences marked with <mark class="core"> -->
<!-- Terminology with <abbr title="Chinese translation"> -->
```

**Output:** Annotated PDF + MD notes (with translations) + Bilingual HTML

### Q1 = C: 不用翻译

**Philosophy:** Pure annotation — English-only, no translation work.

**What Claude skips:**
- NO Chinese translations anywhere
- NO bilingual HTML
- NO terminology Chinese translations (English definitions only if needed)
- MD note: 速览卡片 and 图表结论 in English

**Output:** Annotated PDF + MD notes (English)

---

## Storage Location Comparison

### Q3 = A: Obsidian（默认）

```
{Obsidian Vault}/
└── 文献精读/
    ├── {Author} ({Year}) - {Title} - 精读笔记.md
    └── figures/
        └── {Author}{Year}_fig{N}.png

Zotero:
└── 原文献条目
    └── {name}-annotated.pdf (子附件)
```

### Q3 = B: Zotero

```
Zotero:
└── 原文献条目
    ├── {name}-annotated.pdf (子附件)
    └── {Author} ({Year}) - {Title} - 精读笔记.md (子附件)

⚠️ 笔记作为Zotero附件时：
  - 图片嵌入在Markdown中无法直接显示
  - 建议图片使用绝对路径或base64嵌入
  - 或者images不单独提取，只保留文本描述
```

### Q3 = C: Both

Same file structure as A + B combined.

---

## Mode Selection Decision Tree

```
User opens skill
  │
  ├─ "快速看看值不值得精读" → ⚡ Quick + 默认不用翻译
  │
  ├─ "这篇文章和我研究方向相关" → 📖 Standard + 选小绿鲸 or Claude翻译
  │     │
  │     └─ 如果填写了Q5研究主题 → 建议 🔬 Deep
  │
  ├─ "这是领域内重要论文，要精读" → 🔬 Deep + 勾选跨论文关联
  │
  └─ "不用翻译，英文阅读无障碍" → 任意深度 + Q1=C
```

---

## Anti-Patterns: What Each Mode Should NOT Do

| Anti-Pattern | Explanation |
|--------------|-------------|
| Quick mode generating paragraph summaries | Quick is triage only — summaries defeat the purpose |
| Standard mode adding 20 highlights per page | Keep PDF clean; over-annotation is counterproductive |
| Deep mode translating every sentence | Only core sentences; let 小绿鲸 handle the rest |
| Q1=A mode generating Chinese translations in MD | The point is 小绿鲸 does the translation on-demand |
| Q1=C mode still generating bilingual section headers | If user says no translation, respect that everywhere |
