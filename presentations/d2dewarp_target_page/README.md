# 复杂桌面背景下的目标文档去弯曲：基于页面条件化线图与拓扑约束的D2Dewarp改进

10 页计算机视觉课程开题演示文稿。

## 文件
- `d2dewarp_target_page.pptx`：可编辑标题、正文、公式文本和原生表格
- `d2dewarp_target_page.pdf`：阅读预览
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
条件收录的研究计划。官方 D2Dewarp 论文 Figure 7 提供复杂背景失败案例；当前尚未运行基线或拟议方法，页面线图与残差变形的效果待实验检验。四周为拟定研究安排。

## 素材来源
图片来源见 assets/credits.json 和相关页备注。论文作者图用于研究介绍，保留原作者署名；图片不构成本项目实验结果。
