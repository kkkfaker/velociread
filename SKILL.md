---
name: velociread
description: "velociread 疾速读 — AI驱动的学术文献高效精读与PDF批注引擎。三档深度，三色柔和高亮，图表证据链追踪，术语原位解释，Zotero+Obsidian双轨输出，交互式配置。Trigger: 文献精读, 精读, 深度阅读, 论文精读, intensive reading, paper deep read, 读文献."
---

# velociread 疾速读

## Purpose

将一篇学术论文转化为**带批注引导的 PDF** + **结构化精读笔记 Markdown**，实现「Claude 导读 + 小绿鲸翻译」的分工协作。

核心哲学：**Claude 不替代小绿鲸的翻译引擎，Claude 做**导读标注 + 结构解析 + 图表证据链**，小绿鲸打开批注 PDF 后自主划词翻译。

---

## Trigger Conditions

激活条件（任一即可）：
- **中文触发**：文献精读 / 精读 / 小绿鲸 / 深度阅读 / 论文精读 / 逐段精读 / 读文献 / 文献笔记 / 文献翻译
- **English triggers**: intensive reading / paper deep read / paragraph-by-paragraph paper reading / annotated paper reading
- **输入触发**：用户提供 PDF 路径 / DOI / arXiv ID / 论文 URL 且提及"读"或"精读"

### DOES NOT Trigger (路由到其他技能)

| 场景 | 应路由到 |
|------|---------|
| 只要速览/全文翻译，不需要交互式精读 | `nature-reader` |
| 写论文、做大纲、润色 | `academic-paper` |
| 文献搜索、系统综述 | `academic-search` / `deep-research` |
| 审稿 | `academic-paper-reviewer` |
| 翻译整本书/整篇（非精读） | `translate-book` (if available) |

---

## Input Handling

### Accepted inputs:
1. **PDF file path** — e.g., `C:\Users\...\paper.pdf` or from Zotero
   → Zotero 用户指引：在 Zotero 中右键文献 → Show File → 复制完整路径 → 粘贴
2. **DOI** — e.g., `10.1038/s41586-024-07123-4`
   → Fetch via `https://doi.org/<DOI>`, fallback to Unpaywall
3. **arXiv ID** — e.g., `2401.12345`
   → Fetch via `https://arxiv.org/abs/2401.12345` and `https://arxiv.org/pdf/2401.12345.pdf`
4. **URL** — fetch directly, fallback to web_search for preprint

### Open-access lookup:
If paywalled, try:
- Unpaywall API: `https://api.unpaywall.org/v2/<DOI>?email=open`
- arXiv preprint via web_search: `arxiv "<title>" "<first author>"`
- Inform user if only abstract is available

---

## Workflow: 4-Stage Progressive Deep Reading

---

### Stage 1: 先导配置问卷 🚦

**CRITICAL**: Use `AskUserQuestion` tool for interactive configuration (NOT text dump). Ask Q1-Q3+Q5 together in one call, then follow up for research topic if needed.

**Config memory:** First check if user has prior config. If yes: "沿用上次配置 (A/🔬深度/Obsidian)？直接说「是」或调整单项。" If no: present interactive choices.

**Question mapping for AskUserQuestion:**
- Q1: A.小绿鲸 / B.其它工具 / C.不用翻译
- Q2: ⚡快速(~15min) / 📖标准(~45min) / 🔬深度(~2h)
- Q3: A.Obsidian / B.Zotero / C.两者都要(Obsidian MD + Zotero DOCX)
- Q5: ✏️填写研究主题 / ⏭️先跳过

Q4 (论文来源) is handled separately — user provides PDF path/DOI/arXiv/URL when invoking the skill.

**Wait for user response before proceeding to Stage 2.**

---

### Stage 2: 速览 + PDF 标注

**Progress indicators:** Show stage progress as you work:
```
[1/4] 解析PDF结构...
[2/4] 构建标注数据 (N条高亮, N术语, N图表)...
[3/4] 执行PDF批注 + 图表提取...
[4/4] 生成MD笔记 + 回存...
```

#### Step 2.1: Parse Input
- Read PDF text using `Read` tool or `pymupdf`
- Extract metadata: title, authors, journal, year, DOI
- If DOI provided without PDF, fetch paper first, then proceed

#### Step 2.2: Display Quick Overview Card
Present immediately after parsing:

```
## 📋 速览卡片

| | |
|---|---|
| **核心问题** | [一句话：这篇论文解决了什么问题] |
| **核心方法** | [方法/技术核心] |
| **关键结果** | [最重要的发现] |
| **意义** | [为什么重要] |
| **适合引用于** | [哪类论文的哪个部分可以引用] |
```

#### Step 2.3: Identify Paper Structure
- Parse IMRaD sections (Introduction / Methods / Results / Discussion)
- Identify subsection boundaries
- Build bookmark hierarchy

#### Step 2.4: Execute PDF Annotation

**CRITICAL RULES for PDF annotation:**
1. **NEVER modify the original text content of the PDF.** Use annotation overlays only (highlights, sticky notes, bookmarks).
2. PDF annotations should be **sparse and meaningful** — don't highlight everything.
3. See `references/annotation_system.md` for detailed color/style specifications. If unavailable, use these defaults:

**Annotation Types by Depth:**

| Annotation | Quick | Standard | Deep |
|------------|:-----:|:--------:|:----:|
| 🔴 Red highlight — core argument / topic sentence per paragraph | ✅ | ✅ | ✅ |
| 🔵 Blue highlight — key data / methodology details | ✅ | ✅ | ✅ |
| 🟣 Purple highlight — sentence describing figure/table conclusions (trace back from figures to text) | ✅ | ✅ | ✅ |
| 💛 Yellow sticky note — terminology explanation on first occurrence | ❌ | ✅ | ✅ |
| 📊 Figure/Table sticky note — chart type, variables, main conclusion | ✅ | ✅ | ✅ |
| 📑 Layered bookmarks — IMRaD structure tree | ✅ | ✅ | ✅ |

**Annotation placement rules:**
- Highlight: select the exact sentence text span
- Sticky note: place on the figure/table caption or first occurrence of the term
- Bookmark: one per section/subsectin at its starting page

**What NOT to put on PDF (put in MD notes instead):**
- Paragraph summaries / 段落摘要
- Inter-paragraph logic labels / 段间逻辑标注
- Sentence pattern analysis / 学习句型
- Full terminology glossary table / 术语汇总表
- Review Q&A cards / 复习卡片

#### Step 2.5: Generate Annotated PDF
Use the Python helper `scripts/annotate_pdf.py` if available. If not, provide clear instructions to run pymupdf directly:

```python
import fitz
doc = fitz.open(paper_path)
# For each annotation item specified in the reading analysis:
page = doc[page_num]
page.add_highlight_annot(bbox)  # with color
page.add_text_annot(point, content)  # sticky note
doc.set_toc(bookmark_list)  # hierarchical TOC
doc.save(output_path, incremental=False, deflate=True)
```

Save as: `{original_name}-annotated.pdf` in the same directory as the original PDF. **This is the production path — always save here, overwriting any previous annotated version.**

After annotation, also copy the annotated PDF into the Zotero item's storage directory alongside the original PDF. This allows the annotated PDF to show up as a separate attachment in Zotero after a restart.

---

### Stage 3: 深度加工 (Deep Processing)

After PDF annotation is complete, process additional content for the MD notes:

#### 3.1: Figure/Table Analysis (标准+)
For each figure and table in the paper:
1. **Extract image** from PDF using `scripts/extract_figures.py` (if available) or pymupdf
2. Identify chart type (scatter, bar, line, heatmap, schematic, etc.)
3. List variables: X-axis, Y-axis, grouping, sample size
4. Extract the main conclusion
5. **Trace back to the original sentence in the text** that describes this figure's conclusion → mark with 🟣 purple highlight + note the line number
6. Save image as `fig{N}.{ext}` in the per-paper folder's `figures/` subdirectory (e.g., `文献精读/{Paper Title}/figures/fig01.jpeg`)

Format for MD notes (use relative paths within the per-paper folder):
```markdown
### Figure {N} | 图{N}

![Figure {N}](figures/fig{N}.{ext})

- **基本信息:** {chart type} / X轴={} / Y轴={} / 分组={} (n={})
- **主要结论:** {one sentence take-home message}
- **原文结论句:** 🟢 "{original sentence}" (L.{start}-{end})
- **我的批注:** [leave placeholder for user notes]
```

For tables:
```markdown
### Table {N} | 表{N}

- **基本信息:** {rows}×{cols} / {what is being compared}
- **变量:** {var1} / {var2} / {var3}
- **主要结论:** {one sentence take-home message}
- **原文结论句:** 🟢 "{original sentence}" (L.{start}-{end})
- **我的批注:** [leave placeholder for user notes]
```

#### 3.2: Terminology Extraction (标准+)
- Identify domain-specific terms on first occurrence
- Add 💛 yellow sticky note on PDF at first occurrence: "{English term} → {Chinese translation}"
- Build glossary table in MD notes
- Categories: method / concept / abbreviation / novel term

See `references/terminology_extraction.md` for detailed rules.

#### 3.3: Core Sentence Translation (仅 Q1=B 其它工具时)
- Identify core argument sentences per paragraph
- Provide faithful Chinese translation (not literal)
- Follow translation guidelines from nature-reader
- Include in MD notes as `原文 → 翻译` pairs
- Generate bilingual HTML with side-by-side layout if Q1=B

Translation guidelines:
- Faithful, not literal — preserve scientific meaning
- Keep numbers, formulas, gene names, proper nouns in original
- Ambiguous terms: "催化活性（catalytic activity）"
- Standard Chinese scientific terminology
- Preserve hedging: suggest→表明, indicate→指出, demonstrate→证明

#### 3.4: Deep Mode Extras (🔬 only)

**3.4.1: 精辟句子收藏 ✨**
Identify 5-10 sentences worth collecting:
- Elegantly phrased arguments
- Concise summaries of complex ideas
- Clever transitions or framing
- Record original + why it's valuable

**3.4.2: 学习句型分析 📝**
Identify 3-5 sentences worth studying for academic writing:
- Effective use of hedging / boosting
- Well-structured comparisons ("In contrast to X, Y...")
- Clear hypothesis statements
- Analyze the writing technique

**3.4.3: 段间逻辑标注**
For each paragraph in the main body, label its relationship to the next:
- ➡️ 并列 (parallel)
- ⬆️ 递进 (escalation)
- ↩️ 转折 (contrast/turn)
- ⚡ 因果 (cause-effect)
- 📌 例证 (example/evidence)

**3.4.4: 个性化关联 (if Q5 research topic provided)**
```markdown
## 🔗 与我的研究关联

- **研究主题:** {user's topic}
- **联系:** {how this paper connects to the user's research}
- **可借鉴的方法/思路:** {methods or ideas worth borrowing}
- **值得引用的点:** {specific claims the user can cite}
```

**3.4.5: 复习卡片 🃏**
Generate 5-10 Q&A pairs covering:
- Core research question and answer
- Key methodology decisions
- Most important quantitative results
- Main limitation
- How it differs from prior work

**3.4.6: 跨论文关联 (only if user checked this option)**
- Scan Obsidian `文献精读/` directory for existing notes
- Search for shared methods, cited references, or contradictory findings
- Generate cross-reference links using Obsidian `[[wikilinks]]`

---

### Stage 4: 输出与回存

#### 4.1: Generate Files

**Per-paper folder structure** (one folder per paper in Obsidian):

```
文献精读/{FirstAuthor} et al. ({Year}) - {Short Title}/
├── {Author} et al. ({Year}) - {Short Title} - 精读笔记.md
└── figures/
    ├── fig01.{ext}
    ├── fig02.{ext}
    └── ...
```

| File | Condition | Location |
|------|-----------|----------|
| `{name}-annotated.pdf` | Always | Same directory as original PDF (used for Zotero overwrite) |
| `{name}-annotated.pdf` | Always | Obsidian per-paper folder (backup copy) |
| `精读笔记.md` | 标准+ | Obsidian per-paper folder: `文献精读/{Title}/` |
| `精读笔记.docx` | 标准+ | Zotero item storage directory (Word格式，存为Zotero附件) |
| `figures/fig{N}.{ext}` | 标准+ | Per-paper folder's `figures/` subdirectory |
| `双语对照.html` | Q1=B | Obsidian per-paper folder: `文献精读/{Title}/` |

#### 4.2: Save to Zotero (Overwrite Strategy)
**Overwrite the original PDF with the annotated version** — no manual attachment needed:
1. Rename original PDF: `paper.pdf` → `paper-clean.pdf` (backup)
2. Copy annotated PDF to take original's name: `paper-annotated.pdf` → `paper.pdf`
3. Zotero opens `paper.pdf` = annotated version directly
4. Also copy the annotated PDF to Obsidian per-paper folder as backup
1. **Copy** `{name}-annotated.pdf` to the Zotero item's storage directory (same directory as the original PDF, found via the `storage/<item-key>/` path)
2. The Zotero SQLite database will index it; **user needs to restart Zotero** to see the new attachment appear
3. The Zotero local API (port 23119) is unreliable — use filesystem overwrite, no API needed

#### 4.3: Save to Obsidian
**Per-paper folder structure** — one folder per paper for clean management:
1. Create per-paper folder: `文献精读/{FirstAuthor} et al. ({Year}) - {Short Title}/`
2. Create per-paper figures: `文献精读/{Title}/figures/`
3. Write MD note inside the per-paper folder
4. Extract figures into the per-paper folder's `figures/` subdirectory (NOT a shared flat `figures/`)
5. Use relative paths in MD: `![Figure N](figures/fig{N}.ext)` — this works correctly because figures and MD are in the same folder tree
6. Use `[[wikilinks]]` for cross-references to other notes

Obsidian Vault path detection:
1. Check default: `C:\Users\<username>\Documents\Obsidian Vault\`
2. If not found, ask user for their Vault path

#### 4.4: Summary Output
Present a final summary to the user:

```
✅ 精读完成！

📄 批注 PDF: {path-to-annotated-pdf}
   → Zotero: 与原文同一目录，重启 Zotero 可见
📝 精读笔记: {Obsidian Vault}/文献精读/{Title}/精读笔记.md
   → Obsidian: [[{Title} - 精读笔记]]
   📁 图片: {Title}/figures/ ({N} 张)
🌐 双语 HTML: {Title}/双语对照.html  (if Q1=B)
💡 重启 Zotero 即可在附件中看到批注 PDF

⏱️ 耗时: Stage 1: Xmin | Stage 2: Xmin | Stage 3: Xmin | Stage 4: Xmin
```

---

## PDF Annotation Technical Details

### Color Scheme
| Color | RGB | Purpose |
|-------|-----|---------|
| Red | (1.0, 0.55, 0.55) | Core argument / topic sentence |
| Blue | (0.55, 0.65, 1.0) | Key data / methodology |
| Purple | (0.55, 0.4, 0.9) | Figure/table conclusion sentence |

### Annotation Types (pymupdf)
```python
# Highlight
page.add_highlight_annot(quads)  # or annot = page.add_highlight_annot(start=point1, stop=point2)

# Sticky Note
annot = page.add_text_annot(position, content, icon="Note")

# Bookmark TOC
doc.set_toc([[1, "Introduction", 3], [2, "Methods", 6], ...])
```

### Critical: Avoid Over-Annotation
- Maximum 3-5 highlights per page
- One sticky note per figure/table
- One sticky note per term (first occurrence only)
- If a page has too many candidates, prioritize the most important ones

---

## Output Path Resolution

### Zotero PDF Location
Common paths:
- `C:\Users\<username>\Zotero\storage\<item-key>\*.pdf`
- Ask user for the PDF path at Q0 if they choose Zotero input

### Obsidian Vault Detection
Priority order:
1. Check for `obsidian.json` config in user's AppData
2. Default: `C:\Users\<username>\Documents\Obsidian Vault\`
3. Ask user if not found at default location

### File Naming
- **Per-paper folder**: `{FirstAuthor} et al. ({Year}) - {Short Title (3-5 words)}/`
  - Example: `Chen et al. (2025) - OER Catalyst Design/`
- **MD Note**: `{FirstAuthor} et al. ({Year}) - {Short Title} - 精读笔记.md`
  - Example: `Chen et al. (2025) - OER Catalyst Design - 精读笔记.md`
- **Figures**: `fig{N}.{ext}` (short names, no author prefix needed since in per-paper folder)
  - Example: `fig01.png`, `fig02.jpeg`
- **Annotated PDF**: `{original-filename}-annotated.pdf` (always alongside original)

---

## Error Handling

| Situation | Action |
|-----------|--------|
| PDF file not found | Ask user to verify path, suggest Zotero Show File workflow |
| DOI cannot be resolved | Try Unpaywall, then arXiv search, then inform user |
| Paper is paywalled without OA | Inform user, offer abstract-only mode or preprint search |
| pymupdf not installed | `pip install pymupdf` and retry |
| Zotero not running | Save PDF locally, instruct user on manual attachment |
| Obsidian Vault not found | Ask user for Vault path explicitly |
| PDF has no extractable text (scanned) | Inform user OCR is needed, skip text-based annotation, offer figure-only mode |
| Very long paper (>50 pages) | Process section by section, suggest user consider 快速标注 mode |

---

## Distinction from nature-reader

| Aspect | nature-reader | paper-anatomist |
|--------|:---:|:---:|
| Workflow | One-pass dump | 4-stage interactive with pauses |
| Output type | Single Markdown file | Annotated PDF + MD notes + optional HTML |
| Translation | Full bilingual all paragraphs | Only core sentences, strategy depends on Q1 |
| PDF annotation | ❌ | ✅ Highlights + sticky notes + bookmarks |
| Zotero integration | ❌ | ✅ Input from Zotero, output as attachment |
| Obsidian integration | ❌ | ✅ Structured MD notes with wikilinks |
| Depth levels | 4 output modes (shallow selection) | 3 depth levels (progressive) |
| Note-taking | Not supported | Placeholder system for user notes |
| Review/memory | ❌ | ✅ Review cards (deep mode) |
| User personalization | Output mode at start | 5-question intake questionnaire |
| Trigger keywords | 读论文, nature reader, 全文翻译 | 精读, 文献精读, 小绿鲸, 深度阅读, 逐段精读 |
| Translation philosophy | Claude translates everything | Claude marks, 小绿鲸 translates (by default) |

---

## Progressive Disclosure

When more detail is needed, read:
- `references/annotation_system.md` — Full PDF annotation color/style/placement rules
- `references/chart_analysis_template.md` — Extended chart interpretation templates by chart type
- `references/output_modes.md` — Detailed differences between Quick/Standard/Deep modes
- `references/terminology_extraction.md` — Term recognition heuristics and glossary standards
- `references/critical_reading_prompts.md` — Critical analysis question bank organized by IMRaD section

---

## User Interaction Protocol

1. **Stage 1**: Ask all 5 questions at once. Wait for full response.
2. **Stage 2**: Show quick overview, then proceed to annotate. No need to pause for confirmation — this stage is internal processing.
3. **Stage 3**: Process all figures, terms, and deep-mode extras. No interactive pauses needed — content goes into MD notes.
4. **Stage 4**: Present final summary with all file paths. One final message.

The skill should feel like a **fast, thorough reading assistant**, not a chatty companion. Most work happens in the background; the user sees the overview first and the summary at the end.
