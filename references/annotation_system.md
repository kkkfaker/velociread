# PDF Annotation System

## Purpose

Detailed specification for PDF annotation colors, styles, and placement rules. Load this reference when the skill needs to execute precise PDF annotations via pymupdf.

---

## Color Scheme

| Annotation | Color Name | RGB (fitz) | Hex | Visual |
|------------|-----------|------------|-----|--------|
| Core argument / topic sentence | Red (soft) | (1.0, 0.55, 0.55) | #FF8C8C | 🔴 |
| Key data / methodology | Blue (soft) | (0.55, 0.65, 1.0) | #8CA6FF | 🔵 |
| Figure/table conclusion sentence | Purple (soft) | (0.55, 0.4, 0.9) | #8C66E6 | 🟣 |
| Terminology note | Yellow (soft, sticky) | (1.0, 1.0, 0.55) | #FFFF8C | 💛 |

Sticky note icon: "Note" (pymupdf default)

---

## Highlight Rules

### Red 🔴 — Core Argument / Topic Sentence
**Selection criteria:**
- The sentence that states the paragraph's main claim or contribution
- Typically the first or second sentence of the paragraph
- NOT background/context sentences
- NOT sentences that only summarize others' work

**Frequency:** One per paragraph maximum. **In the Introduction section, highlight EVERY paragraph's core sentence** — this is the most important section for understanding the paper's motivation, gap, and approach. Other sections: highlight only paragraphs with substantive claims.

**Special rule for Introduction:** Be aggressive. Every paragraph in the Introduction should have at least one red highlight covering its argumentative contribution to the paper's narrative arc. The Introduction is the roadmap — make every paragraph's role visible.

**Precision:** Select the exact sentence text span, not the entire paragraph

**Example selections:**
- ✅ "Here we demonstrate that Ru/C catalysts achieve 98% conversion efficiency..."
- ✅ "Our results establish a new paradigm for catalyst design..."
- ❌ "Previous studies have investigated various catalyst systems..." (this is background, not core)
- ❌ "As shown in Figure 3, the trend is consistent..." (this belongs to purple 🟣)

### Blue 🔵 — Key Data / Methodology
**Selection criteria:**
- Sentences reporting specific quantitative results
- Key experimental parameters or conditions
- Critical methodology steps that define the approach

**Frequency:** 1-3 per results/methods section

**Example selections:**
- ✅ "The catalyst exhibited a TOF of 1200 h⁻¹ at 80°C and 1 atm H₂."
- ✅ "Samples were characterized by HAADF-STEM, XAS, and XPS."
- ❌ "The detailed procedure is described in the Supplementary Information."

### Purple 🟣 — Figure/Table Conclusion Sentence
**Selection criteria:**
- Sentence in the main text that states the conclusion drawn from a specific figure or table
- Must be traceable: the sentence references a figure/table by number ("Figure 3 shows...", "As seen in Table 2...")
- OR the sentence describes a result that is visually evident in a figure/table

**Frequency:** 1-3 per major figure or table

**Placement rule:** Place purple highlight on the text sentence, AND add a sticky note on the figure/table caption pointing back: "🟣 原文结论句见 L.{start}-{end}"

**Example selections:**
- ✅ "Notably, the Ru/C catalyst maintained >90% activity after 100 cycles, confirming its superior stability (Fig. 4b)."
- ✅ "The EXAFS fitting revealed Ru-N coordination at 2.01 Å, consistent with single-atom dispersion (Table 1, Fig. 2c)."

---

## Sticky Note Rules

### Terminology 💛 (Standard+ depth only)
**Trigger:** First occurrence of a domain-specific term
**Content format:**
```
术语 | Term
{English term}
→ {Chinese translation}
{Definition}: {brief explanation in Chinese}
```

**Example:**
```
术语 | Term
oxygen evolution reaction (OER)
→ 析氧反应（OER）
定义: 水氧化产生氧气的电化学反应，是电解水制氢的阳极半反应
```

**Selection criteria for terms:**
- Domain-specific technical terms (not common English words)
- Abbreviations on first use
- Novel/coined terms the authors introduce
- Method/instrument names that are field-specific

**Do NOT annotate:**
- Common scientific vocabulary (e.g., "catalyst", "experiment", "temperature")
- Terms explained well in standard textbooks
- Terms already annotated earlier in the PDF

### Figure/Table Annotation 📊 (All depths)
**Placement:** On the figure/table caption text
**Content format:**
```
📊 Figure {N} | 图{N}
类型: {chart type}
变量: {variables}
主要结论: {one-sentence take-home}
原文结论句: L.{start}-{end}
```

**For tables, add:**
```
行×列: {rows}×{cols}
```

**Example:**
```
📊 Figure 3 | 图3
类型: 散点图 (Scatter plot)
变量: X轴=反应时间(min) / Y轴=转化率(%) / 颜色=催化剂种类
主要结论: Ru/C在30min时转化率达98%，显著高于Pt/C(72%)和Fe/C(45%)
原文结论句: L.234-236
```

---

## Bookmark Hierarchy

### IMRaD Structure TOC
Generate bookmarks matching the paper's hierarchy:

```
1. Introduction                          (page N)
   1.1 Background                       (page N)
   1.2 Research Gap & Hypothesis        (page N)
2. Results                               (page N)
   2.1 [Subsection Title]               (page N)
   2.2 [Subsection Title]               (page N)
3. Discussion                            (page N)
4. Methods                               (page N)
   4.1 [Subsection Title]               (page N)
5. Supplementary (if applicable)         (page N)
```

**Naming convention:** Use the paper's actual section titles. Add Chinese translation in bookmark only if it helps navigation (e.g., "2.1 Catalyst Characterization 催化剂表征").

---

## Density Limits

### Maximum Annotations Per Page
| Annotation Type | Max Per Page |
|-----------------|:---:|
| Red highlight | 3 |
| Blue highlight | 2 |
| Purple highlight | 2 |
| Yellow sticky (term) | 2 |
| Figure/Table sticky | As many as there are figures/tables on the page |

If a page exceeds limits, prioritize:
1. The most novel/important claim
2. The largest quantitative result
3. The figure with the highest evidentiary value

---

## pymupdf Implementation

### Typical annotation workflow:
```python
import fitz

doc = fitz.open("paper.pdf")

# Highlight
page = doc[page_num]
quads = page.search_for("text to highlight")
if quads:
    annot = page.add_highlight_annot(quads)
    annot.set_colors(stroke=(1, 0, 0))  # red
    annot.update()

# Sticky note
point = fitz.Point(x, y)
annot = page.add_text_annot(point, "content", icon="Note")
annot.set_colors(stroke=(1, 1, 0))  # yellow
annot.update()

# Bookmarks (TOC)
doc.set_toc([
    [1, "Introduction", 3],
    [2, "Results", 5],
    [2, "Discussion", 12],
])

# Save (incremental=False compresses away deleted content)
doc.save("paper-annotated.pdf", incremental=False, deflate=True)
doc.close()
```

### Finding text positions:
- Use `page.search_for("text")` to get quads for highlighting
- For sticky notes, place near the figure caption or term's first occurrence
- If text search fails (e.g., ligatures, special chars), use approximate position from paragraph layout

### Color application:
```python
# Red highlight (soft — avoid harsh saturated colors)
annot.set_colors(stroke=(1.0, 0.55, 0.55))

# Blue highlight (soft)
annot.set_colors(stroke=(0.55, 0.65, 1.0))

# Purple highlight (soft — for figure/table conclusion sentences)
annot.set_colors(stroke=(0.55, 0.4, 0.9))

# Yellow sticky note (soft)
annot.set_colors(stroke=(1.0, 1.0, 0.55))
```

---

## Quality Checklist

Before finalizing the annotated PDF, verify:
- [ ] No page exceeds density limits
- [ ] All purple highlights have corresponding figure/table sticky notes
- [ ] All figure/table sticky notes include 原文结论句行号
- [ ] Bookmark hierarchy matches actual paper structure
- [ ] PDF opens correctly in Adobe Reader and 小绿鲸
- [ ] Original text is not obscured by annotations
- [ ] Colors are distinguishable (check: red/blue/purple are visually distinct)
