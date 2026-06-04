# Critical Reading Prompts

## Purpose

Structured critical analysis question bank for use in Deep Dissection mode (🔬). Organized by IMRaD section. Questions follow the Socratic pattern: open-ended, non-leading, designed to trigger critical thinking rather than solicit agreement.

---

## Usage

In Deep mode, select 3-5 most relevant questions per major section of the paper and present them in the MD notes under each section. Do NOT answer the questions — leave them as thought prompts for the reader.

---

## Introduction / 引言

### Motivation & Framing (选 1-2)
1. 作者提出的研究动机是否足够充分？有没有遗漏的重要背景？
2. 文献综述部分是否有选择性引用（只引用支持自己观点的文献）？
3. 作者如何界定"研究空白"（research gap）？这个空白是否真的存在，还是被故意放大？
4. 引言中的假设（hypothesis）是否可检验？如果是探索性研究，是否明确说明了？

### Logic & Structure (选 1-2)
5. 从"已知背景"到"研究问题"的逻辑链条是否完整？有没有跳跃？
6. 作者的研究问题/目标陈述是否清晰、具体？（check: 是否可以在读完引言后用一句话复述）
7. 如果该领域存在争议，作者是否公平地呈现了不同观点？

---

## Methods / 方法

### Design & Reproducibility (选 1-2)
8. 实验设计能否真正回答研究问题？有没有更优的设计方案？
9. 样本量是否合理？能否支撑论文的结论？（如果作者做了 power analysis，检查其假设）
10. 方法和参数描述是否足够详细，使得其他研究者可以复现？
11. 是否缺少关键对照实验/控制组？

### Measurement & Validity (选 1-2)
12. 测量方法的信度和效度是否经过验证？
13. 仪器/试剂的精度是否与论文中报告的有效数字匹配？
14. 如果使用了统计检验，检验方法的选择是否正确？假设是否满足？
15. 作者是否报告了所有必要的不确定性/误差来源？

### Confounding & Bias (选 1)
16. 实验过程中哪些变量未控制，可能成为混杂因子？
17. 是否存在选择偏倚（selection bias）或确认偏误（confirmation bias）的风险？

---

## Results / 结果

### Data Quality (选 1-2)
18. 数据呈现是否清晰？图表是否有误导性的坐标轴尺度、颜色映射？
19. 是否有数据点被"意外"排除？排除标准是否合理且预先定义？
20. 误差棒代表什么（SD/SEM/CI）？样本量是否足以使误差估计可信？

### Statistical Rigor (选 1-2)
21. 统计显著性（p值）是否被正确解读？是否存在 p-hacking 的迹象（多个比较未校正）？
22. 效应量（effect size）是否大于统计显著性？实际意义如何？
23. "不显著"的结果是否被正确报告，还是被忽略了？
24. 相关性和因果性是否被混淆？

### Figure Integrity (选 1-2)
25. 图表是否真实反映了数据？有没有被裁剪/美化/选择性展示的嫌疑？
26. 图中的文字/标签是否与正文描述一致？
27. 补充材料（SI）中的数据和正文中的数据是否一致？

### Results → Interpretation Gap (选 1-2)
28. 从数据到结论的推论是否合理？有没有替代解释？
29. 负面结果或不理想的数据是如何被处理的？（诚实报告 vs. 回避/美化）
30. 结果是否超出了实验设计的证明能力？

---

## Discussion / 讨论

### Interpretation Quality (选 1-2)
31. 作者对结果的解释是否过度推论（overclaiming）？
32. 讨论中是否出现了引言和结果中未提及的"惊喜发现"？（这是 red flag）
33. 作者是否讨论了与已有文献的矛盾之处？对矛盾的解释是否合理？

### Limitation Honesty (选 1-2)
34. 作者是否诚实地讨论了研究的局限性？
35. 有哪些重要局限作者没有提及？（方法、样本、推广性等）
36. 未来研究方向是否具体，还是模板化的"more research is needed"？

### Generalizability (选 1)
37. 结论的适用范围是什么？作者是否夸大了推广性？
38. 如果将样本/条件更换，结论是否仍然成立？

---

## Overall / 整体评估

### Contribution & Novelty
39. 这篇论文的真正贡献是什么？增量式改进还是突破性发现？
40. 如果去掉这篇文章，该领域会失去什么？
41. 该研究与已有的重要工作（尤其是没被引用的相关文献）相比如何？

### Reproducibility & Trust
42. 如果独立团队重复这项研究，有多大把握能得到相同结论？
43. 数据和代码是否可获取？如果不可获取，如何评估可信度？
44. 是否有利益冲突或资助来源可能影响研究结论？

### Personal Relevance (if user filled Q5)
45. 这项研究的方法/结论对我的研究有什么启发？
46. 我的研究中是否存在本文提到的局限性？

---

## Severity Flagging

When presenting questions, optionally tag severity:

| Flag | Meaning | Example |
|------|---------|---------|
| 🔴 | 如成立，可能推翻主要结论 | 样本量不足以支撑统计推断 |
| 🟡 | 影响对结论的信任程度 | 未讨论替代解释 |
| 🟢 | 值得思考，但不影响核心结论 | 推广性边界可以更清晰 |

---

## Application Rules

1. **Select, don't dump.** 3-5 questions per section max. Too many overwhelms.
2. **Prioritize by relevance.** Choose questions that match the paper's methodology and claims.
3. **Adapt wording.** Tailor generic questions to the paper's specific context.
4. **Don't answer.** These are reader prompts, not analysis. The reader engages with them.
5. **Place in MD notes**, not in PDF annotations.
6. **For Quick and Standard modes**, skip entirely. Only Deep mode.
