# 计算机视觉开题PPT合集

2026-10-18 · **9题，89页**（8份10页、1份9页）

本合集包含9份可编辑PPTX及对应PDF，便于一次下载。8项候选包含2项条件候选，另有1项机制诊断备选。

## 选题与文件

| 序号 | 选题 | 状态 | 页数 | 文件 |
|---|---|---|---:|---|
| 1 | 建筑立面复拍的重复数量感知匹配 | 候选 | 10 | [PPTX](01_loma_repetition/loma_repetition.pptx) · [PDF](01_loma_repetition/loma_repetition.pdf) |
| 2 | 机器人突发丢帧下的时间间隔感知跟踪 | 候选 | 9 | [PPTX](02_motion_irregular_time_tapnext/motion_irregular_time_tapnext.pptx) · [PDF](02_motion_irregular_time_tapnext/motion_irregular_time_tapnext.pdf) |
| 3 | 来源不明广角照片的裁切一致相机模型选择 | 候选 | 10 | [PPTX](03_anycalib_crop_model_selection/anycalib_crop_model_selection.pptx) · [PDF](03_anycalib_crop_model_selection/anycalib_crop_model_selection.pdf) |
| 4 | 复杂桌面背景下的目标文档去弯曲 | 条件候选 | 10 | [PPTX](04_d2dewarp_target_page/d2dewarp_target_page.pptx) · [PDF](04_d2dewarp_target_page/d2dewarp_target_page.pdf) |
| 5 | 室内数字化中的有限平面边界恢复 | 条件候选 | 10 | [PPTX](05_zeroplane_visible_boundaries/zeroplane_visible_boundaries.pptx) · [PDF](05_zeroplane_visible_boundaries/zeroplane_visible_boundaries.pdf) |
| 6 | 玻璃隔断场景中的多层表面连续解码 | 候选 | 10 | [PPTX](06_seegroup_surface_sets/seegroup_surface_sets.pptx) · [PDF](06_seegroup_surface_sets/seegroup_surface_sets.pdf) |
| 7 | 遮挡物体重定位的几何可观测概念选择 | 候选 | 10 | [PPTX](07_conceptpose_observable_concepts/conceptpose_observable_concepts.pptx) · [PDF](07_conceptpose_observable_concepts/conceptpose_observable_concepts.pdf) |
| 8 | 亮面商品拍摄的观测约束高光去除 | 候选 | 10 | [PPTX](08_unreflect_observation_constraint/unreflect_observation_constraint.pptx) · [PDF](08_unreflect_observation_constraint/unreflect_observation_constraint.pdf) |
| 9 | 少样本PCB微缺陷的Patch相位诊断与预算化复检 | 机制诊断备选 | 10 | [PPTX](09_subspacead_microdefect_phase/subspacead_microdefect_phase.pptx) · [PDF](09_subspacead_microdefect_phase/subspacead_microdefect_phase.pdf) |

## 阅读与编辑

- PPTX的标题、正文、公式文本和表格可编辑；原论文图及真实实验图保留为图片
- PDF适合直接阅读；逐页预览、素材、研究JSON、生成代码和实验证据保存在各题独立恢复ZIP中
- 本合集只收录PPTX/PDF和目录清单，不重复打包独立素材、渲染图或模型权重
- 中文排版采用Noto Sans CJK SC。缺少该字体时，建议先看PDF；编辑PPTX前安装同名字体以减少替换带来的排版变化
- 9份共89页均已完成渲染和视觉检查；页数、备注、ZIP完整性及文件SHA256已核对

## 研究与实际运行范围

- LoMa：真实HardMatch固定3对建筑图像；TAPNext++：DAVIS固定16帧、单个全可见查询点
- AnyCalib：LaMAR固定首张图像、已知pinhole相机族；SubspaceAD：Small/224，1张正常参考与2张测试图
- 以上运行用于基线可行性和小样本诊断，新增机制的收益仍需实验验证
- D2Dewarp和ZeroPlane保留条件候选状态；SeeGroup、ConceptPose和UnReflectAnything本次尚未完成模型推理
- TAPNext以ICCV 2025主会为依据；最新执行基线TAPNext++属CVPR 2026 Findings

## 保存位置

**PPTX、PDF、预览与恢复ZIP通过本次对话的原生附件交付。GitHub保存逐页内容、生成代码、研究说明与实验记录等文本源。** 本目录中的PPTX/PDF链接指向解压后的本地文件，不表示对应二进制文件已上传GitHub。

各题完整恢复ZIP的名称以及文本源目录见 `manifest.json`。
