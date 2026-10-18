# 几何视觉三题最新竞争审查

核验截止：2026-10-18。对象为此前三份几何项目的核心想法；本文件独立于原项目包。下列数值均为作者论文或仓库报告，本次未运行这些算法。会议论文、预印本和代码状态分别列示。

## 结论与排序

| 原选题 | 结论 | 主要依据 | 重新立项后的优先级 |
|---|---|---|---|
| LightGlue重复纹理配准可靠性 | **重构** | 最新匹配器已显著改善困难匹配；协方差、几何过滤和多平面细化已有直接工作。研究对象应转向重复结构中的多解匹配，而非分数融合 | 1 |
| RAFT-Stereo可靠测量区域 | **重构，有设备条件** | 实时零样本双目已更新至Fast-FoundationStereo、LAS系列；像素置信与区间估计已有成熟研究 | 2；需要真实标定与独立尺寸真值 |
| 少量含噪点校准DAv2 | **淘汰原主线** | 2026-07的MRAC直接覆盖冻结DAv2、5–200点、稳健scale/shift、局部残差及多种传感器离群值 | 不进入当前候选 |

用户希望改从最新会议基线出发，新候选与下载、启动信息另见[geometry-new.md](geometry-new.md)。旧题1、2的“重构”表示研究问题与实验体系需要重新设计。

## 1. 重复纹理平面配准：问题仍在，原方法组合已偏弱

### 最新直接竞争与覆盖

**LoMa，ECCV 2026 Oral。** Nordström等，首版2026-04-06，作者仓库2026-06-18公告接收。推理、模型和评估代码已公开。与其只比较2023年的LightGlue，更有判断力的起点是同为稀疏匹配的LoMa-B/B128。作者仍明确列出HardMatch中的Doppelgängers和极端视角为困难情形。[论文](https://arxiv.org/abs/2604.04931)、[作者代码](https://github.com/davnords/LoMa)

LoMa论文附录表8使用LoFTR式HPatches协议，报告以下**同表**单应AUC；它比跨任务引用HardMatch更接近原题：

| 方法 | AUC@3px | @5px | @10px |
|---|---:|---:|---:|
| ALIKED+LightGlue | 66.2 | 76.9 | 86.3 |
| LoMa-B128 | 67.2 | 78.1 | 87.8 |
| LoMa-B | 66.5 | 77.5 | 87.3 |

这里没有出现“新模型彻底碾压HPatches”的证据。相反，困难场景才有较大区分度：项目页同表HardMatch mAA@10px为35.7→54.3（ALIKED+LightGlue→LoMa-G）。该指标是估计基础矩阵后对人工对应点评分，不是单应角点误差。公开HardMatch还替换了约10对有许可问题的图像；现仓库默认LoMa示例是0.5061，测试版本应单独记录。[HPatches表及协议](https://arxiv.org/html/2604.04931v2#A1.SS3)、[项目表](https://www.davnords.com/loma)、[公开数据说明](https://github.com/davnords/HardMatch)

**RoMa v2，ECCV 2026。** Edstedt等，首版2025-11-19，2026-07-06为v3。作者代码和预训练模型已公开；输出稠密对应、重叠置信及二维像素精度矩阵。协方差训练限定于可共视且残差小于8px的区域。因此“给匹配加不确定度”已有很近的基线，而“多个相隔一周期的全局解如何共存”仍是不同问题。[论文](https://arxiv.org/abs/2511.15706)、[代码](https://github.com/Parskatt/romav2)、[协方差定义](https://arxiv.org/html/2511.15706v3)

**MiHo/MOP/NCC，首版2024-11-14。** Bellavia等已将多平面几何过滤、双向重投影、对称单应归一化和相关性细化组合为模块化匹配后处理；作者代码公开。这与原题中的双向残差及几何一致性直接重叠。**RaCo，首版2026-02-17**进一步将关键点排序与定位协方差纳入学习特征。它们分别构成几何后处理和不确定度建模的近邻。[MiHo论文](https://arxiv.org/abs/2411.09484)、[MiHo代码](https://github.com/fb82/MiHo)、[RaCo论文](https://arxiv.org/abs/2602.15755)、[RaCo代码](https://github.com/cvg/RaCo)

### 剩余值得研究的窄问题

**进一步审查发现，泛化的“保留多候选再消歧”也已有直接工作。** Jiang、Li、Wu的Preserve, Then Resolve首版2026-04-26、v3为2026-08-30，已公开top-k多对多关联、HCM/MCM图感知LO-RANSAC及概率边权。[论文](https://arxiv.org/abs/2604.23670)、[作者代码](https://github.com/LIAS-CUHKSZ/preserve_then_resolve)

新候选因此收窄为**LoMa双softmax分数对重复实例数量的敏感性**：在描述子相似度和可见重叠关系受到控制时，增加相似候选是否仅因归一化分母变大就压低真实候选分数？研究重复等价类之间的总支持与类内几何分配，而将多候选求解作为已有工具。真实失效、超过阈值调节及PTR移植的收益均需通过预实验建立。

Doppelgangers++（CVPR2025）已研究基于MASt3R特征的图像对可共视分类；2026-10-01的MVDG预印本进一步使用VGGT多视图上下文。它们主要判断图像对是否应连接，和本题的局部候选归一化分别评价。[Doppelgangers++](https://openaccess.thecvf.com/content/CVPR2025/html/Xiangli_Doppelgangers_Improved_Visual_Disambiguation_with_Geometric_3D_Features_CVPR_2025_paper.html)、[MVDG](https://arxiv.org/abs/2610.01098)

最小比较应包含LoMa-B128/B、阈值扫描、恢复matchability、相同候选数的top-k+MAGSAC、PTR及MiHo，以及RoMa v2高质量参考。固定特征点上限、分辨率、RANSAC预算和端到端时延。HardMatch承担困难实景外部评价，HPatches承担标准平面回归检查；受控重复平面实验用于区分“可恢复但被早筛丢失”与“图像信息本身不足”。后者记录为多解情形。

**验证入口：**若数量偏置在真实数据上不显著，或阈值调节、PTR移植已解释全部收益，则该新候选不进入正式立项。

## 2. 双目可靠测量：算法基线必须更新，测量问题需要独立建立

### 最新直接竞争与覆盖

**Fast-FoundationStereo，CVPR 2026。** Wen、Dewan、Birchfield，首版2025-12-11，v2为2026-03-17。官方推理代码与研究权重已公开。论文表1在非遮挡像素评价，Middlebury-H BP2为2.20%，Q为2.12%；FoundationStereo同表为1.10%、1.30%。Middlebury-Q、RTX3090测得49ms与496ms。训练数据规模不同，比较的是现成零样本系统的部署表现。[论文与协议](https://arxiv.org/html/2512.11130v2)、[官方代码](https://github.com/NVlabs/Fast-FoundationStereo)

**Lite Any Stereo（LAS1），CVPR 2026；LAS2，2026-06-23预印本。** Jing等。作者仓库同时提供LAS1及LAS2-S/M/L/H推理、评价与权重。LAS2已成为Fast-FoundationStereo之外必须纳入的效率对照。[LAS1论文](https://arxiv.org/abs/2511.16555)、[LAS2论文](https://arxiv.org/abs/2606.24457)、[代码与权重入口](https://github.com/TomTomTommi/LiteAnyStereo)

LAS2论文表II在同一机器、同一指标下重新评价，FFS使用最快的20-30-48、4迭代配置：

| 方法 | Middlebury-H Bad2/% | EPE/px | H200时延/ms | Orin NX 8G/ms |
|---|---:|---:|---:|---:|
| Fast-FoundationStereo | 3.73 | 0.63 | 27.3 | 918 |
| LAS2-H | 3.71 | 0.61 | 15.1 | 344 |
| LAS2-M | 5.47 | 0.77 | 8.1 | 101 |
| FoundationStereo | 1.12 | 0.37 | 292.2 | OOM |

时延输入为384×1248，禁用torch.compile。由此可见，FFS在此设置上已不是效率边界；但其3.73%与自己论文2.20%来自不同checkpoint/协议，不能拼成一次回归结论。LAS2没有目标数据集微调，训练数据仍不与FFS等量。[同表结果与设置](https://arxiv.org/html/2606.24457v1)

**置信度已是主流研究对象。** Cai等《Uncertainty Quantification in Stereo Matching》首版2024-12-24，后以《Probabilistic Modeling of Disparity Uncertainty for Robust and Efficient Stereo Matching》发表于Pattern Recognition。其KITTI表报告EPE/AUSE/95%区间覆盖率，已有后验校准设计。Malinowski等2024-04-09提出基于可能性理论的视差置信区间。2026-07-07的URS-Stereo又以不确定度引导局部视差搜索，当前核验为预印本，未确认作者公开代码。[Cai等论文](https://arxiv.org/abs/2412.18703)、[区间论文](https://arxiv.org/abs/2404.06273)、[URS-Stereo](https://arxiv.org/abs/2607.06779)

### 旧设计与新问题的区别

左右一致性、多尺度差异、纹理强度、平面残差适合作为基础对照。单纯融合这些量输出可靠区域，研究空间较小。更具体的问题是：**当相机标定偏差形成空间相关误差时，像素级高置信能否转化为一次尺寸测量的可靠结论？** 同一物体的两端点共享焦距、基线和主点误差，独立像素误差传播可能误判尺寸区间。

重构后应围绕一个具体测量量，如两平行面的间距，研究共同标定扰动与局部匹配误差的联合传播、可辨识条件及测量方案。需要固定双目装置、已知长度或激光参考、留出的距离/姿态；与独立传播、空间分块重采样及已有视差区间比较。FFS与LAS2作为可替换深度前端，FoundationStereo为离线参照。

仅有Middlebury公开15对数据时，可完成视差与可靠区域实验，但不足以回答上述真实装置标定漂移问题。若没有装置或独立测量真值，本轮优先选择LoMa新候选。

## 3. 少点含噪校准：原主线淘汰

### 最直接的撞题证据

**MRAC，《The Multipath Blind Spot: K-Agnostic Robust Calibration for Sparse-Anchor Metric Depth from Frozen Foundations》**，Roy、Misra、Shastravidyananda、Maharaj，2026-07-05预印本。其设置为冻结DAv2、5–200个点、Theil–Sen与MAD筛点、仿射校准加局部残差，并研究多径、离群点、常值无回波与混合像素。与原题拟用的“极少点、有噪、稳健scale/shift、局部残差”高度重合。作者公开代码和权重本轮未核实。[论文日期及摘要](https://arxiv.org/abs/2607.04101)、[方法和实验](https://arxiv.org/html/2607.04101v1)

论文表II的同骨干对照，在50点、25%近偏置离群点下，DIODE AbsRel由B′的0.364降至MRAC/B′的0.267；该DIODE是含室内外的771图，不是原计划325张室内图。其残差头0.47M参数需要训练；“无重训”指MRAC筛选器，而非整个系统从未训练。其数值目前作为作者报告，撞题结论主要来自问题与方法覆盖。

### 其他强对照已经覆盖的范围

| 方法 | 日期与发表状态 | 已覆盖问题 | 公开情况与可比性 |
|---|---|---|---|
| PromptDA | CVPR 2025 | 低分辨率深度提示高分辨率度量深度 | [代码/权重](https://github.com/DepthAnything/PromptDA)；主要输入密度高于5–50点 |
| TestPromptDC | ICCV 2025 | 推理时稀疏观测驱动提示优化 | [论文](https://openaccess.thecvf.com/content/ICCV2025/html/Jeong_Test-Time_Prompt_Tuning_for_Zero-Shot_Depth_Completion_ICCV_2025_paper.html)、[代码](https://github.com/JinhwiPark/TestPromptDC)；需计入测试时优化成本 |
| Prior Depth Anything | 首版2025-05-15，ICLR 2026 | 任意深度先验、尺度对齐与局部细化 | [论文](https://arxiv.org/abs/2505.10565)、[ICLR论文](https://openreview.net/pdf?id=IROtFft9Q4) |
| CAPA | 首版2026-02-16，预印本 | 冻结模型的条件适配、鲁棒仿射对齐及噪声稀疏点 | [论文](https://arxiv.org/abs/2602.14751)、[作者项目](https://research.nvidia.com/labs/dvl/projects/capa/)；包含多帧共享适配，单帧协议另列；公开实现未核实 |
| Any2Full | 首版2026-03-05，v2为2026-07-10，ECCV 2026 | 不规则稀疏点、孔洞、范围限制等统一补全 | [论文](https://arxiv.org/abs/2603.05711)、[代码](https://github.com/zhiyuandaily/Any2Full)、[Small/Base/Large权重](https://huggingface.co/zhiyuandaily/Any2Full/tree/main/checkpoints)已公开 |

Any2Full论文表1的DIODE使用771图、640×480、0.1%随机稀疏输入：PriorDA和Any2Full-L的AbsRel均为0.022，OMNI-DC为0.017，Any2Full-S为0.023。该表不是5–50点噪声实验，不能拿这些数值和MRAC的0.267直接排序。Small提供了较接近原Small模型预算的强补全对照，参数之外仍应测总时延和显存。[完整协议与表](https://arxiv.org/html/2603.05711v2)

**结论：**原题的few/noisy/biased sampling切口已被覆盖，不继续作为创新主线。若未来研究锚点像素位置的系统性配准误差，应改成明确的传感器联合标定问题，另查误差变量模型、混合像素与真实dToF论文后重新立项。

## 评价证据的统一口径

1. 公平部署对照固定输入、目标数据划分、后处理、GPU、batch=1和端到端计时；预训练规模作为独立事实记录。
2. HPatches像素单应AUC、HardMatch基础矩阵mAA、相对位姿角度AUC分列。
3. Middlebury F/H/Q分辨率、all/nonocc、视差恢复尺度、checkpoint和迭代数完整记录。
4. 稀疏深度方法共用观测点及噪声实现，评价剔除输入点；单帧、多帧和RGB-only分别呈现。
5. 代码/模型链接存在、成功下载、单对前向成功、完整benchmark复现是四个不同阶段。本轮完成官方来源与接口核验；模型实测由后续日志补充。

2026年末刊期但在线日期未核实的论文未作为本轮决定性证据。原三题文档保持原样，新的选题决策以本次审查为准。
