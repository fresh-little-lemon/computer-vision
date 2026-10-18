# 面向来源不明广角照片的裁切一致相机模型选择

10 页计算机视觉课程开题演示文稿。

## 文件
- `anycalib_crop_model_selection.pptx`：可编辑标题、正文、公式文本和原生表格
- `anycalib_crop_model_selection.pdf`：阅读预览
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
AnyCalib-gen 官方未改模型完成 LaMAR2k 首条真实图像的 CPU 标定，已知相机族为 pinhole。2.592秒前向、峰值2759MiB；完整原分辨率上最大相对焦距误差2.454%、拟合相机平均射线角误差0.454°。这一单图结果未验证未知相机族选择或裁切一致性，拟议改进效果仍待实验。

## 素材来源
图片来源见 assets/credits.json 和相关页备注。论文作者图用于研究介绍，保留原作者署名；图片不构成本项目实验结果。
