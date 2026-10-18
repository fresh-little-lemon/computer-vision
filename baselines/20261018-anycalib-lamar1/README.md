# AnyCalib真实LaMAR2k单图baseline（2026-10-18）

官方AnyCalib-gen（320,259,771参数，DINOv2-L）源码、结构、权重和预处理未修改。CPU float32、4线程；官方默认推理尺寸364×280、默认Gauss-Newton/fallback、sample_size=-1。

## 真实结果
- 固定官方CSV第一行95419735117.jpg，原图1440×1920，非质量筛选
- 已知相机族pinhole，由调用者给定
- 推理2.592秒、加载3.640秒、含渲染完整进程峰值2758.555MiB；success=true，全部ray/内参finite
- 预测fx/fy/cx/cy：[1634.3160,1633.7643,719.1027,960.2199]；GT：[1595.1768,1595.1768,720,960]
- GT使用官方loader公式f=(H/2)/tan(vfov/2)，主点中心
- 官方原图完整网格指标：最大相对焦距误差2.4536%，平均标定射线角误差0.453592°、中位0.484473°，垂直FOV误差1.203266°，平均重投影误差15.75135原图像素
- 保存NPZ后重新计算所有官方指标，逐值一致

## 边界
只有一个真实图像、已知pinhole族。不是完整2000图benchmark、论文精度复现、自动相机族选择、裁切一致性或新方法改进。角误差为拟合pinhole相机相对GT的误差，不是直接网络ray-field指标。

## 复跑与文件
源码commit/官方下载URL/SHA256在manifest；Python3.12与CPU依赖记录在logs/pip_freeze_with_anycalib.txt。安装官方源码pip install --no-deps -e sources/AnyCalib。权重放$TORCH_HOME/hub/anycalib/anycalib_gen.pt，本机符号链接到../checkpoints/anycalib_gen.pt。解压LaMAR2k后运行logs/anycalib_lamar1.command。

官方predict已经把内参恢复到原图坐标；评分不能再次缩放。指标函数从官方siclib/eval/simple_pipeline_rays.py中原样提取执行，避免未使用的完整数据加载依赖，函数哈希在result.json。

results/raw_prediction.npz含全部ray/FOV/内参/优化成功标记和信息矩阵；raw_metadata.json记录小数组与密集shape。真实图为输入缩略图、网络ray RGB编码、标定相机与GT角误差热图。热图显示网格192×144，评分网格为原图1920×1440。不是生成图。

Fontconfig cache warnings不影响前向、评分、PNG保存；exit0，图已检查。

## 来源许可
AnyCalib：Javier Tirado-Garin和Javier Civera，ICCV2025，https://github.com/javrtg/AnyCalib ，Apache2.0。
LaMAR：Sarlin等，ECCV2022，https://github.com/microsoft/lamar-benchmark 。GeoCalib发布本2k子集，官方下载URL见manifest；CC BY4.0来源说明保留在licenses。照片仅缩放展示，保留作者、来源、许可。模型与完整数据不再分发。
