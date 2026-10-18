# 室内数字化中的有限平面边界恢复：基于遮挡关系与投影交线的ZeroPlane改进

10 页计算机视觉课程开题演示文稿。

## 文件
- `zeroplane_visible_boundaries.pptx`：可编辑标题、正文、公式文本和原生表格
- `zeroplane_visible_boundaries.pdf`：阅读预览
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
条件收录的研究计划。基线尚未在本环境运行；官方权重约7.1GB，依赖GPU/CUDA算子。有限可见边界类型的作用仍是待检验假设，不归为作者已确认的室内失败。四周安排为拟定计划。

## 素材来源
使用ZeroPlane作者公开的输入样例与跨数据集结果图，具体来源见assets/credits.json及各页备注。所有作者图均为原论文示例，不是本次运行结果。
