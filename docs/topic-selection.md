# 计算机视觉课程选题总表

更新：2026-10-18。当前候选8项（含D2Dewarp与ZeroPlane两项条件收录），另有SubspaceAD机制诊断备选；备选与淘汰方向单列。所有拟议改进均处于机制设计或待验证阶段；已运行结果来自官方基线。

## 决策总表

| 编号 | 场景与选题 | 基线论文 | 基线实测状态 | 首轮资源 | 紧接着做什么 |
|---|---|---|---|---|---|
| C1 | 建筑立面复拍的重复数量感知匹配 | LoMa，ECCV2026 Oral | CPU真实3对完成 | 已测1550MiB RSS | 冻结评分的重复数量实验，再对真实裁切完整重跑 |
| C2 | 机器人突发丢帧的时间感知点跟踪 | TAPNext，ICCV2025；TAPNext++，CVPR2026 Findings | CPU真实16帧单点完成 | 已测3676MiB RSS | 固定到达帧清单，对比均匀与突发丢帧 |
| C3 | 来源不明广角照片的相机族选择 | AnyCalib，ICCV2025 | CPU已知pinhole单图完成 | 已测约2759MiB RSS | 裁切后的选模与边缘偏差诊断 |
| C4〔条件〕 | 复杂桌面目标页面去弯曲 | D2Dewarp，CVPR2026 | 官方失败案例已核，推理待测 | 推荐GPU；CPU需设备适配 | 取得权重、复现背景字干扰，核验改编发布许可 |
| C5〔备选〕 | 少样本PCB微缺陷相位稳定检测 | SubspaceAD，CVPR2026 | CPU Small/224真实1+2张完成 | 已测697MiB RSS；论文Giant/672分列 | 正常子空间固定后的0/3/7像素相位诊断 |
| C6〔条件〕 | 室内有限平面边界恢复 | ZeroPlane，CVPR2025 Highlight | 权重/数据可达，推理待测 | 7.106GB权重；先按16–24GB GPU规划 | 预定义接触/遮挡难例，检查基线错连是否显著 |
| C7 | 玻璃隔断的多层表面连续解码 | SeeGroup，CVPR2026 Oral | 代码、权重元数据与真实数据已核 | 4.27GB权重；16GB级GPU规划 | 小样本层存在性与边界诊断 |
| C8 | 遮挡物体重定位的概念选择 | ConceptPose，CVPR2026 | 官方资源已核，未运行 | 作者16GB GPU/48GB RAM | 固定LMO两对，检查三维支撑 |
| C9 | 亮面商品的观测约束高光去除 | UnReflectAnything，CVPR2026 Oral | 代码/权重元数据已核，未运行 | 3.44GB权重；16GB GPU规划 | 核验PSD条款，真实双图推理与颜色残差诊断 |

资源标注区分实测与规划。当前CPU结果的RSS包括模型及相关数据加载；GPU需求经单图或单对检查后更新。

## C1 建筑立面复拍的重复数量感知匹配

**真实用户与输入输出。** 对建筑巡检和立面复拍，输入不同时间、视角或裁切的两张RGB照片，输出物理对应点及F/H几何关系。重复窗格两侧可见数量不同，可能改变双softmax分母与真对应分数。

**研究机制。** 冻结LoMa检测器、描述器和matcher，在同图描述子与重复结构关系中建立候选等价类；类间归一化表示存在支持，类内由同预算几何求解器分配物理对应。先固定相似度研究评分算子，再对真实图像裁切与遮挡完整重跑，区分数量效应与视觉变化。

**直接近邻。** [Preserve, Then Resolve，2026预印本](https://arxiv.org/abs/2604.23670)已保留多对多候选并做几何消歧，是必要强对照；[MiHo](https://github.com/fb82/MiHo)提供几何后处理；[RoMa v2，ECCV2026](https://arxiv.org/abs/2511.15706)作为不同匹配范式的效果参照。候选创新限定为重复等价类的数量归一化，需超过top-k与已有消歧方法。

| 资源 | 链接 |
|---|---|
| 论文 | [LoMa，ECCV2026 Oral](https://arxiv.org/abs/2604.04931) |
| 作者代码 | [davnords/LoMa](https://github.com/davnords/LoMa) |
| 轻量权重 | [LoMa-B128](https://github.com/davnords/storage/releases/download/loma/loma_B128.pth) |
| 强基线权重 | [LoMa-B](https://github.com/davnords/storage/releases/download/loma/loma_B.pt) |
| 真实数据 | [HardMatch ZIP](https://github.com/davnords/storage/releases/download/hardmatch/hardmatch.zip)，约660MB |
| 官方协议 | [HardMatch代码与划分](https://github.com/davnords/HardMatch) |
| 实跑记录 | [官方预处理3对实验](../baselines/20261018-loma-official-preprocess/README.md) |

**数据版本。** [HardMatch官方说明](https://github.com/davnords/HardMatch)记录公开数据因许可替换约10对，当前公开demo的预期mAA为0.5061，与论文版本不同。公开新版本、论文报告和本次3对validation结果分别列示；跨方法比较固定同一归档哈希、数据清单和划分。

**评价。** 官方种子1337按类别划分100对validation和900对test，按官方规则排除dynamic及GT不足的样本，保留有效样本清单。主指标mAA@10px；另报真对应候选保留率、几何失败率、候选边数和端到端耗时。F评分与点对点真值误差分别处理。对照原LoMa、top-k+MAGSAC、PTR、类级方案；重复类构造与归一化分别消融。

**当前实测。** LoMa-B128官方路径预处理、2048关键点、CPU四线程，3对validation的样本mAA=0.5982517，逐对耗时10.494、9.906、10.146秒，峰值RSS1550.125MiB。完整test和新增方法实验待进行。

**资源与许可。** 初期训练自由；正式B128/B比较先按8–12GB GPU和约20GB磁盘规划。作者代码MIT，继承matcher部分Apache-2.0；HardMatch图片来自Wikimedia，逐图保留元数据中的来源、作者与许可。

## C2 机器人突发丢帧的时间感知点跟踪

**真实用户与输入输出。** 无线机器人相机或共享算力进程造成不规则图像到达。输入为按时间排序的RGB、源帧编号或时间戳，以及单点查询；输出到达帧坐标和可见性。模式为纯因果，缺失区间没有图像或事件观测。

**研究机制。** 将递归保留系数a按相对时间间隔ρ改为a^ρ并同步调整归一化；卷积短缓存记录特征年龄，按物理时间加权或退出支持区。冻结图像编码器与坐标头，只适配小范围时间模块。连续时间离散化为既有思想，本题检验它在预训练视觉状态与短缓存中的联合效果。

**直接近邻。** TAPNext++已有长序列、重检测和状态变化分析；[Track-On-R，CVPR2026](https://arxiv.org/abs/2603.12217)已覆盖跨跟踪器verifier；[EDCPT，ICCV2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Wan_Event-aided_Dense_and_Continuous_Point_Tracking_Everywhere_and_Anytime_ICCV_2025_paper.pdf)使用RGB与事件处理低帧率连续运动，其image-only消融也需对齐。不同传感器信息量分别报告。

| 资源 | 链接 |
|---|---|
| 主会论文依据 | [TAPNext，ICCV2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Zholus_TAPNext_Tracking_Any_Point_TAP_as_Next_Token_Prediction_ICCV_2025_paper.pdf) |
| 最新执行基线 | [TAPNext++，CVPR2026 Findings](https://openaccess.thecvf.com/content/CVPR2026F/html/Jung_TAPNext_Whats_Next_for_Tracking_Any_Point_TAP_CVPRF_2026_paper.html) |
| 作者代码 | [google-deepmind/tapnet](https://github.com/google-deepmind/tapnet) |
| 权重 | [TAPNext++ 256²](https://storage.googleapis.com/dm-tapnet/tapnextpp/tapnextpp_ckpt.pt) |
| 真实测试数据 | [TAP-Vid DAVIS](https://storage.googleapis.com/dm-tapnet/tapvid_davis.zip)、[RoboTAP](https://storage.googleapis.com/dm-tapnet/robotap/robotap.zip) |
| 独立适配素材 | [DAVIS2017 trainval480p](https://data.vision.ee.ethz.ch/csergi/share/davis/DAVIS-2017-trainval-480p.zip)，只取官方train清单 |
| 实跑记录 | [16帧单点实验](../baselines/20261018-tapnextpp-davis16/README.md) |

**评价。** 固定查询与到达帧，比较固定间隔、独立随机和突发缺帧；只在实际到达帧评价AJ、δ平均值、OA，另报缺帧后定位误差、失效持续时间、编码次数和时延。对照原模型、相同丢帧增强、仅LRU校正、仅缓存校正、联合方案、重复上一帧、长间隔清缓存。

**当前实测。** 官方模型在真实DAVIS的bike-packing上运行16帧单点。CPU四线程前向42.039秒，后续帧均值2.635秒，峰值RSS3676.375MiB，全部输出有限。查询帧排除后评价15个位置，该点全程可见，AJ、δ平均值、OA均为1.0。遮挡及缺帧机制尚未测试。

**资源与许可。** 首轮CPU短序列已可行。小参数适配先按24GB GPU、16帧规划。tapnet代码和所列权重Apache-2.0；TAP-Vid点标注与RoboTAP为CC BY4.0，DAVIS源视频保留原始归属和使用条款。

## C3 来源不明广角照片的裁切一致相机模型选择

**真实用户与输入输出。** 巡检、房屋建模及网络照片缺失EXIF且可能经过裁切拉伸。输入一张RGB及其已知数字变换视图，输出当前图域的相机族、内参、射线场和歧义标记。

**研究机制。** AnyCalib已经支持裁切及多种相机族，官方predict接口由调用者给cam_id。拟对原图和2–3个裁切的预测射线联合拟合候选相机族，以空间留出误差、跨裁切一致性及正焦距、投影单调性选模。合成裁切共享原图，关键对照为同推理预算的简单平均与多尺度推理。

**直接近邻。** [Generalized Camera Calibration，IEEE Sensors Journal2025](https://doi.org/10.1109/JSEN.2025.3581377)已做多图BIC选模；[2026自动标定预印本](https://arxiv.org/abs/2609.10082)已用held-out标定板图选择畸变阶数；[AnyCam-MCT，2026硕士论文](https://huggingface.co/thekman17/anycam-mct)已跨真实帧聚合AnyCalib特征。本题限定单张自然图像的未知模型选择。

| 资源 | 链接 |
|---|---|
| 论文 | [AnyCalib，ICCV2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Tirado-Garin_AnyCalib_On-Manifold_Learning_for_Model-Agnostic_Single-View_Camera_Calibration_ICCV_2025_paper.pdf) |
| 作者代码 | [javrtg/AnyCalib](https://github.com/javrtg/AnyCalib) |
| 权重 | [通用gen](https://github.com/javrtg/AnyCalib/releases/download/v1.0.0/anycalib_gen.pt)、[编辑edit](https://github.com/javrtg/AnyCalib/releases/download/v1.0.0/anycalib_edit.pt) |
| 真实数据 | [LaMAR2k](https://cvg-data.inf.ethz.ch/GeoCalib_ECCV2024/lamar2k.zip)，约400MB；[edited](https://drive.google.com/uc?id=1h2HThhQbvqZlMw0OdpF7Y73wodeZMmdj)，约224MB |
| 畸变外部测试 | [MonoVO2k](https://drive.google.com/uc?id=18rQ-WZcxXogeBqMwWvSkxVVEmZ9C12BZ)，约445MB |
| 实跑记录 | [已知pinhole单图实验](../baselines/20261018-anycalib-lamar1/README.md) |

**评价。** 射线角误差中位数、尾部和边缘分区、焦距/主点误差、物理无效率及耗时。已知模型作为oracle参考，主比较为未知模型条件。多个模型在窄视野中可能等价，因此优先比较可见图域射线精度。anycalib_edit只训练编辑透视图像，畸变与裁切组合单列检查。

**当前实测。** 官方gen与原预处理，LaMAR首CSV图95419735117.jpg，已知pinhole；CPU推理2.592秒、加载3.640秒，进程峰值约2759MiB。官方函数评分最大相对焦距误差2.454%、拟合pinhole相机的平均射线角误差0.454°、vfov误差1.203°。本次为已知模型单图标定，未知模型选择与跨裁切实验待进行。

**资源与下一步。** DINOv2-L、该图内部364×280；首版冻结网络与CPU优化。代码权重Apache-2.0，LaMAR数据CC BY4.0；MonoVO归档条款待核。下一步在20–50张独立真实图像验证选模不一致是否存在。

## C4 复杂桌面背景下的目标页面去弯曲

**真实用户与输入输出。** 拍教材或报表时，目标页下方其他印刷页会干扰页面线条。输入RGB和目标页内部一次点击，输出目标页面去弯曲图、选中区域和网格检查。

**问题证据与机制。** D2Dewarp论文Fig.7明确展示背景字引发H-Line分割错误。拟用点击附近H/V线交点作为种子，按线方向、行列顺序及页面边界筛选目标页连通子图；随后拟合低自由度B-spline残差warp，约束交点顺序与正Jacobian。冻结主干，先做图优化后处理。

**直接近邻。** [ForCenNet，ICCV2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Cai_ForCenNet_Foreground-Centric_Network_for_Document_Image_Rectification_ICCV_2025_paper.pdf)已有前景mask和曲率一致性；[DocMatcher，WACV2025](https://openaccess.thecvf.com/content/WACV2025/html/Hertlein_DocMatcher_Document_Image_Dewarping_via_Structural_and_Textual_Line_Matching_WACV_2025_paper.html)使用已知模板。新切口是点击指定页面实例后的线图选择，必须和简单点击分割+裁剪同输入比较。

| 资源 | 链接 |
|---|---|
| 论文 | [D2Dewarp，CVPR2026](https://openaccess.thecvf.com/content/CVPR2026/html/Li_D2Dewarp_Dual_Dimensions_Geometric_Representation_Learning_Based_Document_Image_Dewarping_CVPR_2026_paper.html) |
| 作者代码 | [xiaomore/D2Dewarp](https://github.com/xiaomore/D2Dewarp) |
| 权重发布文件 | [作者Google Drive单文件](https://drive.google.com/file/d/1KcVaW0CfP5YJv6DZQ9EFzRuE9h9x40ij/view)，目录显示862.7MB；文件实际下载待测 |
| 真实DocUNet | [实拍crop.zip](http://vision.cs.stonybrook.edu/~kema/docwarp/crop.zip)、[平整scan.zip](http://vision.cs.stonybrook.edu/~kema/docwarp/scan.zip)，130张实拍 |
| 额外真实数据 | [DIR300作者文件夹](https://drive.google.com/drive/folders/1yySouQQ3BlH7OjnUhq4CLuvpX2KXtifX?usp=sharing)、[DocReal文件](https://drive.google.com/file/d/1fxdUMMCQoTxc-THv1LmO-Ye8XjMyPK--/view?usp=drive_link) |

**评价。** MS-SSIM、LD、AD、OCR CER/ED，另报背景文字保留率、目标页覆盖率和正Jacobian比例。固定目标页面点击及位置扰动，对照原模型、点击分割/GrabCut+裁剪、线图筛选、残差warp与联合方法。简单/复杂背景分层。

**资源与状态。** 未执行推理。官方脚本硬编码CUDA设备，CPU需要显式设备映射。传统LD/AD评价依赖MATLAB，OCR固定工具版本。仓库标CC BY-NC-ND4.0，改编代码/权重的公开发布范围待确认；课程第一阶段进行原版复现和独立后处理研究。数据图像再分发许可逐项核验。

## C5 机制诊断备选 少样本PCB微缺陷的相位稳定检测

**真实用户与输入输出。** 小批量换型只有1–4张正常PCB支持图。输入正常参考与待检RGB，输出缺陷热图、复检区域和残差一致性图。

**研究机制。** 固定正常图拟合的PCA子空间，先测试缺陷与14像素Patch网格的相对相位是否改变残差。首遍候选窗口用半Patch偏移与更高采样率复检，逆映射后按组件保留位置一致的异常证据，并区别padding伪影。相位效应目前是待验证假设。

**直接近邻。** SubspaceAD官方已有重叠patch、背景mask、镜面过滤、CLAHE和增强。[SPARC，2026预印本](https://arxiv.org/abs/2608.18585)已做per-cell子空间校正；[ShiftSplit-AD，2026预印本](https://arxiv.org/abs/2608.27610)已做低秩/稀疏残差分解。候选贡献限定为同计算预算下的微缺陷相位证据保留。

| 资源 | 链接 |
|---|---|
| 论文 | [SubspaceAD，CVPR2026](https://openaccess.thecvf.com/content/CVPR2026/html/Lendering_SubspaceAD_Training-Free_Few-Shot_Anomaly_Detection_via_Subspace_Modeling_CVPR_2026_paper.html) |
| 作者代码 | [CLendering/SubspaceAD](https://github.com/CLendering/SubspaceAD) |
| 论文主干 | [DINOv2 with registers Giant模型页](https://huggingface.co/facebook/dinov2-with-registers-giant) |
| CPU烟测权重 | [DINOv2 with registers Small直链](https://huggingface.co/facebook/dinov2-with-registers-small/resolve/main/model.safetensors)，88.3MB，已核HEAD200 |
| 真实主数据 | [VisA直接下载](https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar)，约1.93GB，CC BY4.0 |
| 跨类验证 | [MVTec AD官方分类下载](https://www.mvtec.com/company/research/datasets/mvtec-ad/downloads)，CC BY-NC-SA4.0 |

**评价。** 图像AUROC/AUPR、像素AUROC、AU-PRO，另报微缺陷组件召回、热图逆映射一致性与总token预算。对照官方重叠patch、固定四相位均值/max、等预算全图高分辨率和候选复检。五seed固定支持图，所有PCB类别均报告；原始真实测试与派生相位扰动分开。

**当前实测。** 官方源码未改，CPU四线程，DINOv2-registers-Small/224、mean层[-4,-5,-6,-7]、1shot、aug0、PCA99%（154维）、seed42。固定CSV首条：正常支持图0499.JPG；测试正常0107.JPG和异常000.JPG。热身后测试前向分别0.087083和0.080097秒；完整含下载与启动23.412秒，峰值RSS697.047MiB。异常图得分3.386228、正常图2.218978，定义为像素top1%均值，非概率。两测试图仅有52个GT阳性像素；完整集指标和相位机制待评价，复跑材料待发布。

**资源与下一步。** 算法训练自由，仅使用冻结DINOv2权重和正常图PCA。此次Small/224与论文Giant/672配置分别报告；作者论文使用H100，正式Giant基准按GPU条件安排。机制诊断备选状态保留。下一步先测0/3/7像素相位效应，效应显著后再开发复检。

## C6 室内有限平面边界恢复

**真实用户与输入输出。** 室内AR和简化建模需要桌面、墙面等有限可见区域。输入单张RGB，首轮使用已知内参；输出平面法向、距离、可见多边形与邻接/遮挡关系。

**研究机制。** 冻结ZeroPlane，建立平面邻接图，结合RGB线段、T-junction和深度顺序区分接触边与遮挡边。接触边约束三维平面交线的二维投影，遮挡边约束前后顺序；仅更新小量参数和轮廓顶点，保留原mask证据。室内错连现象尚需首轮诊断。

**直接近邻。** [Pixel-wise Planarity，2026预印本](https://arxiv.org/abs/2609.13246)已有深度、法向、像素平面性区域生长与RANSAC；[PlaneRAS，ICCV2025](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_PlaneRAS_Learning_Planar_Primitives_for_3D_Plane_Recovery_ICCV_2025_paper.html)已有显式平面基元；[MoRe，WACV2026](https://openaccess.thecvf.com/content/WACV2026/papers/Jung_MoRe_Monocular_Geometry_Refinement_via_Graph_Optimization_for_Cross-View_Consistency_WACV_2026_paper.pdf)已有跨视图几何优化。本题限定单图可见边界类型约束。

| 资源 | 链接 |
|---|---|
| 论文 | [ZeroPlane，CVPR2025](https://openaccess.thecvf.com/content/CVPR2025/html/Liu_Towards_In-the-wild_3D_Plane_Reconstruction_from_a_Single_Image_CVPR_2025_paper.html) |
| 作者代码 | [jcliu0428/ZeroPlane](https://github.com/jcliu0428/ZeroPlane) |
| 权重直链 | [dust3r_encoder_released.pth](https://huggingface.co/jcleo0428/ZeroPlane-Dust3R/resolve/main/dust3r_encoder_released.pth)，约7.106GB，已核HEAD200 |
| 真实数据 | [NYUv2平面标注ZIP](https://huggingface.co/datasets/jcleo0428/ZeroPlane_dataset/resolve/main/nyuv2_plane.zip)，约2.529GB；[7Scenes平面标注ZIP](https://huggingface.co/datasets/jcleo0428/ZeroPlane_dataset/resolve/main/sevenscenes_plane.zip) |

**评价。** 官方RI/VOI/SC和深度/法向阈值下平面召回，另报边界F1、交线重投影误差、遮挡序错误和越界面积。对照原mask、连通域清理、统一平面平滑及PixelwisePlanarity。新增边界类型标注按预定义子集盲标复核，粗糙历史平面GT与精细毫米级评价分开处理。

**资源与状态。** 未执行推理，含Detectron2/MSDeformAttn编译依赖，CPU10GB环境优先级较低。先按16–24GB单卡做640×480检查；此为规划值。官方代码MIT，权重及NYUv2/7Scenes源数据条款分别核验。首版冻结模型，后处理在CPU完成。

## C7 玻璃隔断场景中的多层表面连续解码

**真实用户与输入输出。** 室内玻璃隔断、展示柜和玻璃门同时呈现前景表面及后方物体。输入单张RGB，输出每像素的无序多层表面集合、存在性和相对深度关系。

**已有解码与研究机制。** SeeGroup官方`get_depth`已经使用`valid_mask`过滤、移除depth≤0.02、排序，并按绝对差0.02去重。拟冻结四个Laplace分量，将已有绝对阈值替换为按分量尺度归一的兼容性判据，再通过邻域集合传输连接兼容表面，允许层出生和消失，并用RGB边缘调整连接代价。各通道的物理身份保持置换不变。原模型亦已有覆盖损失与梯度损失；拟议贡献限定为尺度归一判据与测试时邻域联合解码。

**直接近邻。** [LayeredDepth，ICCV2025](https://arxiv.org/abs/2503.11633)已建立真实多层深度与tuple评价；[One Scene, Two Depths，ECCV2026](https://arxiv.org/abs/2606.29600)通过输入变换获取玻璃前后两种深度假设。不同数据集的tuple accuracy与ML-SRA分别报告。原SeeGroup完整`get_depth`解码、绝对阈值扫描、仅尺度归一及简单边缘平滑是关键对照。

| 资源 | 链接 |
|---|---|
| 论文 | [SeeGroup，CVPR2026 Oral](https://arxiv.org/abs/2605.28735) |
| 作者代码 | [princeton-vl/SeeGroup](https://github.com/princeton-vl/SeeGroup) |
| 权重直链 | [seegroup.pth](https://huggingface.co/Hermera/SeeGroup/resolve/main/seegroup.pth?download=true)，约4.27GB |
| 真实数据 | [LayeredDepth数据卡](https://huggingface.co/datasets/princeton-vl/LayeredDepth)、[首个validation分片](https://huggingface.co/datasets/princeton-vl/LayeredDepth/resolve/main/data/validation-00000-of-00009.parquet)，约410MB；完整validation300张/9分片 |
| 合成诊断数据 | [LayeredDepth-Syn首个validation分片](https://huggingface.co/datasets/princeton-vl/LayeredDepth-Syn/resolve/main/data/validation-00000-of-00002.parquet)，约402MB |

**评价。** 真实数据使用官方quadruplet/triplet/pair accuracy，报告All、Mixed与各层；另报不存在层误接受率。合成数据单列层出现/消失边界F1和密集误差。开发与留出图像ID固定，官方test1200张的隐藏标注评测与公开validation结果分列。消融尺度归一、邻域传输、出生/消失代价和RGB边缘项。

**资源与状态。** 代码、权重元数据和数据卡已核，尚未推理。官方初始化使用CUDA；先按16GB级单卡、batch1、518输入尺度规划。方案冻结网络。代码BSD-3-Clause，真实LayeredDepth为CC0-1.0，合成LayeredDepth-Syn为BSD-3-Clause。下一步先缓存小样本分量，统计重复层、孤立幻层及薄层漏检，再评估集合解码。

## C8 遮挡物体重定位的几何可观测概念选择

**真实用户与输入输出。** 桌面机器人从一张RGB-D参考图重定位被遮挡物体。输入参考与查询RGB-D、对象mask和固定类别概念库，输出相对6D位姿。

**研究机制。** 概念热图可能集中在同一部件，语义清晰但三维支撑重复。拟依据三维支撑的信息互补性选择K个概念，考虑单部件因遮挡失效后的可观测性。概念数量已有基线实验，本题比较相同K及相同实际时间预算的选择规则。

**直接近邻。** [UNOPose，CVPR2025](https://github.com/shanice-l/UNOPose)、[OPT-Pose，CVPR2026](https://arxiv.org/abs/2603.23370)是单RGB-D参考位姿强基线；[LCVSP，2026预印本](https://arxiv.org/abs/2606.22076)已有跨视图语义与几何训练，正式会议未核，作者仓库注明代码/模型于接收后发布。已有训练方法的作者报告精度高于ConceptPose，本题目标为冻结模型、固定预算下的可观测性收益。

| 资源 | 链接 |
|---|---|
| 论文 | [ConceptPose，CVPR2026](https://arxiv.org/abs/2512.09056) |
| 作者代码 | [StevenKuang/concept-pose](https://github.com/StevenKuang/concept-pose) |
| VLM权重 | [SigLIP2模型页](https://huggingface.co/google/siglip2-giant-opt-patch16-384)、[分片1](https://huggingface.co/google/siglip2-giant-opt-patch16-384/resolve/main/model-00001-of-00002.safetensors)、[分片2](https://huggingface.co/google/siglip2-giant-opt-patch16-384/resolve/main/model-00002-of-00002.safetensors) |
| 额外遮挡压力集LMO | [测试图像](https://huggingface.co/datasets/bop-benchmark/lmo/resolve/main/lmo_test_all.zip)、[基础标注](https://huggingface.co/datasets/bop-benchmark/lmo/resolve/main/lmo_base.zip)、[物体模型](https://huggingface.co/datasets/bop-benchmark/lmo/resolve/main/lmo_models.zip) |
| 论文主协议素材与配对 | [REAL275](http://download.cs.stanford.edu/orion/nocs/real_test.zip)、[GT](http://download.cs.stanford.edu/orion/nocs/gts.zip)、[Oryon固定配对](https://github.com/jcorsetti/oryon/releases/download/v1.0.0-data/oryon_data.zip) |

**评价协议。** 论文主表对齐REAL275及Oryon/Horyon的固定cross-scene配对协议；LMO使用作者same-scene遮挡rebuttal配置，作为额外压力评估，两者分表记录。主指标ADD(-S) recall、对称性分层旋转/平移误差及K–精度和K–延迟曲线；LMO另报BOP AR。对照完整20概念、配置15概念、随机K、热图能量top-K、语义多样性K与几何可观测K。固定mask、pair、RANSAC种子和迭代；参考预计算与在线耗时分列。

**资源与状态。** 尚未运行。作者报告使用RTX4060Ti16GB与48GB RAM、FP16。方案冻结VLM，参考概念离线缓存，需PyTorch3D等依赖。代码MIT，SigLIP2为Apache-2.0，LMO为CC-BY-SA-4.0；REAL275归档许可另核。下一步固定LMO两对并运行，再检查低可见率下的三维支撑退化。

## C9 面向亮面商品拍摄的观测约束高光去除

**真实用户与输入输出。** 商品摄影拍摄印刷包装、塑料器皿与釉面商品，需要消除高光并保留原有颜色和细纹理。输入单张普通RGB，输出漫反射图像、高光残差和饱和区域。核心对象为不透明电介质亮面材质，透明折射、彩色金属镜面和完全饱和区域单列分析。

**研究机制。** 冻结UnReflectAnything，把漫反射输出作为先验。在线性RGB近似下用 `I=clip(D+s·l)` 建模局部反射：未饱和通道施加观测等式残差，饱和通道施加单侧截断约束；估计非负镜面分量与局部照明色度，并保留可见纹理梯度。研究目标是高光掩码内部尚可观测的颜色测量。

**直接近邻。** [One-Step Specular Highlight Removal / ProbLoRA，ICCV2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Atmis_One-Step_Specular_Highlight_Removal_with_Adapted_Diffusion_Models_ICCV_2025_paper.pdf)已有单步扩散去高光；[StableDelight](https://github.com/Stable-X/StableDelight)已有结构相似性和纹理锐度改进；UnReflectAnything官方已有掩码外原图composite。故关键对照是同一掩码、阈值/膨胀扫描、简单混合和传统二色分解，判断掩码内观测约束的独立作用。

| 资源 | 链接 |
|---|---|
| 论文 | [UnReflectAnything，CVPR2026 Oral](https://arxiv.org/abs/2512.09583) |
| 作者代码 | [alberto-rota/UnReflectAnything](https://github.com/alberto-rota/UnReflectAnything) |
| 权重直链 | [full_model_weights.pt](https://huggingface.co/AlbeRota/UnReflectAnything/resolve/main/weights/full_model_weights.pt)，约3.44GB，当前HF文件元数据已核 |
| 真实数据 | [PSD作者仓库](https://github.com/jianweiguo/SpecularityNet-PSD)、[作者归档下载](https://drive.google.com/file/d/1PUrUyUd1ys6pue8jPGchCGVdFBAf8eqg/view?usp=sharing)，13,380张真实图像、2,210场景 |

**评价。** 全图、高光内、边界带和掩码外的PSNR/SSIM，另报ΔE00、纹理边缘保留、高光残差能量与延迟。按物理场景隔离，先固定100个适用材质留出场景；统一输入尺寸和色彩空间。消融饱和分通道约束、照明色度、预测先验和梯度项。偏振参考漫反射的残余误差纳入案例分析。

**资源与状态。** HF当前3.44GB权重文件已核实存在；按[固定源码commit](https://github.com/alberto-rota/UnReflectAnything/tree/363ebb5c87d9f4f49b63f744fded8d3786a051b3)记录运行入口。该commit与当前权重的加载兼容性待实跑验证，尚未下载权重或推理。官方CLI有CPU选项；先按16GB单卡、batch1、约448输入规划，速度与显存待测。首版冻结模型，仅做轻量约束求解。代码MIT，DINOv3预训练部分单独遵循其模型许可。PSD作者公开下载，README独立数据许可未标，归档使用与再分发条款待核。下一步核验数据条款，完成两张真实图像推理，再检查未饱和残差是否对应颜色恢复空间。

## 备选与淘汰记录

| 方向 | 决定 | 已覆盖的关键机制与后续处理 |
|---|---|---|
| MINIMA RGB–热红外成像误差传播 | 场景适配备选 | [PNEC/CVPR2023](https://openaccess.thecvf.com/content/CVPR2023/html/Muhle_Learning_Correspondence_Uncertainty_via_Differentiable_Nonlinear_Least_Squares_CVPR_2023_paper.html)已有各向异性协方差与几何优化；需验证传感器特定新机制 |
| PromptDA手机LiDAR异常传播 | 暂缓原改法 | [PromptDA++](https://github.com/DepthAnything/PromptDA/blob/main/assets/paper.pdf)已有中位数与任意稀疏模式；[DEPTHOR++](https://arxiv.org/abs/2509.26498)已有异常检测与传播抑制 |
| 泛MoGe细节增强 | 淘汰泛化表述 | MoGe-3与MoRe已覆盖精细几何或图优化；有限平面边界另立窄题 |
| Dinomaly常规工业异常改进 | 改由SubspaceAD窄题审查 | 更换主干、前背景过滤和一般局部距离不足以形成明确新机制 |
| 原点跟踪遮挡恢复/跨主干verifier | 重构为C2 | TAPNext++、TAPTRv3和Track-On-R覆盖恢复、记忆及verifier主要想法 |
| 原NAFNet+光流可靠性门控去模糊 | 淘汰原组合 | 时序融合、遮挡处理已有直接强方法，旧单帧基线不足以支撑增量 |
| 原NNDVS低裁切稳像 | 暂缓 | LightStab等较新方法与真实输入链路需对齐；原复现依赖预计算网格 |
| 原八题其余方向 | 历史方案 | 继续保留材料，正式候选以本表为准 |

备选资源仍可用于工程复现，但新算法立题需给出超出直接近邻的机制差异与同协议证据。

## 证据与版本

- 本表实测数值读取LoMa官方预处理3对summary、TAPNext++ 16帧result、AnyCalib单图result与SubspaceAD Small/224两测试图记录
- 论文年份按正式会议区分；TAPNext++为CVPR2026 Findings，TAPNext为ICCV2025主会
- 权重链接可达、脚本可导入、真实推理成功、完整指标复现、新方法有效是不同阶段，表内按实际完成阶段记录
- 每次正式实验保存官方源码commit、环境、参数、数据清单、权重与数据哈希
- 论文图和论文表格注明作者报告；仓库生成的真实结果注明样本、设备和范围

