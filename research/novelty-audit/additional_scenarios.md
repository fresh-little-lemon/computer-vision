# 新增真实场景选题审查

核验日期：2026-10-18。材料范围为作者论文、会议页面、官方仓库与官方数据入口。网络推理尚未在本组执行；代码检查、候选机制与实测结果分别记录。

## 结论

| 场景 | 2025–2026主会依据 | 当前决定 | 关键原因 |
|---|---|---|---|
| 来源不明广角照片的相机标定 | AnyCalib，ICCV 2025 | **正式候选，先验证缺口** | 未知相机族选择具有明确接口缺口；冻结网络后可研究几何约束，数据和权重完整 |
| 手机LiDAR异常返回传播 | PromptDA，CVPR 2025；DEPTHOR，ICCV 2025 | **淘汰原改法，保留轻量基线入口** | PromptDA++已改中位数归一化，DEPTHOR++已覆盖异常检测及阻止错误传播 |
| RGB–热红外异分辨率匹配 | MINIMA，CVPR 2025；AnyMatch，ECCV 2026 | **几何适配型备选，暂缓新算法立题** | 各向异性协方差传播和可微位姿学习已有PNEC系列；剩余场景差异待实测 |

这次新增检索形成一项正式候选、两项有资源但机制重合的备选记录。与之前的TAPNext不规则时间题合计，目前本组提供两项正式候选。独立JSON已给出会议类别、真实场景、近邻、数据、机制、消融与图源，便于制作PPT。

## 一、正式候选：面向来源不明广角照片的裁切一致相机模型选择

### 场景与研究问题

建筑巡检、房屋实景建模及网络照片重建经常使用缺少EXIF的图像。图像可能来自广角相机，也可能经过裁切和非等比缩放。后续去畸变与三维重建需要的是当前图像坐标系中的像素到射线映射。相机模型选错后，即使中心区域拟合良好，边缘也可能产生明显几何偏差。

AnyCalib通过预测射线场并拟合相机模型实现单图标定，已经支持裁切、拉伸和多种畸变模型。官方接口为 `predict(image, cam_id)`，由调用者指定相机族。新研究对象是**相机族未知时的选择及几何歧义**。[ICCV 2025论文](https://openaccess.thecvf.com/content/ICCV2025/papers/Tirado-Garin_AnyCalib_On-Manifold_Learning_for_Model-Agnostic_Single-View_Camera_Calibration_ICCV_2025_paper.pdf)、[官方接口](https://github.com/javrtg/AnyCalib/blob/main/anycalib/model/anycalib_pretrained.py)

拟回答的问题是：同一张自然图像经过已知数字变换后，多个预测射线场之间的一致性，能否帮助排除局部拟合好、边缘外推不稳定的相机族？合成裁切共享原始图像，属于相关观测；其作用应通过与等预算多尺度平均的对照验证。

### 理论与具体机制

网络保持冻结。对原图及两至三个非中心裁切预测射线场，记录裁切、缩放的精确像素变换。候选相机族包括pinhole、低阶radial、Kannala–Brandt及UCM。各视图内参通过已知图像变换绑定，在共同可见区域联合求解少量几何参数。

模型评分包含空间留出区域的射线角残差、跨裁切一致误差与复杂度项，并检查正焦距及可见域径向投影单调性。留出区域避免用同一批像素同时拟合和评价。若多个相机族在可见区域内形成近似相同的射线映射，则保留模型歧义，优先报告几何精度。

这里的候选创新是“预测射线的数字变换一致性如何约束未知相机族选择”。BIC、物理约束和裁切等变性均有既有基础，作为对照与组成部分使用。

### 近邻覆盖

- **Generalized Camera Calibration，IEEE Sensors Journal 2025**已经研究多张标定图像上的BIC相机模型选择。它是自动选模的直接前作；本题的观测来自一张自然图像及其数字变换。[作者机构论文页](https://pure.seoultech.ac.kr/en/publications/generalized-camera-calibration-camera-model-selection-and-calibra/)
- **Automatic Reproducible Camera Intrinsic Calibration，2026预印本**通过独立标定板图像选择畸变阶数，说明“加入验证集选阶数”已有覆盖。[作者论文](https://arxiv.org/abs/2609.10082)
- **Perspective Fields，CVPR 2023**已讨论编辑变换下的几何等变性；该性质作为本题的理论基础。[论文](https://arxiv.org/abs/2212.03239)
- **AnyCam-MCT，2026硕士论文**聚合多个真实视频帧的AnyCalib特征。其输入信息量与本题不同，且“增加跨帧Transformer”已有实现。[作者模型卡](https://huggingface.co/thekman17/anycam-mct)

### 实验设计与预期产物

首轮使用20–50张真实图像，固定候选相机族，在中心裁切、非中心裁切、窄视野及拉伸条件下检查选模一致性。参数开发与最终测试按原始场景、相机或序列分组，同一原图的裁切变体属于同一组。

主要指标为射线角误差中位数和尾部误差、边缘分区误差、相对焦距误差、主点误差、物理无效模型率及额外推理成本。已知相机族的AnyCalib作为oracle参考。直接对照包括单图最小残差、单图BIC、多裁切简单平均、等推理预算多尺度平均。消融分离一致性项、复杂度项与单调约束。

预期产物为训练自由的选模模块、按真实设备分组的评价脚本、跨裁切误差可视化，以及多模型近似等价时的诊断报告。算法收益由未知相机族、独立真实图像和同预算对照共同验证。

### 资源卡

| 项目 | 官方入口与状态 |
|---|---|
| 代码 | [javrtg/AnyCalib](https://github.com/javrtg/AnyCalib)，Apache-2.0 |
| 通用模型 | [anycalib_gen.pt](https://github.com/javrtg/AnyCalib/releases/download/v1.0.0/anycalib_gen.pt) |
| 编辑图像模型 | [anycalib_edit.pt](https://github.com/javrtg/AnyCalib/releases/download/v1.0.0/anycalib_edit.pt) |
| LaMAR2k | [官方2k子集](https://cvg-data.inf.ethz.ch/GeoCalib_ECCV2024/lamar2k.zip)，解压约400MB |
| LaMAR2k edited | [作者下载地址](https://drive.google.com/uc?id=1h2HThhQbvqZlMw0OdpF7Y73wodeZMmdj)，约224MB |
| MonoVO2k | [作者下载地址](https://drive.google.com/uc?id=18rQ-WZcxXogeBqMwWvSkxVVEmZ9C12BZ)，约445MB，归档许可待核 |
| 数据许可 | LaMAR为CC BY4.0，[官方数据许可说明](https://github.com/microsoft/lamar-benchmark) |
| PPT图源 | [官方方法图](https://raw.githubusercontent.com/javrtg/AnyCalib/main/assets/method.png) |
| 本次运行状态 | 已检查官方调用路径；CPU smoke脚本通过语法检查，网络推理待执行 |

官方路径仅要求Python≥3.10与PyTorch，xformers为可选项。骨干实际是DINOv2-L，默认推理面积约320²。当前10GB RAM环境先安排一张图；批量GPU推理可先按8–12GB卡规划，实际峰值与速度待测。首版冻结模型，缓存射线后在CPU上拟合几何参数。

```bash
git clone https://github.com/javrtg/AnyCalib.git
cd AnyCalib
python -m pip install -e .
python /workspace/shared/cv-project-proposals/novelty-audit/anycalib_cpu_smoke.py \
  --image PATH_TO_REAL_IMAGE --model anycalib_gen --camera pinhole \
  --out anycalib_smoke.json
```

上述为待执行清单。完整基准使用官方siclib评估入口；单图smoke记录实际设备、有限输出、优化状态、耗时与内存。

## 二、暂缓：手机LiDAR异常返回的局部传播控制

### 审查结果

PromptDA-Small具有轻量权重和手机RGB/ARKit深度样例，适合快速跑通。原始源码使用全局min/max归一化，异常极值可能改变整张图的输入与输出量程。这是可核验的机制问题，但后续直接竞品已覆盖初始改法：

1. **PromptDA++作者扩展论文**对不规则稀疏点使用token化，并改用中位数归一化。更换鲁棒统计与适配任意稀疏模式已属于后续工作。[官方扩展PDF](https://github.com/DepthAnything/PromptDA/blob/main/assets/paper.pdf)
2. **Prior Depth Anything，ICLR2026**通过像素尺度对齐、距离加权预填充和条件网络处理不同深度先验。[正式论文](https://openreview.net/forum?id=IROtFft9Q4)
3. **DEPTHOR，ICCV2025及DEPTHOR++**研究真实dToF异常；扩展版还加入无可学习参数的异常检测，以避免错误深度继续传播。这与“先识别坏提示，再限制传播”的提案直接重合。[DEPTHOR++论文](https://arxiv.org/abs/2509.26498)、[官方代码](https://github.com/ShadowBbBb/Depthor)

剩余值得诊断的是固定小模型预算下“去掉异常远值”与“保留真实远景”的取舍。当前尚缺超出上述方法的独立机制，因此保留复现资源，暂缓正式新算法题。

### 可执行资源

- [PromptDA官方代码](https://github.com/DepthAnything/PromptDA)
- [Small官方权重](https://huggingface.co/depth-anything/prompt-depth-anything-vits/resolve/main/model.ckpt)，25.1M参数，Apache-2.0。Large论文主结果与Small分开比较
- [真实RGB样例](https://raw.githubusercontent.com/DepthAnything/PromptDA/main/assets/example_images/image.jpg)、[ARKit深度样例](https://raw.githubusercontent.com/DepthAnything/PromptDA/main/assets/example_images/arkit_depth.png)
- [DIODE验证集](http://diode-dataset.s3.amazonaws.com/val.tar.gz)，2.6GB，MIT许可。它包含真实RGB和高质量深度；模拟手机提示污染的实验单列。[数据说明](https://diode-dataset.org/)

CPU调用应显式指定 `model_kwargs={"encoder":"vits"}`，因为源码构造器默认vitl；图像可先以392长边输入。当前requirements包含旧版torch和xformers，CPU环境需要兼容依赖组合。资源入口已核验，推理与耗时尚未实测。

评价保留AbsRel、RMSE、δ1及近中远分层误差；控制干净输入质量，同时量化错误提示带来的空间误差扩散。单纯改善旧版本归一化可作为工程修复和消融，不作为本次正式选题的独立创新。

## 三、备选：异分辨率RGB–热红外匹配的成像误差传播

### 场景与机制边界

双传感器巡检使用RGB与热红外图像估计相对位姿。不同像素尺寸、模糊方向和热纹理会产生不同的定位误差。MINIMA返回匹配坐标与标量分数；可研究将传感器分辨率及方向性定位误差传入后续几何求解。

但**PNEC，CVPR2022**已把各向异性定位协方差传播到对极几何；**Learning Correspondence Uncertainty，CVPR2023**进一步研究对称约束和通过位姿优化学习协方差。因此“局部相似度得到协方差，再做马氏距离加权”已有完整理论与实现。[PNEC官方代码](https://github.com/tum-vision/pnec)、[CVPR2023正式论文](https://openaccess.thecvf.com/content/CVPR2023/html/Muhle_Learning_Correspondence_Uncertainty_via_Differentiable_Nonlinear_Least_Squares_CVPR_2023_paper.html)

当前方案适合定位为**传感器成像误差的场景适配研究**：冻结同一组MINIMA对应点，经过真实缩放和反投影雅可比传播误差，比较各向同性、标量置信加权与现有PNEC。传感器特定改进的必要性由实验决定。

### 新强基线与数据协议

- **MINIMA，CVPR2025主会**是可执行基础，官方提供SP+LightGlue、LoFTR、RoMa、ELoFTR和XoFTR权重。[论文](https://arxiv.org/abs/2412.19412)、[仓库](https://github.com/LSXI7/MINIMA)
- **AnyMatch，ECCV2026**研究3D一致跨模态数据生成。其当前README仍写明默认使用MINIMA权重，新训练权重的独立发布入口待核；运行该默认脚本得到的是MINIMA初始化路径。[官方代码说明](https://github.com/MnYangs/AnyMatch)
- **XoFTR++，2026期刊**已覆盖跨模态特征增强、粗细注意力和金字塔设计。[正式论文](https://www.nature.com/articles/s41598-026-68975-9)
- **METU-VisTIR**提供六个真实场景及相机位姿，CC BY-NC-SA4.0。天气为晴/阴，定位为真实跨模态评价。其作者指出自动对焦可能使GT内参存在小误差，因此另做内参扰动敏感性分析。[官方数据入口](https://drive.google.com/file/d/1Sj_vxj-GXvDQIMSg-ZUJR0vHBLIeDrLg/view)、[数据说明](https://github.com/OnderT/XoFTR)

最低成本smoke可用作者MMIM仓库的[红外-光学图A](https://raw.githubusercontent.com/StaRainJ/Multi-modality-image-matching-database-metrics-methods/master/Multimodal_Image_Matching_Datasets/RemoteSensing/Infrared_Optical/IO1a.png)、[图B](https://raw.githubusercontent.com/StaRainJ/Multi-modality-image-matching-database-metrics-methods/master/Multimodal_Image_Matching_Datasets/RemoteSensing/Infrared_Optical/IO1b.png)及[标注](https://raw.githubusercontent.com/StaRainJ/Multi-modality-image-matching-database-metrics-methods/master/Multimodal_Image_Matching_Datasets/RemoteSensing/Infrared_Optical/IO1.mat)。此组属于遥感平面诊断，和METU相对位姿分开报告；仓库未列统一数据再分发许可。

[MINIMA-LightGlue权重](https://github.com/LSXI7/storage/releases/download/MINIMA/minima_lightglue.pth)适合CPU单对尝试。源码会选择CPU，但计时包装内两次无条件调用 `torch.cuda.synchronize()`；需增加CUDA设备判断并保存补丁diff。SuperPoint另有许可限制，代码Apache许可与其组件许可分别记录。[源码](https://github.com/LSXI7/MINIMA/blob/main/src/utils/data_io_sp_lg.py)、[许可说明](https://github.com/LSXI7/MINIMA#license)

```bash
python demo.py --method sp_lg --ckpt weights/minima_lightglue.pth \
  --fig1 IO1a.png --fig2 IO1b.png --save_dir results/smoke
```

匹配点、候选数量、RANSAC预算和随机种子固定后，报告相对位姿AUC@5/10/20°、对极匹配精度、失败率和端到端时间。平面样例另报重投影误差。当前尚未执行网络；GPU批量推理初步按8GB级卡规划，几何优化在CPU进行。

## 交付索引

- `additional_scenarios.json`：三场景机器字段，含明确正式/暂缓状态
- `topics/anycalib_crop_model_selection.json`：新增正式候选
- `topics/promptda_tof_outlier_propagation.json`：直接覆盖审查与复现入口
- `topics/minima_thermal_geometry.json`：几何适配型备选
- `topics/motion_irregular_time_tapnext.json`：此前正式候选，TAPNext ICCV2025主会与TAPNext++ CVPR2026 Findings分别标注
- `anycalib_cpu_smoke.py`：单图CPU运行入口；本次仅语法检查

