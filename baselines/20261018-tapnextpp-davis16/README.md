# TAPNext++ real DAVIS smoke（2026-10-18）

官方TAPNext++源码与结构未改，调用官方TAPNextPP.from_checkpoint/track_frame，使用官方256 checkpoint。CPU float32、4线程、torch2.14.1+cpu。

## 真实结果
- 固定选择：30视频中字母序首个bike-packing，query0，真实帧0–15（原视频69帧、25个查询点）；非挑选表现最好的片段
- 模型参数194,202,881；加载2.819秒；16帧前向42.039秒，首帧2.513秒，后续均值2.635秒/帧
- 进程峰值RSS3676.375MiB（包括数据加载和模型初始化）；全部输出finite
- 官方TAP-Vid metric：该子集AJ=1.0、δavg=1.0、OA=1.0。首个query帧按官方first-query协议排除，只评15个位置

## 严格边界
不是完整DAVIS benchmark，不是论文精度复现，不能与论文整集数字比较。16帧内该点全部可见，因此没有测试遮挡或重检测能力。完美子集分数只说明这一个容易短轨迹被正确追踪，不能泛化。小样本只用于证明官方模型、权重和真实数据通路能跑，并观察CPU成本。

## 可复跑
源码commit与官方checkpoint/data URL及SHA256在manifest.json；CPU环境在logs/pip_freeze.txt。先克隆官方tapnet并checkout精确commit；安装对应PyTorch/torchvision、numpy、Pillow、einops；pip install --no-deps -e sources/tapnet。下载manifest资源并解压DAVIS，运行logs/tapnextpp_davis16.command。无需recurrentgemma，本commit包含所需recurrent实现。

脚本不替换模型或修改网络。评分直接取官方evaluation_datasets.py中的纯NumPy compute_tapvid_metrics函数执行，函数体保持不变，SHA256在results/result.json；仅避免导入与本次运行无关的TensorFlow数据加载代码。

## 文件
results含真实预测和GT的NPZ+等价JSON、逐帧stdout、每帧耗时、真实4帧PNG对照（绿色GT，红色预测），不是生成图片。模型权重与整视频数据不包含在包内。

## 来源与许可
代码与checkpoint：Apache2.0；TAP-Vid标注：CC BY4.0。原视频bike-packing：https://www.youtube.com/watch?v=2JMcuDkvX8I，来源关系由官方DAVIS归档SOURCES.md提供。视频归创作者所有，保留完整来源/许可说明；PNG为研究结果展示截图，添加追踪标记和缩放，不作为源视频再分发。其他使用应遵循原视频许可。
