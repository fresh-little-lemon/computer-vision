# 新候选：机器人视频突发丢帧下的时间间隔感知递归点跟踪

## 当前判断

这是值得做首轮实测的新候选，研究对象从遮挡恢复转为**不规则图像到达导致的递归状态失配**。目前完成论文、官方源码及下载入口核验；首轮真实视频运行交由实测结果决定是否入选。

论文依据为 **TAPNext，ICCV 2025 主会**；当前优先运行的强基线为 **TAPNext++，CVPR 2026 Findings**。会议类别在提交材料中分别标注。[TAPNext 正式论文](https://openaccess.thecvf.com/content/ICCV2025/papers/Zholus_TAPNext_Tracking_Any_Point_TAP_as_Next_Token_Prediction_ICCV_2025_paper.pdf)、[TAPNext++ 正式论文](https://openaccess.thecvf.com/content/CVPR2026F/html/Jung_TAPNext_Whats_Next_for_Tracking_Any_Point_TAP_CVPRF_2026_paper.html)

## 实际场景与可核验问题

远程机器人视觉、无线相机传输及算力共享会形成连续帧缺失。递归跟踪器实际收到的相邻图像可能相隔 1、2、4 或更多原始帧，调用次数与经过时间不再一致。官方 PyTorch 实现的 RG-LRU 以一次调用作为一步，短时卷积缓存保存最近固定数量的特征；其接口尚未显式接收帧间时间间隔。这是源码事实。由此产生多大的实际精度下降，需要在真实视频上测量。[RG-LRU 与卷积源码](https://github.com/google-deepmind/tapnet/blob/main/tapnet/tapnext/tapnext_lru_modules.py)、[逐帧接口](https://github.com/google-deepmind/tapnet/blob/main/tapnet/tapnextpp/votsp2026/model.py)

## 具体机制

1. **时间标尺进入记忆更新**：对相邻到达帧使用相对时间间隔 ρ=Δt/Δt₀，将递归保留系数的初始形式由 a 改为 a^ρ，同时一致修改输入归一化项。ρ=1 时恢复原计算，稳定性由 0<a<1 保持。该形式属于连续时间离散化的已有思想，拟研究的贡献是它在预训练视觉递归状态上的可迁移校正及与短缓存的联合处理。
2. **按真实时间整理短缓存**：每个缓存特征保存源时间戳，对卷积核按特征年龄取权重；较久未更新的缓存按时间衰减或退出支持区。每个到达图像仍只进行一次图像编码，缺失帧作为没有图像观测的时间间隔处理。
3. **小范围适配与采样一致性**：冻结图像编码及坐标头，先只适配末两层时间模块的小参数。用独立训练视频的完整因果序列输出作教师，在相同物理时刻约束稀疏采样分支的坐标分布与可见性。相同训练视频、相同丢帧增强而无时间机制的模型构成关键对照。

需要比较的技术假设很明确：丢帧增强是否已足够；独立修改 LRU 是否有效；卷积缓存按调用编号更新是否抵消 LRU 校正；联合方法是否只改变置信阈值而没有改进定位。

## 直接竞品与区别

- **TAPNext++** 研究长序列训练及重新检测；其原生时间模块与最终权重是首要基线。论文已研究静态图重复输入时的状态变化，也讨论可变深度，因此“记忆稳定”与“动态浅层推理”本身已有覆盖。[作者论文](https://arxiv.org/html/2604.10582v1)
- **Track-On-R** 研究跨跟踪器 verifier 与真实视频自训练。它是强跟踪基线；本候选的改动位于时间更新方程与短缓存，而非候选评分。[论文](https://arxiv.org/abs/2603.12217)、[代码](https://github.com/gorkaydemir/track_on)
- **EDCPT，ICCV 2025** 已研究低帧率和连续点轨迹，并在补充实验中比较跳帧设置。其完整方法使用 RGB 与事件；论文还含 image-only curve 消融。相关实验与其低帧率设置对齐，并将完整多模态方法单列。[主文](https://openaccess.thecvf.com/content/ICCV2025/papers/Wan_Event-aided_Dense_and_Continuous_Point_Tracking_Everywhere_and_Anytime_ICCV_2025_paper.pdf)、[低帧率消融](https://openaccess.thecvf.com/content/ICCV2025/supplemental/Wan_Event-aided_Dense_and_ICCV_2025_supplemental.pdf)
- **TAPFormer，2026 预印本** 通过帧与事件的异步融合处理连续运动及模态失效，提供了直接相关的问题背景。当前候选输入为 RGB 与采集时间戳，缺失区间没有事件观测。[论文](https://arxiv.org/abs/2603.04989)

此次定向检索发现上述近邻，尚未找到与“纯 RGB、突发缺帧、时间尺度化递归状态与短缓存联合校正”完全一致的实现。选题是否成立以强基线缺口和必要消融的实测结果为依据。

## 官方资源与最快运行路径

| 用途 | 官方入口 |
|---|---|
| 代码 | https://github.com/google-deepmind/tapnet |
| TAPNext++ 256² 权重 | https://storage.googleapis.com/dm-tapnet/tapnextpp/tapnextpp_ckpt.pt |
| 官方逐帧推理与 DAVIS 指标 notebook | https://github.com/google-deepmind/tapnet/blob/main/colabs/torch_tapnextpp_demo.ipynb |
| TAP-Vid DAVIS，真实视频与点轨迹测试包 | https://storage.googleapis.com/dm-tapnet/tapvid_davis.zip |
| RoboTAP，265 段真实机器人测试视频 | https://storage.googleapis.com/dm-tapnet/robotap/robotap.zip |
| 独立适配素材：DAVIS 2017 trainval 480p | https://data.vision.ee.ethz.ch/csergi/share/davis/DAVIS-2017-trainval-480p.zip |
| DAVIS 官方下载说明 | https://davischallenge.org/davis2017/code.html |

DAVIS trainval 包中只使用官方 `train` 清单进行适配和内部验证；TAP-Vid DAVIS 对应验证视频保持测试用途。RoboTAP 全部作为外部测试。训练素材的分割标注不等同于点轨迹标注，伪标签由冻结教师生成并保存来源。原始视频素材的许可分别遵循数据集条款；tapnet 代码及其当前 README 所列预训练权重为 Apache 2.0，RoboTAP 视频和 TAP-Vid 点标注为 CC-BY 4.0。[官方许可说明](https://github.com/google-deepmind/tapnet#license-and-disclaimer)

已经准备 `tapnextpp_smoke.py`，读取官方 DAVIS 真实视频，取一个点和最多 16 帧，输出轨迹有效性、实际设备、同步耗时与显存峰值。以下命令是待执行清单：

```bash
python -m pip install git+https://github.com/google-deepmind/tapnet.git
python -m pip install git+https://github.com/google-deepmind/recurrentgemma.git@main
curl --fail --location --output tapnextpp_ckpt.pt \
  https://storage.googleapis.com/dm-tapnet/tapnextpp/tapnextpp_ckpt.pt
curl --fail --location --output tapvid_davis.zip \
  https://storage.googleapis.com/dm-tapnet/tapvid_davis.zip
unzip -n tapvid_davis.zip
python tapnextpp_smoke.py --checkpoint tapnextpp_ckpt.pt \
  --data tapvid_davis/tapvid_davis.pkl --frames 16 --out result.json
```

环境中的 PyTorch、torchvision 与 CUDA 组合需匹配；运行记录固定包版本和 Git 提交。官方 notebook 的 GPU 元数据为 T4，可据此先安排单卡 16GB、256²、单点的推理试验；这是一项资源安排估计，实际峰值和速度由 smoke 输出记录。短序列适配初步按单卡 24GB、16 帧、末两层时间模块规划，资源需求以梯度试跑为准。

## 首轮实测与决定条件

**运行关**：官方权重对真实 DAVIS 视频输出有限坐标、合法可见性与完整文件；另导出可视化检查坐标顺序。16 帧 smoke 只证明该配置可执行，标准性能复现使用完整视频及官方指标。

**问题关**：在 DAVIS 与 RoboTAP 的固定视频清单上生成同一组缺帧计划：固定间隔、随机独立丢帧及突发缺帧，保留每个点的查询帧。间隔使用原始帧编号差；有真实采集时间戳的补充视频再转换为毫秒。只在实际到达帧上评价 AJ、δ_avg、OA，另报告突发缺帧后的可见点定位误差与失效持续帧数。完整帧输入作为信息量上界单列。

**机制关**：比较原模型、相同增强的小参数适配、仅时间系数、仅缓存调整、联合调整；增加“重复上一帧填空”和“长间隔清空短缓存”两种低成本对照。所有方法使用相同到达帧、查询和前视约束，分别记录额外编码次数与时延。

**入选依据**：两个真实域均出现可重复的缺帧退化，联合机制优于增强及简单缓存对照，正常帧率性能保持在预设容差内。若原模型已经稳定，或优势完全由训练增强解释，则停止把它发展为新算法题，保留可复现实测结果。

## 三个近期 baseline 的可执行性比较

- TAPNext++：官方直接权重、真实小数据与逐帧 demo 完整，无需额外骨干访问；优先安排 smoke。正式类别为 CVPR 2026 Findings
- Track-On-R：CVPR 2026 主会，官方权重与接口存在；DINOv3-vits16plus 骨干需要独立授权访问，当前权重包未含该骨干。[官方模型卡](https://huggingface.co/gorkaydemir/track_on_r)
- LightStab：CVPR 2026 主会，推理与资源包已提供；训练材料仍待发布，当前 demo 含整段统一裁切及默认补边，逐帧输出协议需要单独核验。[官方仓库](https://github.com/liutao23/LightStab)
