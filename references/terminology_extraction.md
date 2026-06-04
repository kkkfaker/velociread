# Terminology Extraction Guidelines

## Purpose

Rules for identifying, extracting, and annotating domain-specific terminology from academic papers. Used in Stage 3.2 for PDF sticky notes and MD glossary table.

---

## Term Recognition Heuristics

### High-confidence signals (extract these):
1. **Capitalized abbreviations defined in parentheses**: "...oxygen evolution reaction (OER)..."
2. **Italicized or bolded technical terms**: "*in situ* Raman spectroscopy"
3. **Defined-in-context patterns**: "...herein referred to as..." / "...defined as..."
4. **Repeated specialized vocabulary**: appears 5+ times but not in general English
5. **Method/instrument names**: "HAADF-STEM", "X-ray absorption spectroscopy"
6. **Novel terms coined by the authors**: "We term this...", "Here we introduce..."
7. **Domain-specific jargon** that a non-specialist wouldn't know

### Low-confidence signals (only extract if central to the paper):
1. Common scientific vocabulary (e.g., "catalyst", "experiment", "synthesis")
2. Terms with obvious meanings from context
3. General academic vocabulary (e.g., "furthermore", "notably", "demonstrate")

### DO NOT extract:
- Common English words used in their standard sense
- Journal names, author names, institution names
- Very common abbreviations (e.g., "e.g.", "i.e.", "etc.")
- Terms that every undergraduate in the field already knows

---

## Glossary Table Format

```markdown
## 📊 术语表

| # | 英文术语 | 中文翻译 | 定义/说明 | 类别 | 首次出现 |
|---|---------|---------|----------|------|---------|
| 1 | oxygen evolution reaction (OER) | 析氧反应 | 水氧化产生O₂的电化学反应，电解水制氢的阳极半反应 | concept | §1, L.23 |
| 2 | turnover frequency (TOF) | 转换频率 | 单位时间内每个活性位点转化的反应物分子数，单位h⁻¹ | method | §2.3, L.156 |
| 3 | single-atom catalyst (SAC) | 单原子催化剂 | 活性金属以单个原子形式分散在载体上的催化剂 | concept | §1, L.12 |
| 4 | Ru/C | Ru/C催化剂 | 钌纳米颗粒负载于碳载体的催化剂 | abbrev | §1, L.15 |
| 5 | *in situ* Raman | 原位拉曼光谱 | 在反应条件下实时采集的拉曼光谱，用于监测反应中间体 | method | §2.4, L.189 |
```

### Category Taxonomy:
| Category | Code | Criteria |
|----------|------|----------|
| concept | 概念 | Core scientific concept in the field |
| method | 方法 | Methodology, technique, instrument |
| abbrev | 缩写 | Abbreviation or acronym |
| novel | 新造词 | Term newly introduced/coined by the authors |
| reagent | 试剂 | Chemical, material, reagent |

---

## PDF Sticky Note Format

For each term's **first occurrence only**:

```
术语 | Term
{English term}
→ {Chinese translation}
{简要定义 — 1行中文}
```

**Keep it short** — the sticky note must be readable at a glance. Full definitions go in the MD glossary table.

**Example:**
```
术语 | Term
oxygen evolution reaction (OER)
→ 析氧反应（OER）
电解水阳极产氧反应
```

**Placement:** Position the sticky note near the first occurrence of the term on the page. If the term first appears in the abstract, annotate there.

---

## Quality Verification Rules

1. **Verify from context:** Does the paper's usage support the definition? Don't guess from prior knowledge alone.
2. **Flag uncertain definitions:** If the definition is inferred rather than explicitly stated, mark with `[推断]`.
3. **Consistency check:** Same term should have the same translation throughout.
4. **Abbreviation pairing:** Always pair abbreviations with their full form on first occurrence.
5. **Chinese translation priority:** Use standard Chinese scientific terminology (国家标准) when available. For novel terms, provide a reasonable translation and mark as `[暂译]`.

---

## Domain-Specific Knowledge

### Materials/Chemistry
- Standard translations: catalyst→催化剂, adsorption→吸附, desorption→脱附
- Be careful: "conversion" could be 转化率 or 转换 depending on context
- XRD, XPS, TEM, SEM, BET typically don't need translation (keep as abbreviations)
- Chemical formulas stay in original: Ru/C NOT 钌碳

### Biology/Medicine
- Gene names: keep in original (italicized per convention)
- Protein names: standard Chinese nomenclature or keep English
- Disease names: use ICD standard Chinese translations

### Computer Science / AI
- Many terms don't have settled Chinese translations — use English original + Chinese explanation
- Architecture names: keep English (ResNet, Transformer, LSTM)

### Economics / Social Sciences
- Statistical terms: use standard Chinese translations from 统计学教材
- Theoretical framework names: may keep English or use settled translations

---

## Per-Depth Extraction Rules

| Depth | # Terms to Extract | Category Coverage |
|-------|:---:|---|
| ⚡ Quick | 0 | No terminology extraction |
| 📖 Standard | 8-15 | concept + method + abbrev (top priority) |
| 🔬 Deep | 15-25 | All categories including novel terms |

**Selection priority within Standard mode:**
1. Central to understanding the paper (appears in abstract/introduction)
2. Used in the main findings/results
3. Method-specific terms
4. Supplementary/background terms (can skip in Standard)
