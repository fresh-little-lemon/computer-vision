# 面向建筑立面复拍的重复数量感知匹配

基于 LoMa 的类级归一化与几何分配研究。10 页开题演示文稿。

## 文件
- `loma_repetition.pptx`：可编辑正文、公式文本和原生表格
- `loma_repetition.pdf`：便于快速阅读的预览
- `previews/`：逐页 PNG 和总览图
- `source/topic.json`：研究信息与一手来源
- `source/slides.json`：逐页内容、版式和备注来源
- `source/build.mjs`：ArtifactTool JavaScript 制作源码
- `assets/`：来源明确的论文图与真实图像，授权见 `credits.json`
- `evidence/`：对应 PPT 小样本实跑的摘要和资源记录

## 编辑与再生成
在已提供 `@oai/artifact-tool` 的 Node.js 环境中安装 Noto Sans CJK SC 字体，在本目录运行：

`node source/build.mjs source/slides.json revision-name`

输出进入新的 `generated/` 子目录。外部论文图保留为图片，标题、正文、公式文本和表格可在 PowerPoint 中编辑。PDF预览由PPTX转换获得。

## 实验范围
LoMa-B128 对固定的三对 HardMatch 验证图像完成 CPU 推理。第 8 页同时展示真实失败案例与三对样本的独立分数。完整测试和拟议方法的实验仍待开展，解析算子示例不属于实测结果。

## 图像授权
LoMa 论文 Figure 2 为 CC BY 4.0。第 2 页图片为 Kai NeSmith 的 CC BY 4.0 图像。第 8 页图片由 Михайло Потупчик 与 Secret ua 的 CC BY-SA 4.0 图像叠加真实 GT 几何残差得到，该派生图继续使用 CC BY-SA 4.0。原作者、图像直链和许可证见 `assets/credits.json` 及相关页备注。
