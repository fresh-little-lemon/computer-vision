# 几何与成像新候选：2025–2026基线扩展审查

核验日期：2026-10-18。三题均已核作者论文、公开实现、模型入口和真实数据入口；当前状态为调研与研究设计，尚未下载模型或执行推理。每题附独立topic JSON与10页PPT内容规格。

## 建议顺序

| 顺位 | 题目 | 选择理由 | 第一阶段需要得到的证据 |
|---|---|---|---|
| 1 | SeeGroup：透明多层表面连续解码 | 多层几何问题明确，CVPR2026主会基线、真实CC0基准与官方评分齐全 | 真实重复层/边界错误是否具有可修正的空间结构 |
| 2 | ConceptPose：可观测概念选择 | 作者已在4060Ti16GB上推理，冻结模型条件清楚，预算与6D几何有明确关系 | 同K下几何支撑选择是否优于原文数量消融及简单选择 |
| 3 | UnReflectAnything：观测约束去高光 | 2026公开模型结合成像物理，真实成对数据可直接验证颜色与纹理 | 掩码内部未饱和通道能否提供稳定增益；数据归档许可需核读 |

三题的研究机制均为待检验假设。精度、显存和耗时表将分别记录本项目实测、作者论文报告和设备预算估计。

## 1. 玻璃隔断场景中的多层表面连续解码

**场景。** 室内AR展示人员拍摄玻璃隔断，希望虚拟标注能区分玻璃表面与玻璃后的物体，并保持相邻像素的遮挡关系一致。

**研究问题。** 在冻结SeeGroup且相同图像分辨率下，尺度归一的集合去重与遮挡感知邻域传输，能否提高LayeredDepth验证集Mixed quadruplet accuracy，同时减少不存在层的误报并保留薄玻璃边界？

**现有缺口。** 透明边界同时包含真实表面出现/消失与候选分量重复。逐像素层有效性选择难以显式约束相邻像素是否属于同一连续表面。该现象在公开模型上的发生频率是本课题第一阶段的测量对象。

### 基线、资源与许可

- 论文：[SeeGroup: Multi-Layer Depth Estimation of Transparent Surfaces via Self-Determined Grouping](https://arxiv.org/abs/2605.28735)，CVPR 2026 Oral；首稿2026-05-27，本轮阅读arXiv:2605.28735v1
- 作者：Hongyu Wen, Jia Deng
- [作者代码](https://github.com/princeton-vl/SeeGroup)；[本轮固定实现](https://github.com/princeton-vl/SeeGroup/tree/765cbe45f218553a146f8f887c09310c1e96998e)
- 模型：DINOv2 ViT-L / recurrent decomposition / four Laplace components
- 机制：将沿相机射线的多个表面表示成无序事件；循环分解生成Laplace分量，采用置换不变强度、覆盖和梯度损失。
- 许可：仓库 BSD-3-Clause；预训练依赖许可随作者仓库保留
- [模型/权重入口](https://huggingface.co/Hermera/SeeGroup/resolve/main/seegroup.pth?download=true)，4,266,170,584 bytes
  - 作者HF LFS对象SHA256：`c21ccdd1595fbf7bbf6045c5825314cae5d302ad95a9f862c1088bbc4d7b9c77`

### 输入输出及研究方法

输入：单张RGB图像；SeeGroup公开预训练权重；推理不输入深度传感器或真实层标签。
输出：每像素无序深度候选集合及层存在性；透明区域的前后遮挡关系与连续表面可视化。
评价范围：真实数据主要验证相对深度次序；米制距离和碰撞安全另需传感器校准。

数学对象：D_p={d_pi,b_pi}；令c_ij=|d_pi-d_qj|/s_I，求带未匹配代价的邻域集合最小传输；目标E=数据强度项+λ·边缘门控集合传输+μ·层数复杂度。s_I为预测深度稳健尺度，统一处理正比例尺度变化。

**定位层数和边界错误。** 缓存四个深度分量、尺度参数与公开有效性输出；用真实tuple的不存在层标签、边界距离和层数分组定位错误。 预期检验：改进空间主要集中在分量重叠、玻璃边缘与多层交叠区域。

**构造无序集合解码。** 以归一化分量距离建立去重候选，邻域之间通过最小集合传输连接兼容表面；允许层出生和消失，RGB边缘调节连接代价。 预期检验：在不固定通道物理含义的条件下，连续表面的证据可减少重复层及孤立幻层。

**边界保留与尺度测试。** 在小规模开发集确定复杂度和边缘项；在固定留出验证图像上评估，并对预测深度整体正比例变换做等变性测试。 预期检验：集合约束提升跨层次序，同时不依赖图像的任意深度尺度。

### 最新近邻与直接比较

- [Seeing and Seeing Through the Glass / LayeredDepth](https://arxiv.org/abs/2503.11633)：ICCV 2025；2025-03-14首稿；作者代码和基准公开
  - 已覆盖：已经建立真实多层相对深度评估和多头预测基线。
  - 本题问题：冻结SeeGroup后，联合解码相邻像素的无序表面集合能否改善层存在性与跨层次序？
  - 比较协议：相同LayeredDepth tuple指标；作者原文测试All quadruplet为61.34%，SeeGroup为70.09%。
- [One Scene, Two Depths / Laplacian Visual Prompting](https://arxiv.org/abs/2606.29600)：ECCV 2026；2026-06-28首稿；官方代码公开
  - 已覆盖：通过RGB/Laplacian两次冻结模型推理探测前景玻璃与背景两种深度假设。
  - 本题问题：本题直接解码多层集合的空间连续性；两层输入变换作为独立方法对照。
  - 比较协议：原文DAv2-L的75.5% ML-SRA来自MD-3K两层稀疏序关系，与LayeredDepth quadruplet不直接换算。
- [SeeGroup原有覆盖损失与梯度损失](https://arxiv.org/html/2605.28735v1)：CVPR 2026公开基线内部机制
  - 已覆盖：已有重复分量抑制和局部平滑训练约束。
  - 本题问题：检验测试时、通道置换不变的邻域集合传输是否提供额外信息；增益须在原始解码与简单平滑之外成立。
  - 比较协议：同权重、同四分量、同推理分辨率，仅替换集合解码器。

### 真实数据、划分和下载

**[LayeredDepth真实数据](https://huggingface.co/datasets/princeton-vl/LayeredDepth)**
- [直接下载入口](https://huggingface.co/datasets/princeton-vl/LayeredDepth/resolve/main/data/validation-00000-of-00009.parquet)
- 规模：首个验证分片409,777,263 bytes；完整公开验证集300张/9分片；测试集1200张
- 划分：validation 300 / test 1200；真实测试标注由官方评测服务保留
- 实验样本：验证集按固定图像ID划分开发/留出组，分组清单随实验发布；课程核心离线评估使用公开validation。
- 许可：CC0-1.0，HF数据卡
- 版本记录：固定HF revision、图像ID与分片SHA256
- [评分入口](https://github.com/princeton-vl/LayeredDepth)

**[LayeredDepth-Syn](https://huggingface.co/datasets/princeton-vl/LayeredDepth-Syn)**
- [直接下载入口](https://huggingface.co/datasets/princeton-vl/LayeredDepth-Syn/resolve/main/data/validation-00000-of-00002.parquet)
- 规模：首个验证分片401,772,358 bytes；validation 500张
- 划分：只用synthetic validation作密集层边界与层数诊断
- 实验样本：固定100张分层样本；最终可扩500张
- 许可：BSD-3-Clause，HF数据卡
- 版本记录：固定revision和样本清单
- [评分入口](https://github.com/princeton-vl/SeeGroup)

### 指标、对照与消融

- 主指标：官方tuple-wise quadruplet/triplet/pair accuracy：All、Mixed和各层分别报告
- 辅助指标：不存在层tuple的误接受率；合成集层出现/消失边界F1与密集误差；每图延迟、峰值显存、尺度等变误差
- 对照：作者公开SeeGroup解码；论文峰值解码复现配置；阈值扫描；逐通道排序+边缘平滑；本题集合解码；相同权重
- 消融：去掉尺度归一；去掉邻域传输；去掉层出生/消失代价；去掉RGB边缘门控
- 协议：调参只用开发组；留出图像ID固定；真实数据报告序关系；合成数据报告密集误差；两层MD-3K跨数据集验证单列；公开test结果与自划验证结果分别列明
- 统计：按图像bootstrap置信区间，并检查改进是否以薄层漏检换取整体分数。

### 实施与最小推理命令

- 356M参数；原文Table4每forward CPU16.29s、GPU9.41s；该表硬件配置未在本轮核到
- 单张16GB级GPU、batch1、作者518输入尺度；实际峰值显存与时延待smoke测量
- 方案冻结网络；原文从头方案训练使用4×L40，本课题预算不包含该训练
- PyTorch/torchvision、OpenCV、mmengine、datasets、wandb等；官方model初始化调用CUDA。

以下为根据当前官方接口整理的执行步骤，实际环境安装与推理待实施。

```text
git clone https://github.com/princeton-vl/SeeGroup.git
cd SeeGroup && git checkout 765cbe45f218553a146f8f887c09310c1e96998e
pip install -r requirements.txt
bash scripts/download_seegroup_checkpoint.sh
python val.py --checkpoint-path checkpoints/seegroup.pth --max-samples 2 --num-workers 0
```

- 1 基线与错误图谱：2张GPU smoke后缓存公开验证预测；产物：命令、原始分量和错误分组表
- 2 集合解码原型：用小规模开发集实现无序传输和边界门控；产物：可独立运行的后处理模块及单元测试
- 3 控制实验：固定留出集完成原始解码、简单后处理与消融；产物：定量表、失败样例与耗时显存报告
- 4 跨场景检验：有预算时扩展MD-3K或作者正式测试；产物：跨数据集结果及适用场景总结

内容文件：`topics/seegroup_surface_sets.json`。PPT内容规格：`cv-decks/topics/seegroup_surface_sets.slides.json`。

## 2. 面向遮挡物体重定位的几何可观测概念选择

**场景。** 桌面物体重新摆放后，操作人员用一张已存RGB-D参考图，在物体部分被遮挡的情况下恢复它的相对位置与朝向。

**研究问题。** 对K=5/10/15的查询概念预算，基于参考RGB-D三维支撑和单部件失效的稳健可观测性选择，能否比随机、热图强度和纯语义多样性选择得到更好的ADD(-S)与旋转误差？

**现有缺口。** 固定类别概念会在不同物体上产生不同三维支撑。若热图集中在同一小部件，概念虽语义清晰，位姿旋转仍可能欠约束。原文已研究概念数量，本题进一步测量有限查询预算下的支撑互补性和遮挡后可观测性。

### 基线、资源与许可

- 论文：[ConceptPose: Training-Free Zero-Shot Object Pose Estimation using Concept Vectors](https://arxiv.org/abs/2512.09056)，CVPR 2026；首稿2025-12-09，本轮阅读arXiv:2512.09056v3，2026-04-12
- 作者：Liming Kuang, Yordanka Velikova, Mahdi Saleh, Jan-Nico Zaech, Danda Pani Paudel, Benjamin Busam
- [作者代码](https://github.com/StevenKuang/concept-pose)；[本轮固定实现](https://github.com/StevenKuang/concept-pose/tree/9b1deece942bb14373874c71033c841d146a3809)
- 模型：SigLIP2-giant-opt-patch16-384，FP16，类别概念库+3D配准
- 机制：把语义部件热图投影到RGB-D点云，为每点构造归一化概念向量，匹配后以RANSAC/Umeyama和ICP求位姿。
- 许可：ConceptPose代码MIT；SigLIP2模型Apache-2.0
- [模型/权重入口](https://huggingface.co/google/siglip2-giant-opt-patch16-384)
  - [权重分片](https://huggingface.co/google/siglip2-giant-opt-patch16-384/resolve/main/model-00001-of-00002.safetensors)
  - [权重分片](https://huggingface.co/google/siglip2-giant-opt-patch16-384/resolve/main/model-00002-of-00002.safetensors)

### 输入输出及研究方法

输入：一张参考RGB-D与一张查询RGB-D；相机内参、目标类别、两视图目标掩码；参考图可预先缓存概念热图；查询阶段最多K次概念热图计算。
输出：查询物体相对于参考的刚体变换R,t；被选概念、三维支撑范围及配准对应点。
评价范围：基准主协议使用GT mask隔离位姿误差；真实使用可由人工选区或已有分割提供mask。三维CAD只参与指标计算。

数学对象：把物体点坐标按中心和半径归一；每概念c产生信息近似A_c=Σ_p w_cp J_pᵀJ_p，J_p=[I,-[p]×]。选择|S|≤K以最大化min_{j∈S} log det(εI+Σ_{c∈S\{j}}A_c)，检验一个部件被遮挡时的几何冗余。

**缓存参考概念的三维支撑。** 用作者现有类别概念词表计算参考热图并投影点云；统计空间聚集、非共线程度及概念间重叠。 预期检验：语义多样性与几何互补性不完全一致。

**预算内稳健选择。** 使用归一化位姿信息矩阵和单概念失效目标贪心选择K个概念；查询图仅计算该子集，保持原RANSAC和ICP。 预期检验：同K下保留互补三维支撑可降低遮挡导致的旋转退化。

**真实遮挡和预算曲线检验。** 在固定RGB-D配对上比较K=5/10/15/20，按可见比例、重叠和对称性分组；参考预计算与在线查询耗时分开。 预期检验：性能增益主要来自几何可观测性，在线热图计算减少是否转化为时延下降由实测确定。

### 最新近邻与直接比较

- [UNOPose: Unseen Object Pose Estimation with an Unposed RGB-D Reference Image](https://github.com/shanice-l/UNOPose)：CVPR 2025；官方代码和训练权重入口公开
  - 已覆盖：单RGB-D参考、语义与SE(3)几何联合匹配已是成熟强基线。
  - 本题问题：冻结VLM、无任务训练条件下，概念查询预算如何转化成可观测位姿信息？
  - 比较协议：训练方法作为强精度参照单列；重跑时与本题统一mask、配对与指标。
- [OPT-Pose](https://arxiv.org/abs/2603.23370)：CVPR 2026；2026-03-24首稿；官方代码和rel_pose.pt公开
  - 已覆盖：通过物体中心三维表征进行单参考位姿估计。
  - 本题问题：本题研究显式可解释概念子集的免训练预算配置，不替换成训练位姿网络。
  - 比较协议：输入、mask和配对统一后列为有任务训练的精度/推理资源参照。
- [Learning Cross-View Semantic Priors / LCVSP](https://arxiv.org/abs/2606.22076)：2026-06-20 arXiv首稿；v2 2026-06-25；作者仓库说明代码、数据和模型将在论文接收后发布，当前主要为项目网页，未核到正式venue
  - 已覆盖：早期跨视图语义交互、结构保持与几何训练约束；明确处理大视角和噪声mask。
  - 本题问题：概念预算与遮挡后的几何可观测性是本题目标；跨视图注意力本身已有覆盖。
  - 比较协议：作者TableII同Oryon/Horyon RGB-D+GT mask协议报告REAL275 ADD(-S)86.2、ConceptPose71.5，均为作者报告；资源和训练设定分别列示。

### 真实数据、划分和下载

**[LINEMOD-Occlusion / BOP LMO](https://huggingface.co/datasets/bop-benchmark/lmo)**
- [直接下载入口](https://huggingface.co/datasets/bop-benchmark/lmo/resolve/main/lmo_test_all.zip)
- [补充归档](https://huggingface.co/datasets/bop-benchmark/lmo/resolve/main/lmo_base.zip)
- [补充归档](https://huggingface.co/datasets/bop-benchmark/lmo/resolve/main/lmo_models.zip)
- 规模：真实桌面遮挡场景，8个物体；下载体积以HF文件清单为准
- 划分：作者oneshot_lmo_full.yaml：1000对same_scene、seed42、BOP targets，固定生成的pair清单
- 实验样本：按物体ID和可见率分层选200对开发/留出；完整配置评估另列。
- 许可：CC-BY-SA-4.0，BOP HF数据卡
- 版本记录：固定HF revision、scene/image/object ID与pair清单
- [评分入口](https://github.com/thodan/bop_toolkit)

**[REAL275 + Oryon固定配对](https://github.com/hughw19/NOCS_CVPR2019)**
- [直接下载入口](http://download.cs.stanford.edu/orion/nocs/real_test.zip)
- [补充归档](http://download.cs.stanford.edu/orion/nocs/gts.zip)
- [补充归档](http://download.cs.stanford.edu/orion/nocs/obj_models.zip)
- [补充归档](https://github.com/jcorsetti/oryon/releases/download/v1.0.0-data/oryon_data.zip)
- 规模：真实测试RGB-D及标注；官方Oryon cross_scene_test 2000对
- 划分：与ConceptPose、LCVSP报告使用的Oryon/Horyon配对协议对齐
- 实验样本：2000对完整评估；开发用独立预定配对子集并单列
- 许可：NOCS代码MIT；数据归档许可单独待核，正式再分发前读取归档声明
- 版本记录：固定2000对文件和数据hash
- [评分入口](https://github.com/StevenKuang/concept-pose)

### 指标、对照与消融

- 主指标：ADD(-S) recall at 0.1 object diameter；对称性分层的旋转/平移误差
- 辅助指标：BOP AR：VSD/MSSD/MSPD；K–accuracy曲线与K–latency曲线；在线推理峰值显存；参考预计算独立计费
- 对照：原ConceptPose完整20概念；公开配置15概念；随机K；热图能量top-K；语义多样性K；几何可观测选择K；UNOPose/OPT-Pose有训练强基线单列
- 消融：去掉单部件失效稳健目标；去掉三维信息项；仅三维均匀采样；关闭ICP；固定K与相同实际壁钟预算分别比较
- 协议：同一SigLIP2、同mask、同pair、同RANSAC种子和迭代数；类别概念库固定；测试GT只用于评分和遮挡分组；主协议使用真实RGB-D；RGB-only wild demo另列；预计算与在线计算成本分开；训练成本另列
- 统计：关注低可见率与非对称物体；自然对称方向按BOP/ADD-S评估。

### 实施与最小推理命令

- 原文使用RTX4060Ti 16GB、48GB RAM，FP16；平均7.65秒/图对，体素化6.80秒/图对
- 单16GB GPU；参考概念可离线缓存；本题不训练VLM
- PyTorch、transformers、open3d、grad-cam、PyTorch3D（VSD渲染）；仓库已带基准类别概念缓存。

以下为根据当前官方接口整理的执行步骤，实际环境安装与推理待实施。

```text
git clone https://github.com/StevenKuang/concept-pose.git
cd concept-pose && git checkout 9b1deece942bb14373874c71033c841d146a3809
pip install -e . && pip install -r requirements.txt
pip install grad-cam
按作者安装指引配置与PyTorch/CUDA兼容的PyTorch3D，填写configs/datasets/lmo.json的数据路径
python test_oneshot.py --config configs/evaluations/oneshot_lmo_full.yaml --max_pairs 2 --device cuda --cpu-ransac
```

- 1 两对smoke与配对锁定：固定类别缓存、模型和RGB-D路径；产物：原始位姿、对应点、指标与时延日志
- 2 可观测性诊断：检验热图聚集是否伴随旋转退化；产物：概念三维支撑图和分组错误统计
- 3 子集选择原型：固定K实现几何与遮挡稳健目标；产物：选择器及消融开关
- 4 同协议比较：完成留出配对与强基线资源表；产物：准确率–预算曲线和失败边界

内容文件：`topics/conceptpose_observable_concepts.json`。PPT内容规格：`cv-decks/topics/conceptpose_observable_concepts.slides.json`。

## 3. 面向亮面商品拍摄的观测约束高光去除

**场景。** 商品摄影人员拍摄带印刷纹理的亮面包装，希望去掉反光时保留原有颜色和细小图案。

**研究问题。** 在冻结UnReflectAnything、相同高光掩码下，按通道饱和状态施加二色反射观测约束，能否在PSD真实图像上减少颜色与细纹理误差，同时保持高光消除效果？

**现有缺口。** 原文记录了非高光细节损失及平缓高光边缘的接缝。当前公开合成选项保留掩码外原图，而掩码内仍同时包含完整测量的未饱和通道和信息丢失的饱和通道，两者适合不同的重建约束。

### 基线、资源与许可

- 论文：[UnReflectAnything: RGB-Only Highlight Removal by Rendering Synthetic Specular Supervision](https://arxiv.org/abs/2512.09583)，CVPR 2026 Oral；首稿2025-12-10，本轮阅读arXiv:2512.09583v2，2025-12-11
- 作者：Alberto Rota, Mert Kiray, Mert Asim Karaoglu, Patrick Ruhkamp, Elena De Momi, Nassir Navab, Benjamin Busam
- [作者代码](https://github.com/alberto-rota/UnReflectAnything)；[本轮固定实现](https://github.com/alberto-rota/UnReflectAnything/tree/363ebb5c87d9f4f49b63f744fded8d3786a051b3)
- 模型：冻结DINOv3编码器、高光预测、token修复与漫反射解码
- 机制：利用单目几何合成镜面高光监督，通过高光定位和特征token修复产生漫反射图像。
- 许可：项目代码MIT；DINOv3预训练部分另见仓库LICENSE_DINO.txt与模型许可
- [模型/权重入口](https://huggingface.co/AlbeRota/UnReflectAnything/resolve/main/weights/full_model_weights.pt)，3,441,741,454 bytes
  - 作者HF LFS对象SHA256：`12c0cf4518a39325b7bfe2bed04a96395189f2643c2f90b7b79360a659dc739b`

### 输入输出及研究方法

输入：单张普通RGB图像；UnReflectAnything公开权重。
输出：去高光的漫反射图像；像素级高光残差与饱和区域标记。
评价范围：核心对象为不透明电介质亮面材质；透明折射、金属彩色镜面和完全饱和区域单独分析。

数学对象：近似线性RGB中I=clip(D+s·l)，s≥0，l为局部照明色度。优化D对冻结先验D0的偏离、未饱和通道的测量残差、饱和通道的单侧截断损失，以及可见纹理梯度一致性。

**分离可观测颜色与截断颜色。** 保存原始RGB、作者高光图和漫反射预测；逐通道识别饱和，按高光强度与边缘平缓程度分层。 预期检验：同一高光区域内仍有未饱和通道携带可利用的颜色与纹理信息。

**观测约束残差重建。** 以预测D0为先验，在局部共享照明色度下估计非负镜面残差；未饱和通道使用稳健等式残差，饱和通道使用单侧下界。 预期检验：观测约束减少生成先验对可见细节的改写。

**验证边缘与颜色保留。** 对照作者composite、简单混合、传统二色分解和StableDelight；固定掩码与尺寸，分别统计高光内部、边界、外部。 预期检验：收益来自掩码内部的测量利用，而非仅扩大原图保留范围。

### 最新近邻与直接比较

- [One-Step Specular Highlight Removal with Adapted Diffusion Models / ProbLoRA](https://openaccess.thecvf.com/content/ICCV2025/papers/Atmis_One-Step_Specular_Highlight_Removal_with_Adapted_Diffusion_Models_ICCV_2025_paper.pdf)：ICCV 2025；CVF全文公开，作者代码与权重本轮未核到
  - 已覆盖：SD-Turbo单步生成和ProbLoRA适配已能进行高光去除。
  - 本题问题：利用仍可观测的未饱和通道，约束生成先验对颜色与纹理的修改。
  - 比较协议：原文数字受数据划分、分辨率和掩码定义影响；同协议实现后进入定量表。
- [StableDelight](https://github.com/Stable-X/StableDelight)：作者公开代码与Torch Hub模型；仓库未标正式会议
  - 已覆盖：单步扩散、多尺度SSIM和随机条件尺度已覆盖纹理锐度增强。
  - 本题问题：本题把RGB测量作为显式约束，与仅优化感知或结构相似性的路线比较。
  - 比较协议：同一PSD留出图像、统一尺寸与色彩空间，资源成本单列。
- [UnReflectAnything当前composite选项及2026 MM-SHR](https://github.com/alberto-rota/UnReflectAnything/blob/main/endpoints/model_.py)：作者源码已有掩码外原图合成；MM-SHR发表于Optics & Laser Technology 2026
  - 已覆盖：原图合成已经保留掩码外区域；MM-SHR使用频率和注意力结构改善亮度及过处理。
  - 本题问题：研究掩码内部、未饱和通道的观测一致性及饱和通道的截断约束。
  - 比较协议：必须包含公开composite与阈值/膨胀半径扫描；MM-SHR来源https://doi.org/10.1016/j.optlastec.2026.115171。

### 真实数据、划分和下载

**[PSD / Paired Specular-Diffuse](https://github.com/jianweiguo/SpecularityNet-PSD)**
- [直接下载入口](https://drive.google.com/file/d/1PUrUyUd1ys6pue8jPGchCGVdFBAf8eqg/view?usp=sharing)
- 规模：作者提供13,380张真实图像，2,210个场景；1,010组固定偏振角序列和1,200组随机偏振图像对
- 划分：按物理场景ID隔离开发与留出组；作者公开标准test清单若归档含有则单独沿用
- 实验样本：先选不透明亮面材质的100个固定留出场景，再扩完整适用测试组
- 许可：作者公开下载；仓库README未见独立数据许可证，使用及再分发条款待归档说明核验
- 版本记录：记录归档hash、场景ID、图像对和排除材质清单
- [评分入口](https://github.com/jianweiguo/SpecularityNet-PSD)

### 指标、对照与消融

- 主指标：PSNR与SSIM：全图、高光内、边界带、掩码外分别报告；ΔE00颜色误差与可见纹理边缘保留
- 辅助指标：高光残差能量；亮度与色偏分组；单图延迟和峰值显存
- 对照：作者原始diffuse输出；作者composite输出；阈值与膨胀半径扫描；简单线性混合/Poisson融合；传统二色反射分解；StableDelight
- 消融：统一等式约束与按饱和状态分开约束；白光假设与局部照明色度；去掉先验D0；去掉可见纹理梯度项；线性RGB与直接sRGB计算
- 协议：所有方法相同RGB输入和图像对；掩码阈值在开发集选择；真实高光评价掩码单独固定；同一色彩空间和数据范围计算指标；参考漫反射由偏振采集得到，其残余误差在案例分析中记录
- 统计：按场景bootstrap置信区间，并单列近白漫反射、彩色照明和完全饱和失败组。

### 实施与最小推理命令

- 公开权重3.44GB；拟单16GB GPU、batch1、模型默认约448输入。实际显存/速度待测；官方CLI另有CPU选项。
- 第一阶段冻结模型，仅优化轻量观测约束模块
- Python>=3.11；PyTorch/transformers等按官方包安装，作者使用Python3.12。

以下为根据当前官方接口整理的执行步骤，实际环境安装与推理待实施。

```text
git clone https://github.com/alberto-rota/UnReflectAnything.git
cd UnReflectAnything && git checkout 363ebb5c87d9f4f49b63f744fded8d3786a051b3
pip install -e .
unreflectanything download --weights
unreflectanything inference /path/to/psd_input.png -o output/ --device cuda --batch-size 1
CPU接口测试可将--device cuda改为--device cpu，耗时与内存尚未实测
```

- 1 真实图像推理：两张PSD图像跑通公开权重，保存原始预测；产物：原图/高光/漫反射和资源日志
- 2 观测模型诊断：核验未饱和残差与颜色误差的关系；产物：高光分组及模型适用性分析
- 3 约束求解原型：实现先验引导的截断观测优化；产物：独立后处理模块和物理约束测试
- 4 同协议对照：完成留出真实场景和消融；产物：区域指标表、失败样例与商品图像演示

内容文件：`topics/unreflect_observation_constraint.json`。PPT内容规格：`cv-decks/topics/unreflect_observation_constraint.slides.json`。

## 实施前核验项与作者报告摘记

### SeeGroup

- [作者论文Table1](https://arxiv.org/html/2605.28735v1)的真实LayeredDepth test，All Q/T/P为70.09/74.88/82.62%；Layer1 Q=72.73%，Layer5 Q=60.21%。这些结果支持分层评估的必要性，具体错误原因仍由公开模型诊断确定。
- 论文推理说明采用峰值检测并抑制间隔小于0.02的深度。当前[公开头部](https://github.com/princeton-vl/SeeGroup/blob/main/model/seegroup.py)输出四个深度分量和尺度参数，[公开评价](https://github.com/princeton-vl/SeeGroup/blob/main/dataset/__init__.py)使用valid_mask阈值。实验保留“公开实现解码”和“论文峰值解码”两个明确配置，所有新增解码共享同一模型输出。
- 官方模型初始化当前调用CUDA。论文有CPU耗时报告，CLI的CPU执行路径待适配测试；GPU两图测试从官方val.py开始。checkpoint约4.27GB，实际加载内存高于裸权重大小，主机RAM也要记录。

### ConceptPose

- [作者原文](https://arxiv.org/html/2512.09056v3)默认20个概念，公开yaml默认15。本题并列保留15/20原始设置，再比较同K选择。LMO公开配置为1000对same-scene、seed42，使用BOP targets及GT masks。
- [LCVSP TableII](https://arxiv.org/html/2606.22076v2)在同Oryon/Horyon RGB-D+GT mask配对上报告：REAL275 ADD(-S)为LCVSP86.2%、UNOPose84.4%、ConceptPose71.5%。这些是作者报告的准确率，训练和硬件成本分列；本项目关注冻结模型/概念查询预算，不用该表推导相同资源结论。
- [LCVSP作者仓库](https://github.com/chenjiahongbq/LCVSP)目前说明代码、数据、预训练模型将在接收后发布；已核论文页未注明正式会议。它作为最新相关工作与报告值参照，现阶段可执行强对照选UNOPose或OPT-Pose。
- 当前安装文件未完整列出源码所用grad-cam，最小步骤已补上。VSD渲染使用PyTorch3D，需要与本机PyTorch/CUDA匹配。基准类别概念缓存随仓库提供，跑这些类别可直接读取缓存。任意新类别的自动概念生成另有Gemini调用依赖。
- [LMO数据卡](https://huggingface.co/datasets/bop-benchmark/lmo)明确CC-BY-SA-4.0。NOCS仓库MIT是代码许可，REAL275归档的单独数据声明待读取。

### UnReflectAnything

- [作者HF当前weights目录](https://huggingface.co/AlbeRota/UnReflectAnything/tree/main/weights)已有full_model_weights.pt，3,441,741,454 bytes。当前作者加载器支持checkpoint内嵌config；旧README中尚未提供权重的说明与当前文件状态不同，本轮以实际文件元数据和当前加载器为准。
- [当前forward接口](https://github.com/alberto-rota/UnReflectAnything/blob/main/endpoints/model_.py)已有composite=True，按预测掩码合成原图。因此直接原图粘贴作为基线，新机制聚焦掩码内未饱和测量及饱和通道截断。
- [原文Table1](https://arxiv.org/html/2512.09583v2)PSD结果中，UnReflectAnything PSNR17.230、SSIM0.911，DHAN-SHR PSNR24.863、SSIM0.868。指标呈现不同取舍，实验将核对掩码MSE、全图PSNR与结构指标的实现并分区报告。
- [PSD作者仓库](https://github.com/jianweiguo/SpecularityNet-PSD)给出Google Drive归档入口，但README未列独立数据许可证；下载后读取归档中的使用说明，再确定可共享的演示素材。PPT当前使用模型作者公开方法图。
- [MM-SHR](https://doi.org/10.1016/j.optlastec.2026.115171)在2026年已研究频率/注意力与过处理问题。本题具体测试冻结预测的物理观测投影，而非笼统增加边缘或频率模块。多光源、金属镜面和折射会偏离局部二色模型，需要独立失败分组。

## 本轮未收为正式新题的线索

- MoGA：官方评估需MoGA自身checkpoint，本轮只核到原SAM2权重和训练流程，尚未核到作者训练好MoGA权重，因此未生成正式topic。
- RobustPVOS：曾作高效视频分割线索检索，本轮优先保留与现有TAP方向差异更明显的几何与成像三题。

## 文件与执行状态

三份topic JSON和三份10页slidespec均通过JSON解析与素材路径存在性检查。没有安装这些新模型，没有下载这些权重，没有生成新方法跑分。PPT的渲染与版面检查由展示文稿制作流程完成。
