# Chart Analysis Template

## Purpose

Extended chart interpretation templates organized by chart type. Used in Stage 3 during figure/table deep processing to ensure consistent, high-quality chart annotations.

---

## Common Chart Types

### 1. Scatter Plot / 散点图
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** 散点图 / X轴={independent_var} / Y轴={dependent_var} / 每个点={unit_of_observation} / 颜色/形状分组={grouping_var} (n={sample_size})
- **趋势:** {overall trend — positive/negative/nonlinear/no correlation}
- **异常点:** {notable outliers and what they might mean}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

### 2. Bar Chart / 柱状图
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** 柱状图 / X轴={categories} / Y轴={measured_value} ({unit}) / 误差棒={error_type} / 分组={grouping_var} (n={sample_size})
- **显著差异:** {which bars are significantly different, p-values if given}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

### 3. Line Chart / 折线图
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** 折线图 / X轴={time/condition} / Y轴={measured_value} ({unit}) / 每条线={series_var} / 误差带={error_type} (n={sample_size})
- **关键拐点:** {turning points, inflection thresholds}
- **趋势:** {overall trend per series}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

### 4. Heatmap / 热图
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** 热图 / X轴={col_var} / Y轴={row_var} / 颜色映射={color_scale} / 数值={value_represented}
- **高值区域:** {clusters of high values and their meaning}
- **低值区域:** {clusters of low values and their meaning}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

### 5. Microscopy/TEM/SEM Image / 显微图像
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** {technique}图像 / 放大倍数={magnification} / 标尺={scale_bar} / 视角={top-view/cross-section/...}
- **关键特征:** {visible structures — particles, layers, pores, lattice fringes, etc.}
- **测量的特征尺寸:** {quantitative measurements from the image}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

### 6. XRD Pattern / XRD图谱
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** XRD图谱 / X轴=2θ(°) / Y轴=Intensity(a.u.) / 辐射源={Cu Kα/Mo Kα/...}
- **主要衍射峰:** 2θ={peak1}°({hkl}) / 2θ={peak2}°({hkl}) / ...
- **晶相鉴定:** {identified phases with PDF card numbers}
- **晶粒尺寸:** {Scherrer估算 if applicable}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

### 7. XPS / Spectroscopy / 谱图
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** {technique}谱图 / X轴={energy/wavelength/wavenumber} / Y轴={Intensity/Absorbance}
- **主要峰位:** {peak1} at {position} — assigned to {chemical_state/species}
- **峰位归属:** {detailed peak assignments}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

### 8. DFT / Computational Result / 计算图
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** {calculation_type} / {functional/basis_set} / {model_system}
- **关键能量:** {energy_barrier/adsorption_energy/reaction_energy} ({unit})
- **结构/路径:** {key structural features or pathway steps visualized}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

### 9. Schematic / Mechanism Diagram / 示意图
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** 示意图 / 描述={what the diagram illustrates}
- **关键步骤/组件:** {step1 → step2 → step3 / component1 — component2 — component3}
- **新颖之处:** {what this mechanism proposes that's new}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

### 10. Multi-Panel Figure / 多面板组合图
```markdown
### Figure {N} | 图{N}

![Figure {N}](./figures/{Author}{Year}_fig{N}.png)

- **基本信息:** {N}面板组合图 / a={panel_a_desc} / b={panel_b_desc} / c={panel_c_desc}
- **面板a:** {chart_type_a} / {main finding from panel a}
- **面板b:** {chart_type_b} / {main finding from panel b}
- **面板c:** {chart_type_c} / {main finding from panel c}
- **整体叙事:** {how the panels together tell a story}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

---

## Table Analysis Template

```markdown
### Table {N} | 表{N}

- **基本信息:** {rows}行×{cols}列 / 比较={what aspect is compared across what conditions}
- **变量列表:**
  | 列名 | 含义 | 单位 |
  |------|------|------|
  | {col1} | {meaning1} | {unit1} |
  | {col2} | {meaning2} | {unit2} |
- **关键数据:**
  - {row_label}: {most_important_value} — {what it means}
  - {row_label}: {most_important_value} — {what it means}
- **趋势/规律:** {overall pattern across conditions}
- **主要结论:** {one sentence take-home}
- **原文结论句:** 🟢 "{original}" (L.{start}-{end})
- **我的批注:**
```

---

## Evidence Chain Quality Rules

For every figure/table annotation, enforce these rules:

1. **原文结论句 must be a real sentence from the paper text**, not a paraphrase. Quote exactly.
2. **Line numbers must be accurate.** If the PDF doesn't have line numbers, use page+paragraph position: "P.5, §3"
3. **主要结论 should be a one-sentence take-home**, not a description of what the figure literally shows. Answer: "What does this figure prove?"
4. **变量列表 should be specific** — don't say "various conditions", list them.
5. **If the paper reports statistics** (p-values, error bars, R²), include them in the annotation.
6. **My 批注 field** is intentionally left as placeholder for the user to fill in. Never fill it with AI-generated content.

---

## Figure Extraction

Use pymupdf to extract embedded images from the PDF:

```python
import fitz

doc = fitz.open("paper.pdf")
for page_num in range(len(doc)):
    page = doc[page_num]
    image_list = page.get_images()
    for img_idx, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        ext = base_image["ext"]  # png, jpeg, etc.
        with open(f"figures/{Author}{Year}_fig{img_idx+1}.{ext}", "wb") as f:
            f.write(image_bytes)
```

**Important:** pymupdf extracts ALL embedded images, including small icons, journal logos, etc. Filter by size — only keep images larger than ~50KB or wider than 200px. Manually match extracted images to figure numbers by cross-referencing with the PDF page where they appear.

---

## Chart Type Quick Reference

| English | 中文 | Key Analysis Points |
|---------|------|---------------------|
| scatter plot | 散点图 | correlation, outliers, clustering |
| bar chart | 柱状图 | comparison, significance, error bars |
| line chart | 折线图 | trend, inflection, slope |
| heatmap | 热图 | clustering, hot/cold regions |
| box plot | 箱线图 | median, quartiles, outliers |
| violin plot | 小提琴图 | distribution shape, multi-modal |
| histogram | 直方图 | distribution, bin width artifacts |
| pie chart | 饼图 | proportions (rare in science papers) |
| TEM/SEM | 电镜图 | morphology, size, lattice, EDS mapping |
| XRD pattern | XRD | phase ID, crystallinity, Scherrer size |
| XPS spectrum | XPS | chemical state, deconvolution |
| Raman/IR | 拉曼/红外 | vibrational modes, bonding |
| NMR | 核磁 | chemical shift, coupling |
| TGA/DSC | 热分析 | decomposition, phase transition |
| BET isotherm | 比表面 | surface area, pore size distribution |
| cyclic voltammetry | 循环伏安 | redox potential, reversibility |
| EIS (Nyquist) | 阻抗谱 | charge transfer resistance |
| DFT/calculation | 计算 | energy profile, transition state, DOS |
| schematic/diagram | 示意图 | mechanism, workflow, model |
| phylogenetic tree | 系统发育树 | clade relationships, bootstrap |
| volcano plot | 火山图 | optimal binding energy descriptor |
