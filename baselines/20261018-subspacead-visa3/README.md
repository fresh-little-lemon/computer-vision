# SubspaceAD：真实VisA三图CPU可行性实跑

2026-10-18完成。官方SubspaceAD算法源码未修改；DINOv2 with registers **Small/224** 为资源受限变体，不是论文Giant/672配置，也不是完整VisA复现。

## 固定数据和配置
从官方VisA split_csv/1cls.csv按顺序取pcb1第一个train normal0499.JPG、第一个test normal0107.JPG、第一个test anomaly000.JPG。只解出这3图和异常mask；使用官方prepare_visa.py转换目录/二值mask，未按结果挑选。

1正常训练图，2测试图；CPU4线程、batch1、layers[-4,-5,-6,-7]均值、k_shot1、aug0、seed42、PCA解释方差0.99，实选154维/384；每图256个patch特征。无crop/CLAHE/kernelPCA/背景mask/specular filter/零样本测试集拟合。评分是官方重建误差，图级分数为像素前1%均值，不是概率。

## 实际运行
- 异常000：图级分数3.3862281，官方热身后推理0.0870831秒
- 正常0107：图级分数2.2189782，官方热身后推理0.0800966秒
- 平均0.0835899秒/图；完整进程23.4122秒（含首次网络下载、导入、模型加载、PCA拟合及评分），峰值697.047MiB
- 全部异常图数值finite；原始NPZ落盘后独立重算官方指标逐值一致
- 无独立验证集，阈值未标定，官方Image/Pixel F1均N/A，未从测试集调阈值

官方两个测试的I-AUROC/I-AUPR为1，P-AUROC0.9953528，AU-PRO0.984633；仅100352总像素中的52个GT阳性像素。两个样本不能支持排行榜、总体精度、论文分数或新方法改进。高像素指标不代表热图精准分割：热图仍有背景与正常物体响应。保留这些数值仅用于执行/复算审计。

## 环境与复跑
仓库commit、HF不可变revision、checkpoint及数据SHA256在manifest/provenance；完整命令在logs/subspacead_visa3.command，依赖在logs/subspace_pip_freeze.txt。官方requirements未pin，本次单独环境固定numpy2.2.6，使源码原有np.trapz继续可用，不修改算法。初次因SOCKS依赖缺失退出，补装socksio后成功；失败记录保留。pip check还列出未使用anomalib及另一项目TAP的JAX依赖，本次真实路径不导入这些模块。

训练集永远非空且k_shot1；不可误用batched_zero_shot。精确复跑可从provenance的3个不可变HF URL下载config/preprocessor/model文件并传本地目录为model_ckpt，或预填同revision缓存后HF_HUB_OFFLINE=1。官方main.py经只读profile return事件保存现有局部数组，任何模型/PCA/评分/阈值/指标函数均未替换；计时含观察器开销。

代码库意外跟踪pyc和egg-info文件，运行会再生成它们；所有.py/.toml/LICENSE与git HEAD逐字节比对一致。官方日志“eigendecomposition on GPU”为源码固定措辞；实际为CPU，环境无CUDA。

## 图与原始结果
results/raw_predictions.npz含2张未经归一化评分图、对应GT、图级标签和分数、测试耗时；pca_arrays.npz为真实PCA参数。real_anomaly_demo.png和clean三联图来自上述真实结果，输入仅缩放，GT/分数图未人为修补。两图共用同一原始色阶；左/中/右分别输入、GT、异常热图。train_reference_clean.png为唯一训练正常图。没有生成式假结果。

## 许可和出处
SubspaceAD： https://github.com/CLendering/SubspaceAD ，Apache2.0。
DINOv2-registers-Small： https://huggingface.co/facebook/dinov2-with-registers-small ，模型卡Apache2.0。
VisA：Zou, Jeong, Pemula, Zhang, Dabeer，SPot-the-Difference（2022）， https://github.com/amazon-science/spot-diff ，数据CC BY4.0。展示图作缩放、排版和分数着色；保留来源说明。完整数据和模型不再分发。
