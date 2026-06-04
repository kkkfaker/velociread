<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-skill-8A2BE2?style=flat-square" />
  <img src="https://img.shields.io/badge/Obsidian-ready-7C3AED?style=flat-square" />
  <img src="https://img.shields.io/badge/Zotero-integrated-CC2936?style=flat-square" />
  <img src="https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey?style=flat-square" />
</p>

<h1 align="center">⚡ velociread</h1>
<p align="center"><strong>AI-driven intensive paper reading · PDF annotation · bilingual notes</strong></p>
<p align="center"><a href="#chinese">中文</a> · <a href="#english">English</a></p>

---

<h2 id="chinese">🇨🇳 中文</h2>

### 简介

**velociread**（原 paper-anatomist）是一个 Claude Code 技能，将学术论文转化为**带高亮批注的 PDF** + **结构化精读笔记**。

专为用户设计的文献阅读工具链整合：

- 📚 **[Zotero](https://www.zotero.org/)** 管理你的文献库 —— 论文从 Zotero 一键输入，批注版自动存回
- 🧠 **[Obsidian](https://obsidian.md/)** 构建你的知识网络 —— 精读笔记（含图表+术语+复习卡）自动归档，双向链接串联论文
- 🐋 **小绿鲸（IvySci）** 是你的翻译利器 —— 批注 PDF 保留原文不动，用惯的小绿鲸打开继续划词翻译，CN 用户无缝衔接

核心哲学：**Claude 做导读标注 + 结构解析，小绿鲸做翻译**——各司其职，效率翻倍。

### 核心特色

| 特色 | 说明 |
|------|------|
| 📄 **PDF 原位批注** | 三色柔和高亮（核心观点/关键数据/图表结论）+ 术语旁注 + 层级书签，不破坏原文 |
| 🌐 **翻译引擎可选** | 小绿鲸用户：仅标注引导，不翻译原文；其他工具用户：Claude 翻译核心句 + 生成双语 HTML |
| 🔗 **Zotero → Obsidian 双轨** | 从 Zotero 输入 PDF → 批注版自动覆盖 Zotero 原文件 → 精读笔记（.md + .docx）同步到 Obsidian 和 Zotero |
| 📊 **图表证据链** | 每张图标注类型/变量/结论 + 🟣高亮回溯原文结论句，图表和原文互相对应 |
| 🎚️ **三档深度** | ⚡快速标注(~15min) / 📖标准精读(~45min) / 🔬深度解剖(~2h) |
| 🎯 **交互式配置** | 点选式问卷，不用打字；记住上次配置，一键复用 |
| 📝 **双格式输出** | Markdown → Obsidian（含图片嵌入+双向链接） + Word → Zotero 附件 |
| 🃏 **复习卡片** | 深度模式自动生成 5-10 对 Q&A 复习卡 |

### 快速开始

```bash
# 1. 克隆仓库到 Claude Code skills 目录
git clone https://github.com/<your-username>/velociread.git ~/.claude/skills/velociread

# 2. 安装依赖
pip install pymupdf python-docx

# 3. 在 Claude Code 中调用
/精读
# 或直接说：精读这篇论文
```

### 功能一览（6 模块 · 23 项）

```
📥 输入        Zotero PDF / DOI / arXiv / URL
📖 阅读翻译    速览卡片 · IMRaD识别 · 核心句定位 · 术语提取 · 按需翻译
🎨 PDF批注     三色高亮 · 侧边批注 · 层级书签 · 图表双向标注(图旁+原文🟣高亮)
🏷️ 批注体系     核心观点💡 · 重点数据⭐ · 图表结论📊 · 精辟句子✨ · 学习句型📝
🗂️ 可视化      章节结构树 · 段落摘要 · 段间逻辑 · 个性化关联 · 复习卡片 · 跨论文关联
💾 输出        PDF→Zotero覆盖 + MD→Obsidian + DOCX→Zotero · 图表嵌入 · 可选双语HTML
```

### 工作流

```
Stage 1: 先导问卷  → 点选配置（翻译引擎/深度/存储/研究主题）
Stage 2: 速览+标注  → 速览卡片 + IMRaD结构 + PDF三色高亮 + 术语旁注 + 书签
Stage 3: 深度加工   → 图表提取+解读 + 术语表 + 段落摘要 + 复习卡片(深度模式)
Stage 4: 输出回存   → 批注PDF覆盖Zotero + MD→Obsidian + DOCX→Zotero
```

### 与同类工具对比

| 功能 | **velociread** | nature-reader | paper-reading-zh | evil-read-arxiv | Echo/PBurnerX |
|------|:---:|:---:|:---:|:---:|:---:|
| PDF原位高亮批注 | ✅ 自动三色 | ❌ | ❌ | ❌ | ✅ 手动 |
| 翻译引擎可选 | ✅ 小绿鲸/Claude/无 | ❌ | ❌ | ❌ | ❌ |
| Zotero→Obsidian双轨 | ✅ | ❌ | ❌ | Obsidian仅 | ❌ |
| 交互式配置问卷 | ✅ | 部分 | ❌ | ❌ | ❌ |
| 图表⇔原文证据链 | ✅ | ✅ 图表解读 | ❌ | ❌ | ❌ |
| 术语PDF原位旁注 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 三档深度分级 | ✅ | ❌ | ✅ 三模式 | ❌ | ❌ |
| 复习卡片 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 双语翻译 | ✅ | ✅ 全文翻译 | ✅ | ✅ | ❌ |
| 结构化笔记输出 | ✅ MD+Docx | ✅ MD | ✅ MD | ✅ MD | ❌ |
| 跨论文关联 | ✅ 按需 | ❌ | ❌ | ❌ | ❌ |
| Web UI | ❌ CLI | ❌ CLI | ❌ CLI | ✅ Web | ✅ Web |
| 每日论文推荐 | ❌ | ❌ | ❌ | ✅ | ❌ |
| 离线可用 | ❌ 需API | ❌ | ❌ | ❌ | ✅ 浏览器 |

### 依赖

- **Python**: pymupdf (PDF批注), python-docx (Word输出)
- **Zotero 7**: 文献管理（输入PDF + 存储输出）
- **Obsidian**: 知识管理（笔记存储，可选）
- **小绿鲸**: 翻译阅读（可选，Q1=A时使用）

### 安装

```bash
git clone https://github.com/<your-username>/velociread.git ~/.claude/skills/velociread
pip install pymupdf python-docx
```

确保 Zotero 7 后台运行。Obsidian Vault 默认路径：Windows `C:\Users\<用户名>\Documents\Obsidian Vault\` / macOS `~/Documents/Obsidian Vault/`，技能会自动检测。

### 打赏

如果这个工具提升了你的文献阅读效率，欢迎请我喝杯咖啡 ☕

<p align="center">
  <img src="assets/sponsor.jpg" width="400" alt="打赏码" />
</p>

---

<h2 id="english">🇬🇧 English</h2>

### Overview

**velociread** is a Claude Code skill that transforms academic papers into **annotated PDFs** + **structured reading notes**.

Built for a seamless toolchain:

- 📚 **[Zotero](https://www.zotero.org/)** for reference management — import papers directly, annotated PDFs save back automatically
- 🧠 **[Obsidian](https://obsidian.md/)** for knowledge management — structured notes with figures, glossary, and review cards, linked via wikilinks
- 🐋 **IvySci (小绿鲸)** for on-demand translation — annotated PDFs preserve original text, open in IvySci to translate any sentence

Core philosophy: **Claude annotates and structures; your translator handles the rest** — each tool does what it does best.

### Key Features

| Feature | Description |
|---------|-------------|
| 📄 **PDF Annotation Overlay** | 3-color soft highlights + term sticky notes + layered bookmarks |
| 🌐 **Translation Engine Choice** | Mark for IvySci/other translation, Claude translate, or annotation-only |
| 🔗 **Zotero → Obsidian Pipeline** | PDF in from Zotero → annotated PDF overwrites original → notes to Obsidian (.md) + Zotero (.docx) |
| 📊 **Figure Evidence Chain** | Chart type/variables/conclusion + 🟣 trace back to source sentence in text |
| 🎚️ **Three Depth Levels** | Quick(~15min) / Standard(~45min) / Deep(~2h) |
| 🎯 **Interactive Config** | Click-through questionnaire with config memory |
| 🃏 **Review Cards** | Auto-generated Q&A pairs (Deep mode) |

### Quick Start

```bash
git clone https://github.com/<your-username>/velociread.git ~/.claude/skills/velociread
pip install pymupdf python-docx
# In Claude Code: /精读
```

### License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — Free for non-commercial use with attribution.
