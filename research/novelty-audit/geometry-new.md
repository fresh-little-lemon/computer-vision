# 最新会议基线新候选：LoMa重复数量偏置与匹配分配

核验日期：2026-10-18。本文件给出一个可立即做预实验的新候选，并提供Fast-FoundationStereo复现入口作为后备基线资料。启动脚本已做语法检查，算法运行结果由单独实验日志记录。

## 候选题目

**面向建筑立面复拍的重复数量感知匹配：LoMa候选归一化与几何分配研究**

### 1. 真实场景与研究问题

楼宇巡检、旧照片重定位和建筑翻修前后对齐，经常遇到相似窗格在两张照片中出现次数不同：拍摄范围变了、部分立面被遮挡，或者裁剪只保留某几排窗。期望恢复的是同一物理位置之间的对应。LoMa在ECCV2026展示了很强的稀疏匹配性能，其困难样例仍包含相似建筑结构；论文HardMatch的Doppelgänger分组mAA@10px，LoMa-B为30.3、LoMa-G为36.3，RoMa v2为34.1。这给出了明确的困难场景，但尚不能定位失效原因。[LoMa论文及附录表14](https://arxiv.org/html/2604.04931v2)

本题选择一个可从源码推导、可单独控制的原因：重复实例数量变化是否引起匹配分数的归一化偏置。LoMa使用双softmax乘积，再执行互为最大和0.1阈值；推理中未使用训练过的matchability分支。[官方实现](https://github.com/davnords/LoMa/blob/main/src/loma/loma.py)

### 2. 数学对象与拟研究机制

记匹配相似度为S，LoMa的候选分数为Pij=softmax行(S)ij×softmax列(S)ij。在一个由m个源点、n个目标点形成的等相似度重复块中，若其他相似度可以忽略，则Pij约为1/(mn)。例如4×4的歧义块给出0.0625，低于0.1。这个理想化结论是对评分算子的分析；真实网络的注意力和位置编码可能已消除部分歧义，预实验需要测出剩余影响。

拟研究“重复等价类的存在支持”与“类内具体物理对应”的分开表示。前者根据类间聚合证据和无匹配状态确定候选保留，后者在固定候选预算内由几何决定。评估量包括重复数量改变前后的真对应保留率、错误候选增量及最终几何精度。学习描述器与主干保持冻结，先研究可解释的推理规则，确认有效后再考虑轻量参数学习。

### 3. 最新近邻与真正需要证明的区别

| 近邻 | 已解决内容 | 本题的比较位置 |
|---|---|---|
| LoMa，ECCV2026，首版2026-04-06 | 扩大训练数据、描述器与匹配器规模；双softmax一对一输出 | 主baseline；同时测B128/B，保留相同提取器和点数 |
| Preserve, Then Resolve，2026-04-26，v3 2026-08-30 | 多对多top-k、概率边权、HCM/MCM与LO-RANSAC | **最直接近邻**；在同一LoMa候选图上移植其求解器；研究区别限定为学到的双softmax面对重复数量变化时的类级归一化 |
| MiHo/MOP/NCC，首版2024-11-14 | 多平面过滤与局部匹配细化 | 几何后处理对照 |
| 2026年UAV重复环境匹配 | 特征唯一性与运动约束进入线性分配 | 简单唯一性加权对照；本题使用单对RGB、没有VIO或额外双目观测 |
| Doppelgangers++，CVPR2025；MVDG，2026-10-01预印本 | 图像对可共视判断、多视图消歧 | 若扩展负图像对测试，则纳入；当前局部匹配主实验与图像对分类分列 |

来源：[LoMa](https://github.com/davnords/LoMa)、[PTR论文](https://arxiv.org/abs/2604.23670)、[PTR代码](https://github.com/LIAS-CUHKSZ/preserve_then_resolve)、[MiHo](https://github.com/fb82/MiHo)、[UAV原论文](https://doi.org/10.1016/j.rineng.2026.110864)、[Doppelgangers++](https://openaccess.thecvf.com/content/CVPR2025/html/Xiangli_Doppelgangers_Improved_Visual_Disambiguation_with_Geometric_3D_Features_CVPR_2025_paper.html)、[MVDG](https://arxiv.org/abs/2610.01098)

“多保留几个候选”“加入几何一致性”已经有成熟依据。新候选的立项证据是：数量变化产生了与真实对应正确性不同的系统效应；类级规则在相同候选数与求解预算下，优于调阈值、温度调整、恢复matchability及PTR。若这些简单对照已经解决问题，本题在预实验后结束。

### 4. 实验路线和预期产物

1. 复现LoMa-B128真实图像前向与HardMatch小样本评分，保存matches、基础矩阵和人工真值的对称极线误差。
2. 在100对validation上预先确定重复结构样例及参数。建立两类反事实实验：固定描述子仅增删相似候选，用于隔离评分算子；对真实照片改变裁剪/遮挡，完整重跑提取器，用于检验真实链路。
3. 固定总点数、候选数与求解预算，对比原LoMa、阈值/温度扫描、matchability分支、top-k+MAGSAC、PTR，再加入类级归一化。训练或选择超参数均使用validation。
4. 锁定代码和参数，在900对test上运行官方评分，分别报告所有合格静态pair和重复结构分组。补充独立拍摄的建筑立面或印刷重复平面，按建筑/物理板划分，报告真实同一位置匹配与单应误差。

产物包括一个可解释的数量偏置分析、一套可重复的真实场景干预协议，以及一项经过近邻消融的匹配规则。当前假设的实景普遍性、性能增益及资源消耗待测。

## 官方基线、模型和数据下载

### LoMa

- 论文：[LoMa: Local Feature Matching Revisited](https://arxiv.org/abs/2604.04931)，Nordström等，ECCV2026 Oral；首版2026-04-06，作者仓库接收公告2026-06-18
- 官方repo：[davnords/LoMa](https://github.com/davnords/LoMa)
- B128权重：[loma_B128.pth](https://github.com/davnords/storage/releases/download/loma/loma_B128.pth)
- B权重：[loma_B.pt](https://github.com/davnords/storage/releases/download/loma/loma_B.pt)
- 初始化依赖的DaD：[dad.pth](https://github.com/Parskatt/dad/releases/download/v0.1.0/dad.pth)
- B使用DeDoDe-G，初始化另取[DINOv2 ViT-L/14](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_pretrain.pth)；B128使用较轻的DeDoDe-B
- 许可证：作者代码MIT，继承自LightGlue的matcher部分Apache-2.0；依赖组件分别记录许可证

### HardMatch

- 官方数据repo：[davnords/HardMatch](https://github.com/davnords/HardMatch)
- **数据直链：[hardmatch.zip，作者标注660MB](https://github.com/davnords/storage/releases/download/hardmatch/hardmatch.zip)**
- [在线真实样例浏览器](https://www.davnords.com/loma/hardmatch)
- 1000对人工标注图像，100类别、9个困难组；官方代码按固定种子1337打乱类别，10类用于val、90类用于test，对应100/900对
- 评分跳过dynamic及不足8个GT对应的样本，应另记录实际纳入数；mAA@10px来自基础矩阵的GT对称极线距离阈值0至10px的平均比例
- 数据来自Wikimedia，每对各自附许可证；公开版因许可替换了约10对，官方repo的LoMa示例0.5061与论文表不能直接作为同版复现目标
- 研究使用公开版当前commit及zip SHA-256固定；所有方法共享相同划分与评分文件

以上数据和协议来自[作者README](https://github.com/davnords/HardMatch)、[划分源码](https://github.com/davnords/HardMatch/blob/main/src/hardmatch/dataset.py)、[评分源码](https://github.com/davnords/HardMatch/blob/main/src/hardmatch/benchmark.py)。

## 最小启动命令

下面命令整理自当前官方接口；本文件作者未执行模型，实测日志另存。Linux/Python3.12为官方测试环境。项目元数据要求Python≥3.10，依赖torch、torchvision≥0.23、Pillow≥12、OpenCV≥4.12、einops、tyro、tqdm。实际安装后保存pip freeze与git commit。[依赖文件](https://github.com/davnords/LoMa/blob/main/pyproject.toml)

```bash
git clone https://github.com/davnords/LoMa.git
git clone https://github.com/davnords/HardMatch.git
python3.12 -m venv .venv-loma
source .venv-loma/bin/activate
python -m pip install --upgrade pip
# CPU环境；GPU环境改用与本机CUDA兼容的PyTorch官方wheel
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -e ./LoMa -e ./HardMatch

cd LoMa
# 先用repo自带真实图像，自动下载B128与DaD权重
python /完整路径/loma_smoke.py \
  --variant b128 --side 224 --keypoints 256
```

脚本实际位置取决于保存目录；本包附[loma_smoke.py](loma_smoke.py)。该脚本用224×224张量输入，避免路径接口默认的高分辨率描述器开销。它是缩小分辨率的CPU smoke。标准官方demo为`python demo.py matcher:loma-b`；正式benchmark采用官方路径接口与4096点。

```bash
# 下载并解压官方数据，在上面的虚拟环境内运行
curl -L --fail \
  https://github.com/davnords/storage/releases/download/hardmatch/hardmatch.zip \
  -o hardmatch.zip
unzip hardmatch.zip -d data

# 本包脚本：真实validation前三个合格静态pair
python /完整路径/loma_hardmatch_sample.py \
  --data-root data/hardmatch --out outputs/loma_val_smoke --count 3
```

[loma_hardmatch_sample.py](loma_hardmatch_sample.py)保存真实PNG、可视化、原始matches、GT对应、F、逐GT对称极线误差和JSON汇总。预测坐标从224方形输入恢复到官方图像坐标；评分直接调用官方函数。F估计失败使用官方fallback并单独标注。少样本结果用于核验链路，不估计完整test性能。

正式公开版验证入口：

```bash
cd HardMatch
uv sync --extra baselines
uv run demo.py --matcher loma
```

### 资源规划

- B128 CPU smoke：已有CPU和16GB系统内存可作为尝试配置，时间/峰值内存待测
- 正式B128/B比较：建议先预留单张8–12GB GPU和20GB磁盘；这是工程预算估计，具体峰值由224 smoke逐级升至官方配置实测
- LoMa-B的“与LightGlue同大小”指matcher规模，完整DaD+DeDoDe-G流水线还包含大描述器；所有速度比较计入提取和匹配
- 本题初期只做冻结推理和求解器，不依赖重训LoMa的规模化数据与算力

## Fast-FoundationStereo：保留启动资料，暂不凑第二个研究题

已核实的CVPR2026基线是Wen、Dewan、Birchfield的[Fast-FoundationStereo](https://arxiv.org/abs/2512.11130)，首版2025-12-11。官方repo为[NVlabs/Fast-FoundationStereo](https://github.com/NVlabs/Fast-FoundationStereo)，研究[权重下载文件夹](https://drive.google.com/drive/folders/1HuTt7UIp7gQsMiDvJwVuWmKpvFzIIMap)，repo自带demo_data。预处理要求已去畸变和水平极线校正的左右图。[论文](https://arxiv.org/html/2512.11130v2)

```bash
git clone https://github.com/NVlabs/Fast-FoundationStereo.git
cd Fast-FoundationStereo
conda create -n ffs python=3.12
conda activate ffs
pip install torch==2.6.0 torchvision==0.21.0 xformers \
  --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
# 下载23-36-37目录至weights/后
python scripts/run_demo.py \
  --model_dir weights/23-36-37/model_best_bp2_serialize.pth \
  --left_file demo_data/left.png --right_file demo_data/right.png \
  --intrinsic_file demo_data/K.txt --out_dir output/ \
  --get_pc 0 --remove_invisible 0 --denoise_cloud 0 \
  --scale 1 --valid_iters 4 --max_disp 192 --zfar 100
```

官方默认CUDA路径；CPU可运行性未确认。作者报告3090、640×480、23-36-37/4迭代为41.1ms，计时范围和峰值内存均待本机复核。研究权重与商业版C-FFS分开授权，前者按repo许可证使用。LAS1是同届CVPR2026效率对手；2026-06-23预印本LAS2也已有权重和代码，进一步压低了效率边界。[LAS系列](https://github.com/TomTomTommi/LiteAnyStereo)

双目置信、在线极线校正、按不确定度调整搜索、伪标签过滤均已有近邻。本轮将主要计算预算用于验证LoMa的具体假设，再决定是否正式立项。
