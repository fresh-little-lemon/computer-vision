# 新版计算机视觉开题候选：文档、室内几何与工业质检

研究核验日期：2026-10-18。以下为三个独立应用场景的开题计划，主基线均来自已确认的2025–2026顶会主会。文档中的“拟改进”是研究假设，尚无新方法性能结果。

## 建议顺序

1. **D2Dewarp目标文档去弯曲**：最明确的问题证据。原论文Fig.7直接展示背景文字干扰，能从一次页面点击、线图和非刚性几何展开课程研究。先击败简单点击分割加裁剪。
2. **ZeroPlane有限平面边界**：室内数字化场景清楚，投影几何联系最强。主模型资源较重，接触/遮挡边界假设需第一阶段诊断。原作者没有将该假设列为已知室内失败。
3. **SubspaceAD微缺陷采样相位**：CPU小模型可起步，真实VisA数据直链明确。创新风险相对较高，需要先证明微缺陷对采样相位有实质敏感性，并超过同计算预算的平移TTA与重叠切块。

## 资源核验摘要

| 项目 | 论文状态 | 作者资源 | 数据可达性 | 当前证据 |
|---|---|---|---|---|
| D2Dewarp | CVPR 2026主会 | 推理代码；Drive单权重862.7MB | DocUNet crop/scan原始HTTP链HEAD200 | 文献和源码已读，未跑 |
| ZeroPlane | CVPR 2025主会Highlight | 7.106GB权重；Detectron2/CUDA算子 | NYUv2处理包2.529GB，HEAD200 | 文献和源码已读，未跑 |
| SubspaceAD | CVPR 2026主会 | 冻结DINOv2，PCA无需单独网络权重 | VisA 1.930GB，HEAD200 | Small权重88.26MB可达，尚无本分支模型运行 |

HTTP可达只表示本次请求成功，不等于完成下载、校验或复现。GPU显存下限尚未实测。独立可行性卡记录依赖与配置，不把排错细节放进开题正文。

# 复杂桌面背景下的目标文档去弯曲：基于页面条件化线图与拓扑约束的D2Dewarp改进

**研究优先级**：A：最新主会、失败案例明确、场景可解释；创新为待验证假设

## 真实应用场景

学生拍教材、研究者拍资料、办公室拍报表时，目标纸张下方常有其他印刷页。背景文字可能被当作目标页线条，导致去弯曲结果残留背景或拉扯页面。允许用户在目标页点一下，明确任务对象。

## 使用者

- 手机扫描资料的学生
- 办公室纸质文档数字化人员

## 输入、输出与任务边界

- **input**：一张真实拍摄RGB文档照片＋目标页内部1个点击点；无模板、无真实平整图作为推理输入
- **output**：目标页的矩形去弯曲图、目标页区域、H/V线连通可视化、网格fold-over检查
- **excluded**：不做OCR大模型训练、不恢复被遮住的文字、不声称全自动区分多张无边界叠页

## 最新主会基线与公开资源

- **name**：D2Dewarp: Dual Dimensions Geometric Representation Learning Based Document Image Dewarping
- **conference**：CVPR 2026 主会
- **year**：2026
- **status**：已由CVF正式论文页确认，pp.34734–34744；2025 arXiv是预印本时间
- **url**：https://openaccess.thecvf.com/content/CVPR2026/html/Li_D2Dewarp_Dual_Dimensions_Geometric_Representation_Learning_Based_Document_Image_Dewarping_CVPR_2026_paper.html
- **pdf**：https://openaccess.thecvf.com/content/CVPR2026/papers/Li_D2Dewarp_Dual_Dimensions_Geometric_Representation_Learning_Based_Document_Image_Dewarping_CVPR_2026_paper.pdf
- **code**：https://github.com/xiaomore/D2Dewarp
- **weights**：https://drive.google.com/drive/folders/1gv0lLaZWlUt1tX7EJDaVhtFhmV-ewQox?usp=sharing
- **weights_mirror**：https://pan.baidu.com/s/1qnHjy3-ANlrrgjc7hac3Bg?pwd=2cut
- **weights_file_url**：https://drive.google.com/file/d/1KcVaW0CfP5YJv6DZQ9EFzRuE9h9x40ij/view
- **weights_file_id**：1KcVaW0CfP5YJv6DZQ9EFzRuE9h9x40ij
- **weights_download_command**：gdown 1KcVaW0CfP5YJv6DZQ9EFzRuE9h9x40ij -O model_weight.pt
- **weights_verified**：公开model目录GET200，单文件名model_weight.pt，Google Drive展示862.7 MB；未下载，不承诺gdown成功。
- **source_snapshot**：- **repository**：xiaomore/D2Dewarp
  - **sha**：1105c0f0e44404d9a8dedb78f689078dba42221c
  - **commit_url**：https://github.com/xiaomore/D2Dewarp/commit/1105c0f0e44404d9a8dedb78f689078dba42221c
  - **committed_at**：2026-06-25T11:40:24Z

## 已知不足与证据边界

- **evidence**：原论文第8页Fig.7及Bad Case Analysis明确报告：背景文字引发错误H-Line分割，前景隔离失败，输出残留背景。不是本次臆测
- **source**：https://openaccess.thecvf.com/content/CVPR2026/papers/Li_D2Dewarp_Dual_Dimensions_Geometric_Representation_Learning_Based_Document_Image_Dewarping_CVPR_2026_paper.pdf
- **not_claimed**：尚未在本环境独立复现失败，也未证明所提方法优于基线

## 2025–2026近邻覆盖检查

- - **name**：D2Dewarp
  - **year**：2026
  - **status**：CVPR主会
  - **covered**：双方向H/V线预测、融合；不能再声称“新增垂直线”是创新
  - **gap**：没有用户指定目标页实例；Fig.7的背景文字干扰可作为明确起点
- - **name**：ForCenNet
  - **year**：2025
  - **status**：ICCV主会
  - **url**：https://openaccess.thecvf.com/content/ICCV2025/papers/Cai_ForCenNet_Foreground-Centric_Network_for_Document_Image_Rectification_ICCV_2025_paper.pdf
  - **covered**：前景mask和曲率一致性，泛加前景/曲率loss已被覆盖
  - **gap**：本题是1点指定页面实例后，按H/V交点连通与页面边界共同筛选，必须和简单mask前置裁剪公平比较
- - **name**：DocMatcher
  - **year**：2025
  - **status**：WACV主会，仅近邻，不当满足用户顶会门槛的主基线
  - **url**：https://openaccess.thecvf.com/content/WACV2025/html/Hertlein_DocMatcher_Document_Image_Dewarping_via_Structural_and_Textual_Line_Matching_WACV_2025_paper.html
  - **covered**：已知模板的结构/文本线匹配
  - **gap**：本题无模板，点击只指定页面身份

## 具体研究问题

目标页身份未知导致的线条污染，能否用一个页面内部点击、H/V线交点图及闭合页面边界共同约束，使D2Dewarp的去弯曲域只覆盖目标纸面，同时保持文字/表格线的相对顺序？

## 拟改进机制

- - **step**：1
  - **mechanism**：冻结D2Dewarp，保存原始H/V线概率图和backward map；通过点击附近的线条交点建立种子，提取与其几何连续的线段图
  - **why**：把所有文字区域区分为页面实例，不直接按“像文字”与否判前景
- - **step**：2
  - **mechanism**：图边由线方向平滑性、交点行列顺序和纸张边界穿越惩罚决定；优化目标页连通子图。与GrabCut/点击分割+裁剪比较
  - **why**：专门抵抗另一张纸上的平行文本被错误连入
- - **step**：3
  - **mechanism**：仅对目标页区域拟合低自由度B-spline残差warp；损失包含原预测保真、选中H/V交点的顺序、网格正Jacobian和页边界一致性
  - **why**：保持局部排版拓扑，避免修正过程中网格翻转；不把已有一般光滑正则当新贡献
- - **step**：4
  - **mechanism**：先实现完全训练free后处理；只有验证切口后才考虑冻结主干训练轻量实例门控头
  - **why**：课程不需要重训114K合成数据的大模型

## 待检验假设

页面条件化的结构选择比全图前景增强更直接降低背景文本误连；改善应主要发生于多页背景子集，干净背景不能显著退化。此为待验证假设，非已证创新。

## 真实数据、直链与许可

- - **name**：DocUNet真实测试集
  - **real**：是
  - **size**：130张实拍；官方crop 281MB，scan 416MB
  - **download_url**：http://vision.cs.stonybrook.edu/~kema/docwarp/crop.zip
  - **ground_truth_url**：http://vision.cs.stonybrook.edu/~kema/docwarp/scan.zip
  - **source**：https://www3.cs.stonybrook.edu/~cvl/docunet.html
  - **license**：官方页面未见可直接断言的完整图像许可；课程研究按作者说明使用，不公开重分发；非需从零训练数据
  - **download_verification**：- **http_status**：200
    - **size_bytes**：294741912
    - **ground_truth_size_bytes**：436458210
    - **warning**：HTTP原链可达；HTTPS变体本次502，不应擅自改协议后宣称可用
  - **original_full_photos_url**：http://vision.cs.stonybrook.edu/~kema/docwarp/original.zip
  - **evaluation_orientation_caveat**：DocGeoNet说明64_1/64_2与GT相差180度。评测前按同一协议修正/核对，所有方法一致；不得只修正某方法。
- - **name**：DIR300真实测试集
  - **real**：是
  - **size**：300张
  - **download_url**：https://drive.google.com/drive/folders/1yySouQQ3BlH7OjnUhq4CLuvpX2KXtifX?usp=sharing
  - **source**：https://github.com/fh2019ustc/DocGeoNet
  - **license**：需遵守源数据许可；此为作者正式文件夹链接，尚未验证文件级匿名下载
- - **name**：DocReal真实中文测试集
  - **real**：是
  - **size**：200张
  - **download_url**：https://drive.google.com/file/d/1fxdUMMCQoTxc-THv1LmO-Ye8XjMyPK--/view?usp=drive_link
  - **source**：https://github.com/irisXcoding/DocReal
  - **license**：数据可下载；不把该仓未公开的DocReal算法代码说成已公开
  - **download_verification**：作者公开链接已确认，本次GET返回429；文件未下载，不能写已可用。
- - **name**：DocDewarpHV可选训练集
  - **real**：否
  - **download_url**：https://github.com/xiaomore/DocDewarpHV
  - **use**：仅可选门控头训练；不是本题真实评估集

## 指标、官方脚本、对照与消融

- **official_metrics**：- MS-SSIM↑
  - Local Distortion(LD)↓
  - Aligned Distortion(AD)↓
  - OCR字符错误率CER↓
  - OCR编辑距离ED↓
- **official_scripts**：- https://github.com/fh2019ustc/DocGeoNet/blob/main/ssim_ld_eval_DocUNet.m
  - https://github.com/fh2019ustc/DocGeoNet/blob/main/ssim_ld_eval_DIR300.m
  - https://github.com/fh2019ustc/DocGeoNet/blob/main/OCR_eval_DocUNet.py
  - https://github.com/fh2019ustc/DocGeoNet/blob/main/OCR_eval_DIR300.py
  - http://vision.cs.stonybrook.edu/~kema/docwarp/eval.zip
- **additional_metrics**：- 背景文字保留面积率↓
  - 目标页面覆盖率↑
  - 正Jacobian比例↑
  - 每图额外耗时
- **protocol**：先冻结原始公开测试集；另人工标记多页/背景文字干扰子集，不使用结果挑难例。点击由目标页mask内点统一采样，并报告±扰动敏感性；训练调参不能看测试OCR GT。
- **controls**：- 原始D2Dewarp
  - 点击分割/GrabCut+裁剪+D2Dewarp
  - 仅页面线图筛选
  - 仅残差warp约束
  - 完整方法
  - ForCenNet可运行版本（依其资源发布状态）
- **ablation**：- 去掉交点顺序约束
  - 去掉边界穿越项
  - 去掉Jacobian项
  - 点击位置扰动
  - 简单背景与复杂背景分层
- **script_coverage**：已GET200的DocGeoNet MATLAB脚本覆盖MS-SSIM/LD，OCR脚本覆盖CER/ED；D2Dewarp论文报告AD，但独立AD脚本尚未定位，不把前两项脚本冒充AD实现。
- **annotation_budget**：页面实例mask和背景文字干扰标签并非现成全部提供。先人工查看原始照片，独立预选30–50张并画目标页多边形/背景文字区域；不足时缩小研究结论，不能宣称数据集中已有充分多页难例。点击由该mask内统一规则生成，标注/调参/最终测试分开。

## 基线最小命令

```bash
git clone https://github.com/xiaomore/D2Dewarp.git
cd D2Dewarp
mkdir -p outputs
python predict.py --model_path /path/model_weight.pt --img_path /path/DocUNet/crop --save_path outputs
```

## 资源需求与许可

- **course_plan**：冻结权重推理+CPU图优化；不要求重训D2Dewarp。推荐单卡GPU做批量基线，具体显存需实际测量
- **cpu_status**：官方predict.py硬编码CUDA设备3和.cuda()；不能原样在无GPU环境运行。CPU版需要显式设备映射适配，尚未实测。
- **evaluation_dependency**：原论文MS-SSIM/LD/AD采用MATLAB R2019a；OCR官方环境为Windows Tesseract5.0.1.20220118+pytesseract0.3.8，中文PaddleOCR DBNet detv4_teacher_inference + SVTR_LCNet OCRv4_rec_server_infer。替代版本须另报非精确作者环境。
- **license**：仓README标CC BY-NC-ND4.0。私有课程实验可研究，但公开发布改编代码/权重需先检查许可证与联系作者；不要宣称MIT
- **weight_size**：Google Drive显示862.7 MB；只是磁盘文件大小，不是推理显存/内存需求

## 课程算法对应

- 图像形成与透视投影
- 边缘和线检测
- 图割/最短路径/连通图
- 非刚性图像配准与B-spline变形
- 图像重采样与逆映射
- 雅可比与拓扑保持
- 学习特征与几何约束结合

## 阶段计划

- - **time**：第1周
  - **deliverable**：跑通官方权重，复现原图与去弯曲图，整理背景文字失败子集
- - **time**：第2周
  - **deliverable**：页面点击与线图选择；先完成简单裁剪对照
- - **time**：第3周
  - **deliverable**：低维warp修正与全部消融
- - **time**：第4周
  - **deliverable**：OCR/几何指标、显存时延、失败案例、答辩演示

## 论文图素材与出处

- - **url**：https://raw.githubusercontent.com/xiaomore/D2Dewarp/main/images/model1.jpeg
  - **caption**：D2Dewarp整体架构，引用Li et al., CVPR2026
  - **usage**：作为基线解释图；拟议模块另色标注，不伪装成论文原图的一部分
  - **local_path**：/workspace/shared/cv-new-topics/realworld/figures/d2_model1.jpeg
- - **url**：https://raw.githubusercontent.com/xiaomore/D2Dewarp/main/images/model2.jpeg
  - **caption**：论文H/V融合模块，已有方法
  - **local_path**：/workspace/shared/cv-new-topics/realworld/figures/d2_model2.jpeg
- - **local_path**：/workspace/shared/cv-new-topics/realworld/sources/d2_paper.pdf
  - **page_1based**：8
  - **caption**：Fig.7原论文明确失败：背景文字干扰；已渲染并目视确认第8页版面，可裁取左侧Fig.7并引用
  - **rendered_local_path**：/workspace/shared/cv-new-topics/realworld/figures/d2_p8_failure.png

## 拟议方法图示逻辑

左：桌面目标页及背景文字，黄色点表示目标页点击；中：全图H/V线→按目标页连通图筛选（背景灰色、目标蓝色）；右：原warp与修正warp网格及OCR区域对比。所有改善结果未获得时用流程示意，禁止生成虚假实验结果。

## 运行证据状态

- **status**：未跑
- **verified**：已读正式论文、官方README和predict.py；权重链接来自官方仓；Drive单文件ID和862.7MB展示已定位；DocUNet crop/scan/eval HEAD200；四个评估脚本GET200
- **unknown**：权重文件实际下载、GPU/CPU运行、精确显存、指标改善均未确认

## 创新边界

查重覆盖D2Dewarp/ForCenNet/DocMatcher等主干近邻；尚未证明目标页线图方案全球首创。若简单点击裁剪已达到同样效果，应收缩为应用验证或放弃。


---

# 少样本PCB微缺陷检测：面向Patch采样相位的残差保留与预算化复检

**研究优先级**：B：2026新主会+CPU小样本可起步；创新风险中高，先做相位失效诊断

## 真实应用场景

小批量PCB换型后只有1–4张正常板照片可用。细小缺口、焊点异物或短裂纹在缩放和14像素Patch分块后可能跨越token边界，出现同一个缺陷稍微平移就热图大变的情况。任务是稳定定位这些微缺陷，避免靠扩大主干或全图高分辨率增加算力。

## 使用者

- 小批量电子产线视觉质检人员
- 低标注成本工业异常检测研发者

## 输入、输出与任务边界

- **input**：1–4张确认正常的参考图及一张待检PCB RGB图；不使用异常标签训练主干
- **output**：缺陷热图、低预算复检区域、跨相位映射后的残差稳定性图
- **excluded**：不检测需要电路功能知识才能定义的逻辑错误，不作实际安全生产放行决定，不把基准性能当部署保证

## 最新主会基线与公开资源

- **name**：SubspaceAD: Training-Free Few-Shot Anomaly Detection via Subspace Modeling
- **conference**：CVPR 2026 主会
- **year**：2026
- **status**：CVF主会确认，pp.28557–28566
- **url**：https://openaccess.thecvf.com/content/CVPR2026/html/Lendering_SubspaceAD_Training-Free_Few-Shot_Anomaly_Detection_via_Subspace_Modeling_CVPR_2026_paper.html
- **pdf**：https://openaccess.thecvf.com/content/CVPR2026/papers/Lendering_SubspaceAD_Training-Free_Few-Shot_Anomaly_Detection_via_Subspace_Modeling_CVPR_2026_paper.pdf
- **code**：https://github.com/CLendering/SubspaceAD
- **weights**：https://huggingface.co/facebook/dinov2-with-registers-giant
- **cpu_smoke_weights**：https://huggingface.co/facebook/dinov2-with-registers-small/resolve/main/model.safetensors
- **weights_note**：训练free算法只有冻结DINOv2权重，PCA由正常支持图拟合；不需要寻找另一个不存在的SubspaceAD神经网络checkpoint
- **source_snapshot**：- **repository**：CLendering/SubspaceAD
  - **sha**：ef56d5c8ab2f1feb7dda1c93b25cc3f73f0960d7
  - **commit_url**：https://github.com/CLendering/SubspaceAD/commit/ef56d5c8ab2f1feb7dda1c93b25cc3f73f0960d7
  - **committed_at**：2026-08-17T12:58:47Z

## 已知不足与证据边界

- **evidence**：原论文Supplement Appendix F指出逻辑缺陷和背景/正常变化的失败，PCB3/Macaroni2较难；它没有明确量化patch相位问题。本文相位敏感性是待实测推断，不能冒充作者结论。
- **source**：https://openaccess.thecvf.com/content/CVPR2026/supplemental/Lendering_SubspaceAD_Training-Free_Few-Shot_CVPR_2026_supplemental.pdf
- **first_gate**：固定正常参考图和PCA，将真实测试图作0/3/7像素整图平移并逆映射热图；测微缺陷召回和分数波动。若波动很小，则放弃本切口。

## 2025–2026近邻覆盖检查

- - **name**：SubspaceAD当前官方代码
  - **year**：2026
  - **url**：https://github.com/CLendering/SubspaceAD/blob/main/src/subspacead/config.py
  - **covered**：已提供重叠patch、背景mask、镜面过滤、CLAHE、数据增强；都不是本题创新
  - **gap**：需检查固定计算预算下，跨token采样相位复检是否比普通重叠切块/平移平均更有效
- - **name**：SPARC
  - **year**：2026
  - **status**：2026-08 arXiv预印本；未确认已接收主会
  - **url**：https://arxiv.org/abs/2608.18585
  - **covered**：每个空间cell的正常子空间校正，消除照明/装夹等分布变化；本题不以该机制为新贡献
- - **name**：ShiftSplit-AD
  - **year**：2026
  - **status**：2026-08 arXiv预印本
  - **url**：https://arxiv.org/abs/2608.27610
  - **covered**：低秩/行稀疏残差分解已存在，且报告会损害真实缺陷；本题不再次提出泛低秩去噪
- - **name**：AnomalyDINO
  - **year**：2025
  - **status**：WACV主会，作近邻非本题顶会主基线
  - **url**：https://openaccess.thecvf.com/content/WACV2025/html/Damm_AnomalyDINO_Boosting_Patch-Based_Few-Shot_Anomaly_Detection_With_DINOv2_WACV_2025_paper.html
  - **covered**：冻结DINOv2局部特征异常检测已成熟；单纯更换距离或多尺度不够
- - **name**：FB-CLIP
  - **year**：2026
  - **status**：CVPR主会
  - **url**：https://openaccess.thecvf.com/content/CVPR2026/html/Hu_FB-CLIP_Fine-Grained_Zero-Shot_Anomaly_Detection_with_Foreground-Background_Disentanglement_CVPR_2026_paper.html
  - **covered**：前背景分离/背景抑制已覆盖，不纳入拟议创新

## 具体研究问题

正常子空间已冻结时，PCB微缺陷的检测残差会不会因为相对Patch网格的相位变化而被稀释？能否用少量选区复检保留局部缺陷证据，在同等特征提取预算下超过普通平移TTA与重叠切块？

## 拟改进机制

- - **step**：1
  - **mechanism**：用正常支持图拟合原SubspaceAD PCA；先记录各相位输入映射回原像素坐标后的残差，不修改主干或PCA算法
  - **why**：把采样网格现象与模型/数据变化分离
- - **step**：2
  - **mechanism**：首遍由残差局部峰值及高频结构提取候选小窗口；只对这些窗口用半Patch偏移和更高采样率复检
  - **why**：将额外计算集中在微缺陷候选区，而不是全图统一提分辨率
- - **step**：3
  - **mechanism**：构造逆映射后的组件级证据合并：对跨相位位置一致但峰值被摊薄的残差保留峰值邻域证据；对仅出现在填充边界的响应剔除
  - **why**：区别真实小组件持续性与平移padding伪影；不直接平均所有热图导致再次抹平
- - **step**：4
  - **mechanism**：以总处理像素/token数相同为预算，和固定四相位平均、max、重叠切块、统一高分辨率逐一比较
  - **why**：收益必须来自选择和组件对应机制，不能来自多算几次

## 待检验假设

微缺陷跨Patch边界造成残差稀释时，跨相位原坐标组件一致性可在少量复检中保留异常证据。新颖性及性能都待验证；简单TTA若同样好则不成立。

## 真实数据、直链与许可

- - **name**：VisA真实工业异常集
  - **real**：是
  - **download_url**：https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar
  - **size_bytes**：1929840640
  - **source**：https://github.com/amazon-science/spot-diff
  - **use**：主评估PCB1–4；使用官方split并报告所有PCB类别，不挑单一有利类别
  - **license**：CC BY 4.0，已读取原仓LICENSE-DATASET确认；注意同仓代码LICENSE为Apache2.0，不混淆。
  - **license_url**：https://github.com/amazon-science/spot-diff/blob/main/LICENSE-DATASET
  - **download_verification**：HEAD200，1,929,840,640 bytes；未下载与解压
- - **name**：MVTec AD真实异常集
  - **real**：是
  - **download_url**：https://www.mvtec.com/company/research/datasets/mvtec-ad/downloads
  - **use**：screw/grid/cable等微结构跨类验证；需从官方选相应类别下载，不伪造单文件直链
  - **license**：CC BY-NC-SA4.0，非商业研究使用
- - **name**：相位扰动评测子集
  - **real**：由真实VisA图像和mask同步变换派生
  - **download_url**：未提供 / 不适用
  - **use**：平移/裁切仅作机制诊断；不能冒充新增真实采集数据；原始真实测试集仍是主结果

## 指标、官方脚本、对照与消融

- **official_metrics**：- 图像AUROC↑
  - 图像AUPR↑
  - 像素AUROC↑
  - AU-PRO@FPR≤0.3↑
- **official_scripts**：- https://github.com/CLendering/SubspaceAD/blob/main/main.py
  - https://github.com/CLendering/SubspaceAD/blob/main/scripts/benchmark_few_shot.sh
- **additional_metrics**：- 微缺陷组件召回@固定正常误报率
  - 平移逆映射后的热图一致性
  - 每组件异常分数CV/方差
  - 总token/图像处理像素预算
  - CPU时延/GPU峰值内存
- **protocol**：支持图按官方seed重复5次；微缺陷面积分组阈值预注册（例如GT面积≤图像0.1%）；不得用测试异常GT决定复检窗口。每一种方法用相同输入/支持图/预算/输出分辨率。禁止混用few-shot正常支持与batched-zero-shot测试集拟合PCA两种协议。
- **controls**：- 原SubspaceAD
  - SubspaceAD+官方重叠patch
  - 固定4相位均值TTA
  - 固定4相位max TTA
  - 等token统一高分辨率
  - 候选窗口复检+组件保留
- **ablation**：- 无相位偏移
  - 无逆映射组件匹配
  - 均值替代组件保留
  - 残差候选vs高频候选vs均匀候选
  - 1/2/4参考图
  - 相同token预算曲线
- **phase_definition**：相位扰动在固定预处理尺寸后施加；GT最近邻同步变换。逆映射后仅比较共同有效区域，剔除padding。第一阶段固定采样尺度，若使用高分辨率复检则单独控制尺度与正常参考特征预处理。

## 基线最小命令

```bash
git clone https://github.com/CLendering/SubspaceAD.git
cd SubspaceAD
pip install -r requirements.txt
pip install -e .
python main.py --dataset_name mvtec_ad --dataset_path /path/mvtec-ad --categories bottle --model_ckpt facebook/dinov2-with-registers-giant --image_res 672 --k_shot 1 --aug_count 30 --pca_ev 0.99 --outdir results/official
```

## CPU小模型接口命令

```bash
python main.py --dataset_name visa --dataset_path /path/micro_visA --categories pcb1 --model_ckpt facebook/dinov2-with-registers-small --image_res 224 --layers=-4,-5,-6,-7 --k_shot 1 --aug_count 0 --batch_size 1 --pca_ev 0.99 --seed 42 --agg_method mean --outdir results/cpu_smoke
```

## 资源需求与许可

- **cpu_status**：实际源码自动选择CPU；DINOv2-S权重88,256,200 bytes直链HEAD200；224小样本接口烟测可尝试，仍未实际运行。小模型/层/分辨率改动需标非论文配置
- **official_compute**：论文实验使用单张H100，主要开销为DINOv2-G特征；训练free不等于低推理算力
- **course_plan**：CPU小样本调通数据/PCA/评估→固定同一small/base主干完成受控实验；若需复现论文绝对数值再借GPU用G/672。不能把small结果当论文复现
- **full_training_required**：否
- **license**：DINOv2模型卡/代码许可独立核查；PCA参数从授权正常样本生成
- **code_license**：官方SubspaceAD LICENSE已GET200，Apache2.0；DINOv2权重和数据仍按各自许可。
- **official_scheduler_request**：官方benchmark_few_shot.sh申请1张H100、4CPU、128GB主机内存、24小时；这是作者调度请求，不代表最低必要资源。
- **cpu_protocol**：微型目录固定1张官方train正常图、1张官方test正常图与1张官方test异常图及mask。完整VisA直接debug_limit2可能按路径排序取到两个bad，导致单类图像AUROC；因此使用预先确定且含两类的输入清单。

## 课程算法对应

- 采样与混叠
- 图像金字塔/局部裁块
- PCA与低秩子空间
- 残差统计和异常评分
- 连通域与组件匹配
- 视觉Transformer特征
- 精确率召回/AUROC/公平算力比较

## 阶段计划

- - **time**：第1周
  - **deliverable**：CPU小模型smoke和相位敏感性诊断；若没有明显微缺陷相位问题则停止
- - **time**：第2周
  - **deliverable**：候选区域复检与逆映射组件融合
- - **time**：第3周
  - **deliverable**：五seed、等token对照、组件级消融
- - **time**：第4周
  - **deliverable**：原始真实集与扰动集分开报告，整理误报/漏检案例

## 论文图素材与出处

- - **url**：https://raw.githubusercontent.com/CLendering/SubspaceAD/main/assets/subspacead_overview.png
  - **caption**：SubspaceAD冻结特征→PCA→残差流程，Lendering et al., CVPR2026
  - **local_path**：/workspace/shared/cv-new-topics/realworld/figures/subspace_overview.png
- - **url**：https://raw.githubusercontent.com/CLendering/SubspaceAD/main/assets/visa_examples.png
  - **caption**：官方VisA定性基线结果，非本次复现
  - **local_path**：/workspace/shared/cv-new-topics/realworld/figures/subspace_visa.png
- - **local_path**：/workspace/shared/cv-new-topics/realworld/sources/subspace_supp.pdf
  - **caption**：官方Supplement Appendix F失败案例

## 拟议方法图示逻辑

左：PCB小缺陷跨在14×14Patch边界示意；中：原采样网格与半Patch偏移，箭头映射回原坐标；右：同一缺陷组件的残差保留 vs 朴素平均。只画算法原理，未实测前不画假柱状性能。

## 运行证据状态

- **status**：未跑
- **verified**：官方论文、main/config/extractor源代码、VisA下载和small权重HEAD可达
- **unknown**：CPU耗时与峰值内存、相位失效大小、新方法提升未测

## 创新边界

相位TTA本身并不新。新贡献若成立，应是微缺陷的相位失效证据＋相同计算预算下的组件证据保留；仅多跑几次取平均/最大值不构成充分创新。


---

# 室内数字化中的有限平面边界恢复：基于遮挡关系与投影交线的ZeroPlane改进

**研究优先级**：B：课程几何关系强，资源公开；必须先验证窄切口，避免与2026像素平面性方法重复

## 真实应用场景

用一张手机照片做室内AR放置或简化房间模型时，墙、台面和柜门需要有可信的可见边界。只预测无限平面法向/距离不够：跨过前景椅子、显示器或门洞的连接会产生穿插或虚假的支撑面。

## 使用者

- 轻量室内数字化用户
- 室内AR摆放应用开发者

## 输入、输出与任务边界

- **input**：一张室内RGB照片；若内参未知使用基线的设置；课程第一阶段采用NYUv2/7Scenes的已知内参以分离问题
- **output**：每个可见平面实例的法向、距离、有限多边形轮廓与邻接/遮挡关系；只重建可见支持区域
- **excluded**：不臆造被家具遮住的几何，不承诺绝对尺寸测量安全性，不做全屋SLAM或生成完整不可见家具

## 最新主会基线与公开资源

- **name**：Towards In-the-wild 3D Plane Reconstruction from a Single Image (ZeroPlane)
- **conference**：CVPR 2025 主会 Highlight
- **year**：2025
- **status**：CVF已确认主会，pp.27027–27037；官方仓标Highlight
- **url**：https://openaccess.thecvf.com/content/CVPR2025/html/Liu_Towards_In-the-wild_3D_Plane_Reconstruction_from_a_Single_Image_CVPR_2025_paper.html
- **pdf**：https://openaccess.thecvf.com/content/CVPR2025/papers/Liu_Towards_In-the-wild_3D_Plane_Reconstruction_from_a_Single_Image_CVPR_2025_paper.pdf
- **code**：https://github.com/jcliu0428/ZeroPlane
- **weights**：https://huggingface.co/jcleo0428/ZeroPlane-Dust3R/resolve/main/dust3r_encoder_released.pth
- **weights_size_bytes**：7105876663
- **weights_download_verification**：HEAD200，7,105,876,663 bytes；未下载与运行
- **source_snapshot**：- **repository**：jcliu0428/ZeroPlane
  - **sha**：c8d7503d27738749a65f702129113b5f38c9c058
  - **commit_url**：https://github.com/jcliu0428/ZeroPlane/commit/c8d7503d27738749a65f702129113b5f38c9c058
  - **committed_at**：2025-10-06T09:05:03Z

## 已知不足与证据边界

- **evidence**：原论文的显式limitations主要是户外真实数据不足，不能冒充作者已报告室内遮挡失败。本题有限轮廓/遮挡错连是从输出表示与应用需求提出的待诊断问题，必须先在NYUv2难例验证。2026 Pixel-wise Planarity原文报告既有方法分组不精确与GT几何不一致，支持需要检查几何边界但不直接证明本方法有效。
- **source**：https://arxiv.org/abs/2609.13246
- **first_gate**：预先定义遮挡/门洞子集；若ZeroPlane基线边界问题不显著或简单mask连通域处理就解决，则不宣称研究贡献

## 2025–2026近邻覆盖检查

- - **name**：Pixel-wise Planarity for High-Precision Monocular Plane Segmentation
  - **year**：2026
  - **status**：2026-09 arXiv已核验；第三方标ECCV2026，但此处不在未核验会议官网时升级会议状态
  - **url**：https://arxiv.org/abs/2609.13246
  - **code**：https://github.com/alpayozkan/PixelwisePlanarity
  - **covered**：深度+法向+像素平面性联合区域生长、RANSAC平面拟合、严格毫米级评估。不可把此组合当创新
  - **gap**：本题只研究有限可见多边形及相邻平面投影交线/遮挡类型约束，需和该完整方法比较
- - **name**：PlaneRAS
  - **year**：2025
  - **status**：ICCV主会
  - **url**：https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_PlaneRAS_Learning_Planar_Primitives_for_3D_Plane_Recovery_ICCV_2025_paper.html
  - **covered**：显式平面基元重建/聚合/渲染，平面几何一致性已不是空白
  - **gap**：不能仅说加空间约束；本题需验证边界类型判别的收益
- - **name**：MoGe-3
  - **year**：2026
  - **status**：2026-07 arXiv；官方仓2026-08发布，未确认其顶会主会
  - **url**：https://arxiv.org/abs/2607.17967
  - **covered**：精细单目几何稀疏体素迭代修正，不能再以泛细节增强为创新
- - **name**：MoRe
  - **year**：2026
  - **status**：WACV主会，作为近邻
  - **url**：https://openaccess.thecvf.com/content/WACV2026/papers/Jung_MoRe_Monocular_Geometry_Refinement_via_Graph_Optimization_for_Cross-View_Consistency_WACV_2026_paper.pdf
  - **covered**：跨视图点/法向联合图优化；本题固定单视图，不把多视图对齐称新

## 具体研究问题

在冻结单图平面基线的情况下，将接触交线与遮挡轮廓分开建模，能否降低可见平面边界错连，同时保留原有平面法向/距离精度？

## 拟改进机制

- - **step**：1
  - **mechanism**：提取ZeroPlane实例mask、法向、距离和像素深度；检测RGB线段及T-junction候选；建立相邻平面图
  - **why**：把可见边界问题与平面参数估计分开
- - **step**：2
  - **mechanism**：对相邻平面对比两种假设：真实平面接触时3D交线应重投影到2D边界；遮挡时前后深度关系应解释T-junction，不能强迫相交
  - **why**：同样的2D边缘可能对应墙角或前景遮挡，二者应使用不同几何约束
- - **step**：3
  - **mechanism**：图优化只更新少量法向/距离残差及有限多边形顶点，保留mask证据项；对遮挡边施加深度序约束，对接触边施加投影交线距离约束
  - **why**：避免一刀切曼哈顿世界正交化或全部轮廓拉直
- - **step**：4
  - **mechanism**：以原mask、连通域/形态学清理、统一平面平滑、PixelwisePlanarity为对照，评估遮挡边与接触边分别收益
  - **why**：确定收益来自边界类型建模，而不是简单后处理

## 待检验假设

只在高证据的接触边使用交线约束，同时在遮挡边保持前后序，可减少门洞填平与前景穿插；非曼哈顿房间不应被强制正交。该假设尚未实测。

## 真实数据、直链与许可

- - **name**：NYUv2真实室内平面标注（ZeroPlane发布）
  - **real**：是
  - **download_url**：https://huggingface.co/datasets/jcleo0428/ZeroPlane_dataset/resolve/main/nyuv2_plane.zip
  - **source**：https://github.com/jcliu0428/ZeroPlane
  - **license**：作者公开处理数据；底层NYUv2图像/深度许可仍适用，不能仅因代码MIT而称所有数据MIT
  - **size_bytes**：2528721991
  - **download_verification**：HEAD200；未下载与解压
- - **name**：7Scenes真实室内平面标注（ZeroPlane发布）
  - **real**：是
  - **download_url**：https://huggingface.co/datasets/jcleo0428/ZeroPlane_dataset/resolve/main/sevenscenes_plane.zip
  - **source**：https://github.com/jcliu0428/ZeroPlane
  - **license**：遵循微软7Scenes原数据使用条款及作者处理数据说明
- - **name**：自采室内桌面照片（可选定性）
  - **real**：是
  - **download_url**：未提供 / 不适用
  - **use**：仅自己房间、不拍身份隐私；无测距GT时仅做可视化，不能充当定量真值

## 指标、官方脚本、对照与消融

- **official_metrics**：- Rand Index(RI)↑
  - Variation of Information(VOI)↓
  - Segmentation Covering(SC)↑
  - 室内平面召回：深度误差阈值0.05/0.1/0.6m
  - 平面召回：法向角阈值5°/10°/30°
- **official_scripts**：- https://github.com/jcliu0428/ZeroPlane/blob/main/train_net.py
  - https://github.com/jcliu0428/ZeroPlane/tree/main/ZeroPlane/evaluation
- **additional_metrics**：- 可见平面边界F1
  - 接触交线重投影误差
  - 遮挡次序错误率
  - 门洞/前景越界面积
  - 耗时与峰值显存
- **protocol**：先原始官方split复现，再定义固定难例子集并进行人工边界类型标注；新增GT由两人盲标/复核，不能依据最终输出挑图。遵循PixelwisePlanarity警告，毫米级误差不直接用粗糙历史平面GT当绝对正确真值。
- **controls**：- ZeroPlane官方权重
  - ZeroPlane+连通域/形态学清理
  - ZeroPlane+统一平面平滑
  - PixelwisePlanarity最新公开模型
  - 本题完整方法
- **ablation**：- 不区分遮挡/接触的统一约束
  - 移除T-junction
  - 移除3D交线投影
  - 移除原mask保真项
  - 非曼哈顿场景分层

## 基线最小命令

```bash
git clone https://github.com/jcliu0428/ZeroPlane.git
cd ZeroPlane
conda env create -f environment.yml
conda activate zeroplane
# 依官方说明安装与CUDA匹配的PyTorch和Detectron2，并编译MSDeformAttn
mkdir -p checkpoints
wget -O checkpoints/dust3r_encoder_released.pth https://huggingface.co/jcleo0428/ZeroPlane-Dust3R/resolve/main/dust3r_encoder_released.pth
python demo/demo.py --config-file configs/ZeroPlaneNYUV2/dust3r_large_dpt_bs16_50ep.yaml --input ./demo/cvpr_demo.png --out ./demo/demo_out --resize_w 640 --resize_h 480 --opts MODEL.WEIGHTS ./checkpoints/dust3r_encoder_released.pth
```

## 官方评估命令

```bash
python train_net.py --eval-only --num-gpus 1 --config-file configs/ZeroPlaneNYUV2/dust3r_large_dpt_bs16_50ep.yaml MODEL.WEIGHTS ./checkpoints/dust3r_encoder_released.pth OUTPUT_DIR ./visualizations/nyuv2_test_vis INPUT.LARGE_RESOLUTION_INPUT False INPUT.LARGE_RESOLUTION_EVAL False TEST.NO_VIS True
```

## 资源需求与许可

- **course_plan**：冻结模型批量推理+CPU线段检测/小图优化，不从零重训DUSt3R
- **gpu**：作者给出单卡demo入口；本次未执行。显存下限未知，16–24GB单卡仅为待验证规划建议，不是已证实最低配置。
- **cpu_status**：存在Detectron2/MSDeformAttn编译依赖，非当前9CPU/10GB无GPU环境的优先烟测题
- **code_license**：官方仓MIT；预训练权重/源数据应分别检查其条款
- **weight_size**：7.106GB（6.62GiB）checkpoint，载入峰值与推理还需额外内存；不建议当前10GB内存CPU环境作为首跑

## 课程算法对应

- 针孔成像与投影几何
- 平面与交线
- 消失线/线段检测
- T-junction遮挡线索
- RANSAC与最小二乘
- 图优化与鲁棒损失
- 实例分割与Transformer视觉学习

## 阶段计划

- - **time**：第1周
  - **deliverable**：复现单图平面mask/mesh，完成遮挡边界失败证据；若没有问题及时停止
- - **time**：第2周
  - **deliverable**：边界类型提取与几何图
- - **time**：第3周
  - **deliverable**：投影交线/遮挡序联合优化和消融
- - **time**：第4周
  - **deliverable**：对照最新PixelwisePlanarity、真实场景演示和误差报告

## 论文图素材与出处

- - **url**：https://raw.githubusercontent.com/jcliu0428/ZeroPlane/main/imgs/teaser.png
  - **caption**：ZeroPlane跨域单图平面恢复，Liu et al., CVPR2025
  - **usage**：仅基线展示，不标为本题结果
  - **local_path**：/workspace/shared/cv-new-topics/realworld/figures/zeroplane_teaser.png
- - **url**：https://raw.githubusercontent.com/jcliu0428/ZeroPlane/main/demo/cvpr_demo.png
  - **caption**：官方单图demo输入；需检查实际图像后使用
  - **local_path**：/workspace/shared/cv-new-topics/realworld/figures/zeroplane_input.png
- - **local_path**：/workspace/shared/cv-new-topics/realworld/sources/zeroplane_paper.pdf
  - **page_1based**：1
  - **caption**：Fig.1真实室内外平面示意
  - **rendered_local_path**：/workspace/shared/cv-new-topics/realworld/figures/zeroplane_p1.png

## 拟议方法图示逻辑

左：桌面被椅子/显示器遮挡的输入图；中上：两相交平面→墙角投影线；中下：前景遮挡→T型接点及深度序；右：有限可见多边形图，红色虚线表示禁止连接区域。拟议图是机制示意，无性能改善图。

## 运行证据状态

- **status**：未跑
- **verified**：官方论文、代码README、权重直链、NYUv2和7Scenes下载入口已核对
- **unknown**：GPU运行、显存、独立失败统计、新机制增益未测

## 创新边界

这是课程可操作的窄研究假设，不是已确认新颖成果。2026 PixelwisePlanarity已覆盖平面性+区域生长，PlaneRAS已覆盖显式平面几何；若最终只做平面拟合/平滑，应淘汰。


---

