# 机器人视频突发丢帧下的时间间隔感知递归点跟踪

9 页计算机视觉课程开题演示文稿。

## 文件
- `motion_irregular_time_tapnext.pptx`：可编辑标题、正文、公式文本和原生表格
- `motion_irregular_time_tapnext.pdf`：阅读预览
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
官方 TAPNext++ 未修改代码，完成 TAP-Vid DAVIS 的 bike-packing 视频固定单点、前16帧 CPU 推理。仅15个全可见评测点，证明运行可行性；不代表完整benchmark、丢帧或重检测性能。拟议时间间隔校正尚待实验。

## 素材来源
TAPNext Figure 2 引自 Zholus 等人的 ICCV2025 官方论文，保留作者署名。实际结果图来自 TAP-Vid DAVIS 官方归档；点标注为 CC BY 4.0，原视频所有权归创作者，使用各创作者的许可，未独立复核该 YouTube 视频的精确许可变体。结果图仅供科研结果说明，不重新发布原视频或完整数据集。
