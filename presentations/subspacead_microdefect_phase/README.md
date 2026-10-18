# 少样本PCB微缺陷检测：面向Patch采样相位的残差保留与预算化复检

10 页计算机视觉课程开题演示文稿。

## 文件
- `subspacead_microdefect_phase.pptx`：可编辑标题、正文、公式文本和原生表格
- `subspacead_microdefect_phase.pdf`：阅读预览
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
机制诊断备选。已使用官方Small/224配置在VisA PCB1的1张正常参考和2张固定测试图完成CPU推理。仅用于运行可行性与定性诊断；不代表论文Giant/672配置或完整数据集表现。Patch相位效应及预算化复检收益尚待对照实验验证。

## 素材来源
真实样本来自VisA (Zou等，2022)，数据CC BY 4.0。输入/标注/真实官方模型输出仅缩放、排图与着色；两张热图共享原始色阶。官方论文图为作者成果示意，来源见各页备注及assets/credits.json。
