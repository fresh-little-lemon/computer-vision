# 面向遮挡物体重定位的几何可观测概念选择

10 页计算机视觉课程开题演示文稿。

## 文件
- `conceptpose_observable_concepts.pptx`：可编辑标题、正文、公式文本和原生表格
- `conceptpose_observable_concepts.pdf`：阅读预览
- `previews/`：逐页 PNG 和总览图
- `source/topic.json`：研究内容与来源
- `source/slides.json`：逐页内容、版式与备注来源
- `source/build.mjs`：ArtifactTool JavaScript 制作源码
- `assets/`：来源明确的论文图与数据例图，见 credits.json
- `evidence/`：本次真实运行摘要（如有）

## 编辑与再生成
在已提供 `@oai/artifact-tool` 的 Node.js 环境中安装 Noto Sans CJK SC 字体，在本目录运行：

`node source/build.mjs source/slides.json revision-name`

输出写入新的 `generated/` 子目录。外部论文图保留为图片；标题、正文、公式文本和表格为可编辑元素。PDF由PPTX转换获得。

## 研究与实验范围
研究计划，尚未完成本次模型推理。拟议方法及性能收益均为待检验假设。 LMO额外同场景遮挡协议与Oryon跨场景协议分开统计；冻结模型，比较固定K和相同计算预算。

## 素材来源
使用原论文作者公开的真实场景示例和方法图，各图来源见assets/credits.json及相关页备注。所有作者图均为原论文示例，不是本次运行结果；不包含模型权重或完整数据集。
