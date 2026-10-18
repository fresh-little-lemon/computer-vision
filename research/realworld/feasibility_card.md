# 独立可行性评估卡

核验日期：2026-10-18。该卡补充开题PPT所需的运行与资源细节。所有主模型均未由本研究分支实际执行，不能把命令检查、权重HEAD或论文结果写成复现成功。

## 1. D2Dewarp：资源闭环最完整，CPU需设备适配

### 已核验入口

- [CVPR 2026正式论文](https://openaccess.thecvf.com/content/CVPR2026/html/Li_D2Dewarp_Dual_Dimensions_Geometric_Representation_Learning_Based_Document_Image_Dewarping_CVPR_2026_paper.html)
- [作者源码快照1105c0f](https://github.com/xiaomore/D2Dewarp/commit/1105c0f0e44404d9a8dedb78f689078dba42221c)
- [作者model子目录](https://drive.google.com/drive/folders/1wVOeEqkUvTKYDNIyrZRRwaK781lJulM6)：GET200
- [model_weight.pt单文件](https://drive.google.com/file/d/1KcVaW0CfP5YJv6DZQ9EFzRuE9h9x40ij/view)：目录显示862.7MB。文件尚未下载，gdown成功与内容完整性未验证

```bash
# 权重下载入口，尚未实际执行
 gdown 1KcVaW0CfP5YJv6DZQ9EFzRuE9h9x40ij -O model_weight.pt
mkdir -p outputs
python predict.py --model_path /path/model_weight.pt \
  --img_path /path/DocUNet/crop --save_path outputs
```

### 平台注意事项

官方predict.py将CUDA_VISIBLE_DEVICES写为3，使用DataParallel.cuda()、输入.cuda()和未指定map_location的torch.load。在只有一张GPU或无GPU机器上不能假设原样运行。CPU适配需统一device与checkpoint映射，处理DataParallel键前缀，但不修改算法参数。适配后应标为“CPU适配版，非精确作者环境”。默认输入448，模型内attention和网络尺寸与其相关，不应为了省资源随意改尺寸后仍称原配置。

作者接口返回H/V预测和backward map，确实提供拟议研究所需中间量。源码当前输出二值H/V图，研究时应额外保存阈值化前概率图与原始map。保存路径需要先创建。

### 数据与评估

| 资源 | 公开下载 | 本次核验 |
|---|---|---|
| DocUNet实拍crop | http://vision.cs.stonybrook.edu/~kema/docwarp/crop.zip | HEAD200，294,741,912 bytes |
| DocUNet平整scan | http://vision.cs.stonybrook.edu/~kema/docwarp/scan.zip | HEAD200，436,458,210 bytes |
| DocUNet评估工具 | http://vision.cs.stonybrook.edu/~kema/docwarp/eval.zip | HEAD200，1,347,652 bytes |
| DocUNet完整原照 | http://vision.cs.stonybrook.edu/~kema/docwarp/original.zip | 来自作者页，本次未单独下载 |
| DIR300 | https://drive.google.com/drive/folders/1yySouQQ3BlH7OjnUhq4CLuvpX2KXtifX | 作者文件夹，未下载 |
| DocReal | https://drive.google.com/file/d/1fxdUMMCQoTxc-THv1LmO-Ye8XjMyPK--/view | 本次GET429，未下载 |

DocUNet的原始HTTP地址可达，试用HTTPS变体得到502。不得把改写协议的地址当成已核验直链。公开文件无需凭据，但下载后应进行本地校验。

几何评价采用MATLAB R2019a。[DocGeoNet的DocUNet脚本](https://github.com/fh2019ustc/DocGeoNet/blob/main/ssim_ld_eval_DocUNet.m)调用evalUnwarp，覆盖MS-SSIM与LD。D2Dewarp论文也报告AD，本次尚未定位独立AD实现，不能说这份脚本同时计算AD。MATLAB版本和图像插值会影响结果。

英文OCR作者环境为Windows Tesseract5.0.1.20220118与pytesseract0.3.8。[DocUNet OCR脚本](https://github.com/fh2019ustc/DocGeoNet/blob/main/OCR_eval_DocUNet.py)与[DIR300 OCR脚本](https://github.com/fh2019ustc/DocGeoNet/blob/main/OCR_eval_DIR300.py)已GET200。中文使用PaddleOCR DBNet detv4_teacher_inference、SVTR_LCNet OCRv4_rec_server_infer。其他OCR版本可做内部对照，但应单列配置，不能直接混入论文绝对成绩。

DocUNet第64对原图与扫描图方向相差180度，所有方法采用同一检查与处理。OCR Setting1为30份文档/60图，和其他论文的25份/50图协议区别记录。页面实例mask和背景文字区域需额外标注；先检查真实原照是否支持足够多页难例。

### 许可

作者README写CC BY-NC-ND4.0，根目录LICENSE请求404。不能把此仓称为MIT或默认允许公开再发布改编代码/权重。课程研究可先按作者非商业研究说明准备，发布改编成果前单独核对条款。DocUNet图像完整许可本次未明确，不重新分发原图。

## 2. ZeroPlane：几何契合度强，当前CPU机器不宜首跑

- [CVPR2025主会论文](https://openaccess.thecvf.com/content/CVPR2025/html/Liu_Towards_In-the-wild_3D_Plane_Reconstruction_from_a_Single_Image_CVPR_2025_paper.html)
- [作者源码c8d7503](https://github.com/jcliu0428/ZeroPlane/commit/c8d7503d27738749a65f702129113b5f38c9c058)
- [官方权重直链](https://huggingface.co/jcleo0428/ZeroPlane-Dust3R/resolve/main/dust3r_encoder_released.pth)：HEAD200，7,105,876,663 bytes
- [NYUv2真实平面包](https://huggingface.co/datasets/jcleo0428/ZeroPlane_dataset/resolve/main/nyuv2_plane.zip)：HEAD200，2,528,721,991 bytes
- [7Scenes真实平面包](https://huggingface.co/datasets/jcleo0428/ZeroPlane_dataset/resolve/main/sevenscenes_plane.zip)：来自作者README，本次未完整下载

```bash
python demo/demo.py \
 --config-file configs/ZeroPlaneNYUV2/dust3r_large_dpt_bs16_50ep.yaml \
 --input ./demo/cvpr_demo.png --out ./demo/demo_out \
 --resize_w 640 --resize_h 480 \
 --opts MODEL.WEIGHTS ./checkpoints/dust3r_encoder_released.pth
```

依赖包含PyTorch2.1/CUDA12.1、Detectron2、MSDeformAttn编译算子。权重文件7.106GB不是峰值RAM/VRAM，载入副本、网络参数和激活还需额外资源。当前9CPU/10GB RAM无GPU环境不适合作为该题首跑。单卡16–24GB仅为待验证的规划建议，不能写为已测最低配置。

官方train_net.py --eval-only调用ZeroPlane/evaluation，评价RI/VOI/SC以及不同深度、法向阈值下的平面召回。正式路径需要配置register_your_dataset.py中的数据根目录。新增可见边界F1、接触交线投影误差和遮挡序错误率需要新增边界类型标注，不能声称官方NPZ已经含全部标签。

官方仓LICENSE已确认MIT；DUSt3R预训练及NYUv2/7Scenes底层数据条款分别适用。原论文的明确限制主要是室外训练数据，拟议室内边界失效尚待实证。Pixel-wise Planarity已覆盖冻结几何主干、平面性、区域生长和RANSAC，正式比较中不可省略。

## 3. SubspaceAD：优先CPU小样本，但须标非论文配置

- [CVPR2026主会论文](https://openaccess.thecvf.com/content/CVPR2026/html/Lendering_SubspaceAD_Training-Free_Few-Shot_Anomaly_Detection_via_Subspace_Modeling_CVPR_2026_paper.html)
- [作者源码ef56d5c](https://github.com/CLendering/SubspaceAD/commit/ef56d5c8ab2f1feb7dda1c93b25cc3f73f0960d7)
- [Small权重直链](https://huggingface.co/facebook/dinov2-with-registers-small/resolve/main/model.safetensors)：HEAD200，88,256,200 bytes
- [VisA真实数据直链](https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar)：HEAD200，1,929,840,640 bytes

作者代码自动检测CUDA，否则CPU。预训练基础模型是DINOv2，本算法只拟合正常PCA，并不存在需要另外下载的SubspaceAD神经网络权重。完整论文配置使用DINOv2-G和672分辨率；官方SLURM脚本申请1张H100、4CPU、128GB RAM、24小时，这只是调度请求而非最低必要资源。

官方依赖未pin：torch、torchvision、transformers、opencv-python、kornia、numpy、pandas、scikit-learn、Pillow、anomalib、tqdm。main也使用scipy。运行须记录实际版本，检查torch/torchvision兼容与transformers模型导入。

### 固定真实小样本输入

原始VisA split_csv/1cls.csv每行5字段：category、data_split、label_str、image_path、mask_path。normal映射为good，其他为bad。固定pcb1第一张官方train正常图、第一张官方test正常图和第一张官方test异常图，保留真实文件路径清单，不按模型结果选图。

```text
micro_visA/
  pcb1/
    train/good/<name>.JPG
    test/good/<name>.JPG
    test/bad/<name>.JPG
    ground_truth/bad/<same_stem>.png
```

JPG必须保留大写，作者loader以*.JPG读取。mask按官方prepare_visa.py处理为非0→255，读取时最近邻缩放并二值化。可用3行micro.csv调用官方准备脚本，输出会在save-folder下额外创建1cls。全量prepare_visa.py会复制图像，磁盘紧张时避免重复保存完整tar和全量两份解压数据。

```bash
python main.py --dataset_name visa --dataset_path /path/micro_visA \
 --categories pcb1 --model_ckpt facebook/dinov2-with-registers-small \
 --image_res 224 --layers=-4,-5,-6,-7 \
 --k_shot 1 --aug_count 0 --batch_size 1 --pca_ev 0.99 \
 --seed 42 --agg_method mean --outdir results/cpu_smoke
```

默认giant的-12到-18层不能照搬到12层Small。上述Small/224/层选择/无增强均为明确课程小样本配置，与论文G/672/30增强配置分列。它可以验证输入、特征、PCA和输出流程，3张图不能证明一般检测性能。

debug_limit只截取排序后的validation/test，不截train。完整VisA中bad在good前，debug_limit2可能得到两个异常样本，图像AUROC不具意义。微型目录已经两类齐备时不传debug_limit。保持train/good非空及k_shot1，避免进入使用测试集合拟合PCA的batched-zero-shot路径。

相位诊断定义在固定预处理尺寸之后，GT同步最近邻变换，逆映射后仅比较共同有效区域。若再增加局部高分辨率，必须单独控制尺度与支持图特征处理，避免把尺度收益误判为相位收益。原官方配置已有重叠切块、背景mask等，须加入同预算对照。

代码Apache2.0；VisA的LICENSE-DATASET为CC BY4.0，已读原文确认。MVTecAD为CC BY-NC-SA4.0，官方页面需选类别下载，本卡不伪造单文件直链。

## 完成标准

- 锁定源码commit、软件版本、输入清单和命令
- 保存真实输入、输出、耗时、峰值资源与失败日志
- 小样本接口成功与完整基准复现分别标记
- 只有完成实验后才填写新方法收益，论文图始终注明作者来源
- PPT只保留应用、方法、评价与简短平台说明，安装排错留在该卡
